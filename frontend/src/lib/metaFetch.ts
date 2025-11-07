/**
 * `lib/metaFetch.ts`
 *
 * ➤ Loads `/api/system/routes-info` and caches it in RAM.
 * ➤ Converts backend types into Zod schemas.
 * ➤ Provides helpers:
 * `loadMetaRoutes()` – returns `Map<path, { method, inputZod, outputZod }>`
 * `metaFetch()` – strongly typed fetch with auto-validation
 * `InputOf<'/p'>` – infers the input payload type
 * `OutputOf<'/p'>` – infers the response output type
 */

import { z, ZodTypeAny, ZodSchema, ZodObject } from 'zod';
import { API } from "./api";

/* ————————————————— CONSTANTS ————————————————— */
const API_ROOT      = API;
const META_ENDPOINT = '/api/system/routes-info';
const CACHE_TTL     = 1_000 * 60 * 10;           // 10 хв.
const uuidRe        = /[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/gi;
const METHODS_ALLOW_PARTIAL = new Set(['PUT', 'PATCH']);

/* ————————————————— Error class ————————————————— */
export class MetaFetchError extends Error {
    constructor(
        public readonly status: number | undefined,  // HTTP code or undefined (network error)
        public readonly devMessage: string,           // detailed for console
        public readonly userMessage: string           // short for UI
    ) {
        super(devMessage);
        this.name = 'MetaFetchError';
    }
}
const statusToUser = (s: number | undefined): string => {
    switch (s) {
        case 400:
        case 422: return 'Данные отправлены в неверном формате.';
        case 401: return 'Сначала авторизуйтесь.';
        case 403: return 'Недостаточно прав для данного действия.';
        case 404: return 'Сервис временно недоступен.';
        case 409: return 'Такие данные уже существуют.';
        case undefined: return 'Нет связи с сервером.';
        default: return 'На сервере произошла ошибка.';
    }
};

/* ————————————————— Backend meta-структури ————————————————— */
type RawFields = Record<string, string>;
interface RouteMetaRaw {
    path: string;
    methods: string[];
    input_schema: string | null;
    schema_fields: RawFields | null;
    output_schema: string | null;
    output_schema_fields: RawFields | null;
}
interface MetaRouteEntry {
    method: string;
    inputZod: ZodSchema<any>;
    outputZod: ZodSchema<any>;
}

/* ————————————————— In-memory cache ————————————————— */
let cache: { ts: number; data: Record<string, MetaRouteEntry> } | null = null;

/* ————————————————— Zod helpers ————————————————— */
const mapField = (raw: string): ZodTypeAny => {
    const t = raw.trim();

    /* enum – "admin"||"worker" */
    if (t.includes('||')) {
        return z.enum(
            t.split('||').map(s => s.trim().replace(/^"|"$/g, '')) as [string, ...string[]]
        );
    }

    /* union – "string | null" */
    if (t.includes('|')) {
        return z.union(
            t.split('|').map(p => mapField(p.trim())) as [ZodTypeAny, ZodTypeAny, ...ZodTypeAny[]]
        );
    }

    /* arrays */
    if (t.endsWith('[]')) return z.array(mapField(t.slice(0, -2)));

    /* primitives */
    switch (t) {
        case 'string':   return z.string();
        case 'number':   return z.number();
        case 'boolean':  return z.boolean();
        case 'UUID':     return z.string().uuid();
        case 'datetime': return z.string().datetime();
        case 'null':     return z.null();
        default:         return z.any(); // fallback
    }
};
const toZodObject = (fields: RawFields | null) =>
    z.object(
        Object.fromEntries(
            Object.entries(fields ?? {}).map(([k, t]) => [k, mapField(t)])
        )
    );

/* ————————————————— Meta loader ————————————————— */
export async function loadMetaRoutes(): Promise<Record<string, MetaRouteEntry>> {
    if (cache && Date.now() - cache.ts < CACHE_TTL) return cache.data;

    const res = await fetch(`${API_ROOT}${META_ENDPOINT}`);
    if (!res.ok) throw new Error('Failed to fetch meta routes');

    const raw: RouteMetaRaw[] = await res.json();
    const mapped: Record<string, MetaRouteEntry> = {};

    raw.forEach(r => {
        if (!r.schema_fields) return;                        // skip routes без input
        mapped[r.path] = {
            method   : r.methods[0] ?? 'POST',
            inputZod : toZodObject(r.schema_fields),
            outputZod: r.output_schema_fields
                ? toZodObject(r.output_schema_fields)
                : z.any(),
        };
    });

    cache = { ts: Date.now(), data: mapped };
    return mapped;
}

/* ————————————————— util: normalise path → meta-key ————————————————— */
const resolveMetaKey = (meta: Record<string, any>, rawPath: string): string | undefined => {
    if (meta[rawPath]) return rawPath;                // 1️⃣  exact match
    const normalized = rawPath.replace(uuidRe, '{id}');
    return meta[normalized] ? normalized : undefined; // 2️⃣  UUID → {id}
};

/* ————————————————— MAIN: metaFetch ————————————————— */
export async function metaFetch<Path extends string>(
    path: Path,
    body?: unknown,
    init?: Omit<RequestInit, 'method' | 'body'>
) {
    /* 1. Meta */
    const meta    = await loadMetaRoutes();
    const metaKey = resolveMetaKey(meta, path);
    const route   = metaKey ? meta[metaKey] : undefined;

    if (!route) {
        throw new MetaFetchError(404, `Route "${path}" is not described in meta`, statusToUser(404));
    }

    /* 2. Валідація payload-у */
    const needPartial = METHODS_ALLOW_PARTIAL.has(route.method.toUpperCase());
    const inputSchema = needPartial
        ? (route.inputZod as ZodObject<any>).partial()
        : route.inputZod;

    const payload =
        body === undefined ? inputSchema.parse({}) : inputSchema.parse(body);

    /* 3. HTTP fetch */
    let res: Response;
    try {
        res = await fetch(`${API_ROOT}${path}`, {
            method : route.method,
            headers: { 'Content-Type': 'application/json', ...(init?.headers || {}) },
            body   : route.method === 'GET' ? undefined : JSON.stringify(payload),
            ...init,
        });
    } catch (e: any) {
        throw new MetaFetchError(undefined, e?.message ?? 'Network error', statusToUser(undefined));
    }

    /* 4. HTTP error handling */
    if (!res.ok) {
        let dev = `HTTP ${res.status}`;
        try { dev += ` → ${JSON.stringify(await res.json())}`; } catch {}
        throw new MetaFetchError(res.status, dev, statusToUser(res.status));
    }

    /* 5. JSON + output validation */
    const json = await res.json().catch((e: any) => {
        throw new MetaFetchError(res.status, `Invalid JSON: ${e?.message}`, 'Некоректний відповідь сервера.');
    });

    try { return route.outputZod.parse(json); }
    catch (e: any) {
        throw new MetaFetchError(res.status, `Zod parse error → ${e}`, 'Сервер повернув неочікувані дані.');
    }
}

/* ————————————————— Helper TS-типы ————————————————— */
export type InputOf <
    P extends string
> = z.infer<Awaited<ReturnType<typeof loadMetaRoutes>>[P]['inputZod']>;

export type OutputOf<
    P extends string
> = z.infer<Awaited<ReturnType<typeof loadMetaRoutes>>[P]['outputZod']>;
