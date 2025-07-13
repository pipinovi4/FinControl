// src/components/layout/NavProvider.tsx
'use client';

import { usePathname } from 'next/navigation';
import Topbar   from '@/components/layout/Topbar';
import Sidebar  from '@/components/layout/Sidebar';
import AuthGuard from '@/components/guards/AuthGuard';
import React from "react";

const SHOW_PREFIXES = ['/dashboard', '/analyze', '/settings'];

export default function NavProvider({ children }: { children: React.ReactNode }) {
    const pathname = usePathname();
    const showNav  = SHOW_PREFIXES.some(p => pathname.startsWith(p));

    const content = (
        <>
            {showNav && <Topbar />}
            {showNav && <Sidebar />}
            {children}
        </>
    );

    // навігаційні сторінки → захищаємо guard-ом
    return showNav ? content : content;
}
