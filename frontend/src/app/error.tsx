"use client";

import { useEffect } from "react";
import Link from "next/link";

export default function Error({
                                  error,
                                  resetAction,
                              }: {
    error: Error;
    resetAction: () => void;
}) {
    useEffect(() => {
        console.error("🔴 Error caught by error.tsx:", error);
    }, [error]);

    return (
        <div className="bg-white relative min-h-screen flex flex-col items-center justify-center text-center px-4 sm:px-6 lg:px-8 overflow-hidden z-9999">
            {/* 💥 Background 500 */}
            <div className="absolute inset-0 flex items-center justify-center pointer-events-none select-none">
        <span className="text-[clamp(12rem,45vw,32rem)] font-black text-primary opacity-5 leading-none">
          500
        </span>
            </div>
            <div className="absolute inset-0 bg-gradient-to-br from-transparent via-blue-200/50 to-transparent animate-pulse" />

            {/* 🧠 Контент */}
            <h1 className="text-[clamp(1.75rem,5vw,3.5rem)] font-bold text-primary z-10">
                Упс! Что-то пошло не так
            </h1>
            <p className="text-muted-foreground text-sm sm:text-base md:text-lg mt-4 z-10 max-w-md sm:max-w-lg md:max-w-xl">
                Мы уже работаем над тем, чтобы всё вернулось в норму. Попробуйте
                обновить страницу или вернитесь на главную.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 mt-6 z-10">
                <button
                    onClick={() => window.location.reload()}
                    className="rounded-xl bg-primary text-primary-foreground px-5 py-2.5 text-sm sm:text-base font-semibold transition hover:opacity-90"
                >
                    Перезагрузить страницу
                </button>
                <Link
                    href="/auth/login"
                    className="rounded-xl border border-primary text-primary px-5 py-2.5 text-sm sm:text-base font-semibold transition hover:bg-primary hover:text-white"
                >
                    На главную
                </Link>
            </div>
        </div>
    );
}
