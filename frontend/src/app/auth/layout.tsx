import React from 'react'

type AuthLayoutProps = {
    children: React.ReactNode;
};

export default function AuthLayout({children}: AuthLayoutProps) {
    return (
        // flex flex-col items-center justify-center
        <div className="w-full h-full">
            {children}
        </div>
    )
}