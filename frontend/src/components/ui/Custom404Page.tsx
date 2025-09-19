import React from "react";
import Link from "next/link";


const Custom404Page: React.FC = () => {
    return (
        <div className="bg-white relative min-h-screen flex flex-col items-center justify-center text-center px-4 sm:px-6 lg:px-8 overflow-hidden z-9999">
            {/* 🎯 Background 404 */}
            <div className="absolute inset-0 flex items-center justify-center pointer-events-none select-none">
                <span className="text-[clamp(12rem,45vw,32rem)] font-black text-primary opacity-5 leading-none">
                    404
                </span>
            </div>
            <div className="absolute inset-0 bg-gradient-to-br from-transparent via-blue-200/50 to-transparent animate-pulse" />

            {/* 🧠 Контент */}
            <h1 className="text-[clamp(1.75rem,5vw,3.5rem)] font-bold text-primary z-10">
                Страница не найдена
            </h1>
            <p className="text-muted-foreground text-sm sm:text-base md:text-lg mt-4 z-10 max-w-md sm:max-w-lg md:max-w-xl">
                Возможно, вы ввели неверный адрес или страница была перемещена. Пожалуйста, вернитесь на главную или воспользуйтесь меню для навигации.
            </p>
            <Link
                href="/dashboard"
                className="mt-6 inline-block rounded-xl bg-primary text-primary-foreground px-5 py-2.5 text-sm sm:text-base font-semibold transition hover:opacity-90 z-10"
            >
                На главную
            </Link>
        </div>
    )
}

export default Custom404Page;