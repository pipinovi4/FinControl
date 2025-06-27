"use client";

import React, { useState } from "react";

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

export default function Home() {
    const [routePath, setRoutePath] = useState<string>("");
    const [routeData, setRouteData] = useState<null | {
        method: string;
        inputSchema: any;
        outputSchema: any;
    }>(null);

    const fetchAndCacheRoutes = async () => {
        const res = await fetch("http://127.0.0.1:8000/api/system/routes-info");
        if (!res.ok) {
            console.error("❌ Failed to fetch routes info");
            return;
        }

        const allRoutes: RouteMeta[] = await res.json();
        const parsedMeta: Record<string, any> = {};

        for (const route of allRoutes) {
            if (!route.input_schema || !route.schema_fields) continue;

            parsedMeta[route.path] = {
                method: route.methods[0] ?? "POST",
                inputSchema: transformFields(route.schema_fields),
                outputSchema: transformFields(route.output_schema_fields),
            };
        }

        localStorage.setItem("meta_routes", JSON.stringify(parsedMeta));
        console.log("✅ Cached routes:", parsedMeta);
    };

    const handleGetSchema = () => {
        const raw = localStorage.getItem("meta_routes");
        if (!raw) {
            alert("⚠️ No cached data found. Please fetch first.");
            return;
        }

        const metaRoutes = JSON.parse(raw);
        const target = routePath.trim();

        if (target in metaRoutes) {
            setRouteData(metaRoutes[target]);
        } else {
            alert(`❌ Route not found: ${target}`);
        }
    };

    return (
        <div className="min-h-screen bg-white p-8 flex flex-col items-center gap-6">
            <h1 className="text-2xl font-bold">Meta Route Fetcher</h1>

            <div className="flex gap-4">
                <button
                    onClick={fetchAndCacheRoutes}
                    className="px-4 py-2 bg-blue-600 text-white rounded-md"
                >
                    Fetch & Cache All
                </button>
            </div>

            <div className="w-full max-w-2xl mt-4 flex flex-col items-center gap-4">
                <input
                    value={routePath}
                    onChange={(e) => setRoutePath(e.target.value)}
                    placeholder="/api/entities/read/broker/{id}"
                    className="w-full px-4 py-2 border rounded-md"
                />
                <button
                    onClick={handleGetSchema}
                    className="px-4 py-2 bg-black text-white rounded-md"
                >
                    Get Schema Info
                </button>
            </div>

            {routeData && (
                <div className="w-full max-w-3xl bg-gray-100 border p-6 rounded-md shadow-sm mt-6">
                    <h2 className="text-xl font-semibold mb-2">🔗 Endpoint Info</h2>
                    <p><b>Method:</b> {routeData.method}</p>

                    <div className="mt-4">
                        <h3 className="font-semibold">📤 Input Schema:</h3>
                        <pre className="bg-white p-3 mt-1 rounded overflow-auto text-sm">
                            {JSON.stringify(routeData.inputSchema, null, 2)}
                        </pre>
                    </div>

                    <div className="mt-4">
                        <h3 className="font-semibold">📥 Output Schema:</h3>
                        <pre className="bg-white p-3 mt-1 rounded overflow-auto text-sm">
                            {JSON.stringify(routeData.outputSchema, null, 2)}
                        </pre>
                    </div>
                </div>
            )}
        </div>
    );
}
