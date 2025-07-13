"use client";

import { useState } from "react";
import { loadMetaRoutes } from "@/lib/metaFetch";
import { ZodTypeAny, ZodObject } from "zod";

// 🔍 Рекурсивна трансляція Zod → читабельне представлення
const zodToReadableType = (zod: ZodTypeAny): any => {
    if (!zod || typeof zod !== "object" || !("_def" in zod)) return "unknown";

    const def = zod._def;

    switch (def.typeName) {
        case "ZodString":
            return "string";
        case "ZodNumber":
            return "number";
        case "ZodBoolean":
            return "boolean";
        case "ZodLiteral":
            return JSON.stringify(def.value);
        case "ZodArray":
            return `${zodToReadableType(def.type)}[]`;
        case "ZodUnion":
            return def.options.map(zodToReadableType).join(" | ");
        case "ZodNullable":
        case "ZodOptional":
        case "ZodDefault":
            return `${zodToReadableType(def.innerType)} | null`;
        case "ZodObject":
            const shape = typeof def.shape === "function" ? def.shape() : def.shape;
            const result: Record<string, any> = {};
            for (const key in shape) {
                result[key] = zodToReadableType(shape[key]);
            }
            return result;
        default:
            return "any";
    }
};

export default function RouteInspector() {
    const [routePath, setRoutePath] = useState("");
    const [result, setResult] = useState<null | {
        method: string;
        inputSchema: any;
        outputSchema: any;
    }>(null);

    const handleInspect = async () => {
        try {
            const meta = await loadMetaRoutes();
            if (!(routePath in meta)) {
                alert("Route not found in meta");
                return;
            }

            const route = meta[routePath];
            const inputParsed = zodToReadableType(route.inputZod);
            const outputParsed = zodToReadableType(route.outputZod);

            setResult({
                method: route.method,
                inputSchema: inputParsed,
                outputSchema: outputParsed,
            });
        } catch (err) {
            console.error("❌ Failed to inspect route:", err);
        }
    };

    return (
        <div className="min-h-screen p-8 flex flex-col items-center gap-6">
            <h1 className="text-2xl font-bold">🔍 Route Inspector</h1>

            <input
                value={routePath}
                onChange={(e) => setRoutePath(e.target.value)}
                placeholder="/api/auth/register/client/bot"
                className="px-4 py-2 border rounded-md w-full max-w-xl"
            />

            <button
                onClick={handleInspect}
                className="px-4 py-2 bg-black text-white rounded-md"
            >
                Inspect Route
            </button>

            {result && (
                <div className="w-full max-w-3xl mt-8 bg-gray-100 border rounded p-6">
                    <p className="text-lg font-semibold mb-2">📌 Method: {result.method}</p>

                    <div className="mb-4">
                        <h3 className="font-semibold">📤 Input Schema</h3>
                        <pre className="bg-white p-3 mt-2 rounded text-sm overflow-x-auto">
                            {JSON.stringify(result.inputSchema, null, 2)}
                        </pre>
                    </div>

                    <div>
                        <h3 className="font-semibold">📥 Output Schema</h3>
                        <pre className="bg-white p-3 mt-2 rounded text-sm overflow-x-auto">
                            {JSON.stringify(result.outputSchema, null, 2)}
                        </pre>
                    </div>
                </div>
            )}
        </div>
    );
}
