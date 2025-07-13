'use client';

import React, { useState } from 'react';
import { metaFetch, loadMetaRoutes } from '@/lib/metaFetch';
import { cn } from '@/lib/utils';

/* ---------- локальные константы ---------- */
const ROLES = ['admin', 'worker', 'broker', 'client'] as const;

/* -------------------------------------------------------------------------- */
/*                               React-страница                               */
/* -------------------------------------------------------------------------- */

export default function UserEntityLookupPage() {
    const [id, setId] = useState('');
    const [role, setRole] = useState<(typeof ROLES)[number]>('client');
    const [result, setResult] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const [error, setErr] = useState<string | null>(null);

    const handleLookup = async () => {
        setLoading(true);
        setErr(null);
        setResult(null);

        const staticPath = `/api/entities/read/${role}/{id}`;

        try {
            const meta = await loadMetaRoutes();
            const route = meta[staticPath];
            if (!route) throw new Error('Неизвестный путь');

            const res = await fetch(`http://127.0.0.1:8000/api/entities/read/${role}/${id}`, {
                method: route.method,
                headers: { 'Content-Type': 'application/json' },
            });

            if (!res.ok) throw new Error('Ошибка сервера');

            const json = await res.json();
            const parsed = route.outputZod.parse(json);

            setResult(parsed);
        } catch (err: any) {
            setErr(err?.message || 'Ошибка запроса');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="md:ml-60 min-h-screen bg-[#F8FAFF] font-[var(--font-dm-sans)] p-6">
            <h1 className="mb-6 text-2xl font-bold text-[#2B3674]">
                Получить пользователя по ID
            </h1>

            {/* ——— Фильтры ——— */}
            <div className="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:max-w-lg">
                <Input
                    placeholder="ID пользователя"
                    value={id}
                    onChange={(e) => setId(e.target.value)}
                />

                <select
                    className="rounded-xl border border-input bg-white px-4 py-2 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-1"
                    value={role}
                    onChange={(e) => setRole(e.target.value as any)}
                >
                    {ROLES.map((r) => (
                        <option key={r} value={r}>
                            {r.charAt(0).toUpperCase() + r.slice(1)}
                        </option>
                    ))}
                </select>
            </div>

            <Button onClick={handleLookup} disabled={!id || loading}>
                {loading ? 'Поиск…' : 'Найти'}
            </Button>

            {error && <p className="mt-4 text-red-500">{error}</p>}

            {result && (
                <pre className="mt-6 max-w-full overflow-x-auto rounded-xl bg-gray-100 p-4 text-sm">
          {JSON.stringify(result, null, 2)}
        </pre>
            )}
        </div>
    );
}

/* -------------------------------------------------------------------------- */
/*                               Локальный UI                                */
/* -------------------------------------------------------------------------- */

/* ——— Input ——— */
type InputProps = React.InputHTMLAttributes<HTMLInputElement>;
const Input = React.forwardRef<HTMLInputElement, InputProps>(
    ({ className, type = 'text', ...props }, ref) => (
        <input
            type={type}
            ref={ref}
            className={cn(
                'w-full rounded-xl border border-input bg-white px-4 py-2 text-sm shadow-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-1',
                className
            )}
            {...props}
        />
    )
);
Input.displayName = 'Input';

/* ——— Button ——— */
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: 'default' | 'outline';
}
const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
    ({ className, variant = 'default', disabled, ...props }, ref) => {
        const base =
            'inline-flex items-center justify-center rounded-xl px-4 py-2 text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none';
        const variants = {
            default: 'bg-[#4B22F4] text-white hover:bg-[#3818c7]',
            outline:
                'border border-[#4B22F4] text-[#4B22F4] hover:bg-[#F3F3FF] hover:text-[#4B22F4]',
        };

        return (
            <button
                ref={ref}
                disabled={disabled}
                className={cn(base, variants[variant], className)}
                {...props}
            />
        );
    }
);
Button.displayName = 'Button';
