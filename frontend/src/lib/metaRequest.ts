type MetaRoutes = Record<
    string,
    {
        method: string;
        inputSchema: any;
        outputSchema: any;
    }
>;

interface RouteMeta {
    path: string;
    methods: string[];
    name: string;
    summary: string | null;
    tags: string[];
    input_schema: string | null;
    schema_fields: Record<string, string> | null;
    output_schema: string | null;
    output_schema_fields: Record<string, string> | null;
}

const parseType = (typeStr: string): any => {
    const cleaned = typeStr.trim();

    if (cleaned.includes("||")) {
        const options = cleaned.split("||").map((s) => s.trim().replace(/^"|"$/g, ""));
        return options[0] ?? "";
    }

    if (cleaned.includes("|")) {
        const parts = cleaned.split("|").map((s) => s.trim());
        return parseType(parts.find((p) => p !== "null") || "any");
    }

    if (cleaned.endsWith("[]")) {
        const baseType = cleaned.slice(0, -2);
        return [parseType(baseType)];
    }

    switch (cleaned) {
        case "string":
            return "";
        case "number":
            return 0;
        case "boolean":
            return false;
        case "null":
            return null;
        case "UUID":
            return "00000000-0000-0000-0000-000000000000";
        case "datetime":
            return new Date().toISOString();
        case "any":
        default:
            return null;
    }
};

const transformFields = (fields: Record<string, string> | null): Record<string, any> => {
    const transformed: Record<string, any> = {};
    if (!fields) return transformed;

    for (const [key, type] of Object.entries(fields)) {
        transformed[key] = parseType(type);
    }

    return transformed;
};

const validateAgainstMeta = (body: any, metaShape: any): boolean => {
    for (const key in metaShape) {
        if (!(key in body)) return false;

        const expected = metaShape[key];
        const actual = body[key];

        if (Array.isArray(expected)) {
            if (!Array.isArray(actual)) return false;
        } else if (expected !== null && typeof expected !== typeof actual) {
            return false;
        }
    }
    return true;
};

export default async function fetchWithMeta(
    path: string,
    customBody?: any,
    options?: RequestInit
): Promise<Response> {
    let metaRoutes: MetaRoutes;

    const raw = localStorage.getItem("meta_routes");

    if (!raw) {
        // Fetch and cache
        const res = await fetch("http://127.0.0.1:8000/api/system/routes-info");
        if (!res.ok) throw new Error("❌ Failed to fetch meta routes");

        const routes: RouteMeta[] = await res.json();
        const parsed: MetaRoutes = {};

        for (const route of routes) {
            if (!route.input_schema || !route.schema_fields) continue;

            parsed[route.path] = {
                method: route.methods[0] ?? "POST",
                inputSchema: transformFields(route.schema_fields),
                outputSchema: transformFields(route.output_schema_fields),
            };
        }

        localStorage.setItem("meta_routes", JSON.stringify(parsed));
        metaRoutes = parsed;
    } else {
        metaRoutes = JSON.parse(raw);
    }

    if (!(path in metaRoutes)) {
        throw new Error(`❌ Route ${path} not found in cached meta`);
    }

    const { method, inputSchema } = metaRoutes[path];
    const body = customBody ?? inputSchema;

    if (customBody && !validateAgainstMeta(customBody, inputSchema)) {
        console.error("❌ Invalid body provided:", customBody);
        console.error("📌 Expected shape:", inputSchema);
        throw new Error(`❌ Body doesn't match input schema for ${path}`);
    }

    return fetch(`http://127.0.0.1:8000${path}`, {
        method,
        headers: {
            "Content-Type": "application/json",
            ...(options?.headers || {}),
        },
        body: method !== "GET" ? JSON.stringify(body) : undefined,
        ...options,
    });
}
