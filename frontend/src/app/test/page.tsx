'use client';

import { useState } from 'react';
import { roleBasedCrudService } from '@/services/crudService';

export default function CrudTestPage() {
    const [result, setResult] = useState<any>(null);
    const [error, setError] = useState<string | null>(null);
    const [inputId, setInputId] = useState('');

    const handle = async (fn: () => Promise<any>) => {
        setError(null);
        setResult(null);
        try {
            const res = await fn();
            setResult(res);
        } catch (err: any) {
            setError(err?.message || 'Unknown error');
        }
    };

    return (
        <main className="min-h-screen bg-[#F8FAFF] p-8 font-dmSans">
            <h1 className="text-2xl font-bold text-[#2B3674] mb-6">🧪 CRUD Tester</h1>

            <div className="mb-4 flex gap-2">
                <input
                    value={inputId}
                    onChange={(e) => setInputId(e.target.value)}
                    placeholder="ID (для get / update / delete)"
                    className="border border-gray-300 px-4 py-2 rounded-md text-sm w-72"
                />

                <button
                    onClick={() => handle(() => roleBasedCrudService.get(inputId || undefined))}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm"
                >
                    GET
                </button>

                <button
                    onClick={() =>
                        handle(() =>
                            roleBasedCrudService.create({
                                email: `user${Math.floor(Math.random() * 9999)}@mail.com`,
                                password: 'password123',
                                telegram_id: `${Math.random().toString(36).slice(2, 10)}`,
                                telegram_username: `user_${Math.random().toString(36).slice(2, 6)}`
                            })
                        )
                    }
                    className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md text-sm"
                >
                    CREATE
                </button>

                <button
                    onClick={() =>
                        handle(() =>
                            roleBasedCrudService.update(inputId, {
                                display_name: 'Updated Name ' + Math.floor(Math.random() * 100),
                            })
                        )
                    }
                    className="bg-yellow-500 hover:bg-yellow-600 text-white px-4 py-2 rounded-md text-sm"
                >
                    UPDATE
                </button>

                <button
                    onClick={() => handle(() => roleBasedCrudService.delete(inputId))}
                    className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm"
                >
                    DELETE
                </button>
            </div>

            {result && (
                <pre className="mt-6 bg-white p-4 rounded-md shadow text-sm overflow-x-auto">
                    {JSON.stringify(result, null, 2)}
                </pre>
            )}

            {error && (
                <p className="mt-4 text-red-500 font-semibold text-sm">Error: {error}</p>
            )}
        </main>
    );
}
