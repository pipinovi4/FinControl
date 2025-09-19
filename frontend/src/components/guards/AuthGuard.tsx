// src/parts/guards/AuthGuard.tsx
'use client';

import { useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import LoadingScreen from '@/components/ui/LoadingScreen';

export default function AuthGuard({ children }: { children: React.ReactNode }) {
    const [ready, setReady] = useState(false);
    const router = useRouter();
    const pathname = usePathname();

    useEffect(() => {
        const user = localStorage.getItem('user');

        const isAuthLogin    = pathname.startsWith('/auth/login');
        const isAuthRegister = pathname.startsWith('/auth/register');
        const isAuthLogout   = pathname.startsWith('/auth/logout');
        const isAuthPage     = pathname.startsWith('/auth');

        /* ──────────────── 1. Користувач залогінений ──────────────── */
        if (user) {
            // якщо він намагається відкрити login або register → перенаправляємо
            if (isAuthLogin || isAuthRegister) {
                router.replace('/dashboard');         // 👉 змінити на свій route
                return;
            }
            setReady(true);
            return;
        }

        /* ──────────────── 2. Користувач НЕ залогінений ───────────── */
        localStorage.removeItem('accessToken');   // очищаємо можливі крихти

        // не пускаємо на /auth/logout
        if (isAuthLogout) {
            router.replace('/auth/login');
            return;
        }

        // якщо стукають у будь-яку не-/auth-сторінку без user → login
        if (!isAuthPage) {
            router.replace('/auth/login');          // або '/auth/register'
            return;
        }

        // доступні /auth/login та /auth/register
        setReady(true);
    }, [pathname, router]);

    return ready ? <>{children}</> : null;
}
