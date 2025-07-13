'use client';

import React, { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Cookies from 'js-cookie';

type AuthLayoutProps = {
    children: React.ReactNode;
};

export default function AuthLayout({ children }: AuthLayoutProps) {
    const router = useRouter();

    useEffect(() => {
        const accessToken = Cookies.get('accessToken');
        const refreshToken = Cookies.get('refreshToken');

        if (accessToken || refreshToken) {
            router.replace('/dashboard');
        }
    }, [router]);

    return (
        <div className="w-full h-full">
            {children}
        </div>
    );
}
