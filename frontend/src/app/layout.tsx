import './globals.css';
import React from 'react';
import type { Metadata } from 'next';
import { ReactQueryProvider } from '@/components/ReactQueryProvider';
import NavProvider from '@/components/layout/NavProvider';   // ⬅️ добавлено
import { DM_Sans, Poppins } from 'next/font/google';
import AuthGuard from "@/components/guards/AuthGuard";
import {ProfileProvider} from "@/components/profile/useProfileModal";
import ProfileModal from "@/components/profile/ProfileModal";

const dmSans = DM_Sans({
    variable: '--font-dm-sans',
    subsets : ['latin', 'latin-ext'],
    weight  : ['1000'],
});

const poppins = Poppins({
    variable: '--font-poppins',
    subsets : ['latin', 'latin-ext'],
    weight  : ['400', '700'],
});

export const metadata: Metadata = {
    title: 'Fincontrol',
    description: 'Система управления кредитами и клиентами.',
    // icons: {
    //     icon: "/avatar.ico",
    // },
};

export default function RootLayout({
                                       children,
                                   }: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en" className="h-full">
        <body
            className={` 
    ${dmSans.variable} ${poppins.variable} 
    antialiased min-h-screen bg-[#F8FAFF] overflow-x-hidden   /* базовий фон, як у Splash */ 
  `}
        >
        <ReactQueryProvider>
            <ProfileProvider>
                {/* глобальна модалка (рендериться/ховається сама) */}
                <ProfileModal />
                <AuthGuard>
                    <NavProvider>{children}</NavProvider>
                </AuthGuard>
            </ProfileProvider>
        </ReactQueryProvider>
        </body>
        </html>
    );
}
