"use client";

import React from "react";

interface AuthCardProps {
    children: React.ReactNode;
}

export default function AuthCard({ children }: AuthCardProps) {
    return (
        <div className="w-full max-w-md p-8 sm:p-10 bg-white rounded-2xl shadow-2xl border border-border transition-shadow duration-300 hover:shadow-[0_10px_50px_rgba(43,54,116,0.2)]">
            <div className="p6 sm:p-8">
                {children}
            </div>
        </div>
    );
}

