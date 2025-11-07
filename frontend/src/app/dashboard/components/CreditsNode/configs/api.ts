// api.ts
export type DeletedFilter = "active" | "only" | "all";

const API = process.env.NEXT_PUBLIC_API_URL ?? "";

/* ---------------------------------- helpers ---------------------------------- */
function h(token: string) {
    return { "Content-Type": "application/json", Authorization: token };
}
function baseUrl(b?: string) {
    return (b ?? API).replace(/\/+$/, "") + "/";
}
function createUrl(path: string, b?: string) {
    const p = path.replace(/^\/+/, "");
    return new URL(p, baseUrl(b));
}

export class ApiError extends Error {
    status: number;
    body?: any;
    constructor(message: string, status: number, body?: any) {
        super(message);
        this.status = status;
        this.body = body;
    }
}

async function fetchOk(url: string, init?: RequestInit): Promise<void> {
    let res: Response;
    try { res = await fetch(url, init); } catch (err:any) {
        throw new ApiError(err?.message || "Network error", 0);
    }
    if (!res.ok) {
        let text = "";
        try { text = await res.text(); } catch {}
        let msg = text || res.statusText || "Request failed";
        try {
            const maybeJson = text ? JSON.parse(text) : null;
            if (maybeJson?.detail) msg = typeof maybeJson.detail === "string" ? maybeJson.detail : JSON.stringify(maybeJson.detail);
        } catch {}
        throw new ApiError(msg, res.status, text);
    }
}

async function fetchJSON<T>(url: string, init?: RequestInit): Promise<T> {
    let res: Response;
    try {
        res = await fetch(url, init);
    } catch (err: any) {
        // суто мережеві штуки: CORS, відвалився сервер, Abort, тощо
        const msg = err?.message || "Network error";
        throw new ApiError(msg, 0);
    }

    if (!res.ok) {
        let text = "";
        try {
            text = await res.text();
        } catch {
            /* ignore */
        }
        // якщо бек повернув JSON з detail — витягнемо його
        let msg = text || res.statusText || "Request failed";
        try {
            const maybeJson = text ? JSON.parse(text) : null;
            if (maybeJson?.detail) msg = typeof maybeJson.detail === "string" ? maybeJson.detail : JSON.stringify(maybeJson.detail);
        } catch {/* not json */}
        throw new ApiError(msg, res.status, text);
    }

    try {
        return (await res.json()) as T;
    } catch {
        throw new ApiError("Bad JSON in response", res.status);
    }
}

function normSearch(q?: string) {
    const s = q?.replace(/\s+/g, " ").trim();
    return s && s.length ? s : undefined;
}

/* ----------------------------------- lists ----------------------------------- */

export async function fetchAdminCredits({
                                            token, base, skip, limit, statuses, search, deleted,
                                        }: {
    token: string;
    base?: string;
    skip: number;
    limit: number;
    statuses?: string[];
    search?: string;
    deleted?: DeletedFilter;
}) {
    const u = createUrl("dashboard/admin/credits", base);
    u.searchParams.set("skip", String(skip));
    u.searchParams.set("limit", String(limit));
    if (deleted) u.searchParams.set("deleted", deleted);
    (statuses ?? []).forEach((s) => u.searchParams.append("statuses", s));
    const q = normSearch(search);
    if (q) u.searchParams.set("search", q);

    return fetchJSON<{ credits: any[]; total: number }>(u.toString(), {
        headers: h(token),
        cache: "no-store",
    });
}

export async function fetchAdminClients({
                                            token, base, skip, limit, search, id, deleted,
                                        }: {
    token: string;
    base?: string;
    skip: number;
    limit: number;
    search?: string;
    id: string;            // якщо бек справді вимагає admin_id у path — лишаємо
    deleted?: DeletedFilter;
}) {
    const u = createUrl(`dashboard/admin/clients/${id}`, base);
    u.searchParams.set("skip", String(skip));
    u.searchParams.set("limit", String(limit));
    const q = normSearch(search);
    if (q) u.searchParams.set("search", q);
    if (deleted) u.searchParams.set("deleted", deleted);

    return fetchJSON<{ clients: any[]; total: number }>(u.toString(), {
        headers: h(token),
        cache: "no-store",
    });
}

export async function fetchClientOne({ token, base, id }: { token: string; base?: string; id: string; }) {
    const u = createUrl(`dashboard/admin/client/${id}`, base);
    return fetchJSON(u.toString(), { headers: h(token), cache: "no-store" });
}

export async function adminUpdateCredit({ token, base, id, patch }: { token: string; base?: string; id: string; patch: any; }) {
    const u = createUrl(`dashboard/admin/credits/${id}`, base);
    return fetchJSON(u.toString(), { method: "PATCH", headers: h(token), body: JSON.stringify(patch) });
}

export async function adminUpdateClient({ token, base, id, patch }: { token: string; base?: string; id: string; patch: any; }) {
    const u = createUrl(`dashboard/admin/client/${id}`, base);
    return fetchJSON(u.toString(), { method: "PATCH", headers: h(token), body: JSON.stringify(patch) });
}

export async function adminChangeStatus({ token, base, id, status }: { token: string; base?: string; id: string; status: string; }) {
    const u = createUrl(`dashboard/admin/credits/${id}/status`, base);
    u.searchParams.set("new_status", status);
    return fetchJSON(u.toString(), { method: "PATCH", headers: { Authorization: token } });
}

export async function adminCreateCredit({ token, base, client_id, amount }: { token: string; base?: string; client_id: string; amount: number; }) {
    const u = createUrl("dashboard/admin/credits", base);
    return fetchJSON(u.toString(), { method: "POST", headers: h(token), body: JSON.stringify({ client_id, amount }) });
}

export async function adminDeleteCredit({ token, base, id }:{
    token:string; base?:string; id:string;
}) {
    const u = createUrl(`dashboard/admin/credits/${id}`, base);
    await fetchOk(u.toString(), { method: "DELETE", headers: { Authorization: token } });
    return true;
}

export async function adminDeleteClient({ token, base, id }:{
    token:string; base?:string; id:string;
}) {
    const u = createUrl(`dashboard/admin/user/${id}/deactivate`, base);
    await fetchOk(u.toString(), { method: "PATCH", headers: { Authorization: token } });
    return true;
}

export async function adminRestoreClient({ token, base, id }:{
    token:string; base?:string; id:string;
}) {
    const u = createUrl(`dashboard/admin/user/${id}/restore`, base);
    await fetchOk(u.toString(), { method: "PATCH", headers: { Authorization: token } });
    return true;
}

export async function adminRestoreCredit({ token, base, id }: { token: string; base?: string; id: string; }) {
    const u = createUrl(`dashboard/admin/credits/${id}/restore`, base);
    return fetchOk(u.toString(), { method: "PATCH", headers: h(token) });
}

export async function adminAddComment({
                                          token, base, id, text,
                                      }: { token:string; base?:string; id:string; text:string; }) {
    const u = createUrl(`dashboard/admin/credits/${id}/comment`, base);
    return fetchJSON(u.toString(), {
        method: "POST",
        headers: h(token),
        body: JSON.stringify({ text }),
    });
}