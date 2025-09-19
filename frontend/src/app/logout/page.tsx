// src/app/(auth)/logout/page.tsx
'use client';

import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { authService } from '@/services/AuthService';
import { cn } from '@/lib/utils';

/* —————————————————————————————————— */

export default function LogoutPage() {
    const router = useRouter();
    const [state, setState] = useState<'idle' | 'loading' | 'error'>('idle');

    const doLogout = async () => {
        setState('loading');
        try {
            await authService.logout();
            router.replace('/auth/login');
        } catch (e) {
            console.error('Logout failed:', e);
            setState('error');
        }
    };

    /* ——— UI ——— */
    return (
        <main className="flex min-h-screen flex-col items-center justify-center bg-[#F8FAFF] font-[var(--font-dm-sans)] px-4">
            <div className="w-full max-w-xs rounded-2xl bg-white p-8 shadow-lg text-center flex flex-col gap-4">
                {/* ---------- idle ---------- */}
                {state === 'idle' && (
                    <>
                        <h1 className="text-xl font-bold text-[#2B3674]">Выйти из аккаунта?</h1>

                        <button
                            onClick={doLogout}
                            className="cursor-pointer w-full rounded-xl bg-[#4B22F4] px-4 py-2 text-sm font-medium text-white transition hover:bg-[#3818c7]"
                        >
                            Выйти из аккаунта
                        </button>

                        <button
                            onClick={() => router.push('/dashboard')}
                            className="cursor-pointer w-full rounded-xl border border-[#4B22F4] px-4 py-2 text-sm font-medium text-[#4B22F4] transition hover:bg-[#F3F3FF]"
                        >
                            Вернуться на главную
                        </button>
                    </>
                )}

                {/* ---------- loading ---------- */}
                {state === 'loading' && (
                    <>
                        <span className="mx-auto mb-4 block h-6 w-6 animate-spin rounded-full border-4 border-[#4B22F4] border-t-transparent" />
                        <p className="font-semibold text-[#2B3674]">Выходим…</p>
                    </>
                )}

                {/* ---------- error ---------- */}
                {state === 'error' && (
                    <>
                        <p className="mb-4 text-lg font-bold text-red-500">Не удалось выйти</p>

                        <button
                            onClick={doLogout}
                            className="mb-3 w-full rounded-xl bg-[#4B22F4] px-4 py-2 text-sm font-medium text-white transition hover:bg-[#3818c7]"
                        >
                            Попробовать ещё раз
                        </button>

                        <button
                            onClick={() => router.push('/dashboard')}
                            className="w-full rounded-xl border border-[#4B22F4] px-4 py-2 text-sm font-medium text-[#4B22F4] transition hover:bg-[#F3F3FF]"
                        >
                            Вернуться на главную
                        </button>
                    </>
                )}
            </div>

            <p
                className={cn(
                    'mt-6 text-xs text-[#8F9BBA] transition-opacity',
                    state === 'loading' ? 'opacity-100' : 'opacity-0'
                )}
            >
                Redirecting to login…
            </p>
        </main>
    );
}
