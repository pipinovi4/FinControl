'use client';

import { useState, useEffect } from "react";
import { AnalyzeIcon, HouseIcon, LockIcon, LogInIcon, BurgerIcon } from "@/components/icons";
import clsx from 'clsx';
import { usePathname, useRouter } from 'next/navigation';

// Sidebar menu items
const sidebarItems = [
    { label: "Панель управления", href: "/dashboard", icon: HouseIcon },
    { label: "Аналитика", href: "/analyze", icon: AnalyzeIcon },
    { label: "Авторизация", href: "/auth/register", icon: LogInIcon, requireLogin: false },
    { label: "Выход", href: "/logout", icon: LockIcon, requireLogin: true },
];

const Sidebar = () => {
    const pathname = usePathname(); // current route
    const router = useRouter();     // router for manual navigation

    const [isLogin, setIsLogin] = useState(true); // simulate login status
    const [open, setOpen] = useState(false);      // mobile drawer state
    const [isMobile, setIsMobile] = useState(false); // mobile flag

    const MOBILE_BREAKPOINT = 768;

    // Check screen width and update isMobile
    useEffect(() => {
        const checkIsMobile = () => {
            setIsMobile(window.innerWidth < MOBILE_BREAKPOINT);
        };

        checkIsMobile(); // on mount
        window.addEventListener("resize", checkIsMobile);
        return () => window.removeEventListener("resize", checkIsMobile);
    }, []);

    // Filter visible items based on login status
    const filteredItems = sidebarItems.filter(
        item => item.requireLogin === undefined || item.requireLogin === isLogin
    );

    // Handle navigation with delayed route push (for animation)
    const handleNav = (href: string) => {
        setOpen(false);
        setTimeout(() => {
            router.push(href);
        }, 300); // match animation duration
    };

    // Sidebar content (shared between desktop and mobile)
    const SidebarContent = () => (
        <div className="grid grid-rows-[70px_1px_1fr] bg-white h-full w-60 shadow-md p-4 z-40 overflow-hidden">
            <div className="flex justify-center items-center">
                <h1 className="text-xl font-bold text-primary font-poppins">FINBOARD</h1>
            </div>
            <div className="w-60 h-[1px] border-1 border-solid border-gray-100 -ml-4 mt-3"/>
            <ul className="flex flex-col gap-2 mt-5">
                {filteredItems.map(({ label, href, icon: Icon }) => {
                    const isActive = pathname === href;
                    return (
                        <li key={href} className="relative group">
                            {/* Left bar for an active link */}
                            {isActive && (
                                <span className="absolute -left-4 top-1/2 -translate-y-1/2 w-[5px] h-[80%] bg-[#4318FF] rounded-r-md" />
                            )}
                            {/* Button instead of Link for smooth closing before navigation */}
                            <button
                                onClick={() => handleNav(href)}
                                className={clsx(
                                    "flex items-center gap-2 px-3 py-2 rounded-md transition duration-150 group w-full text-left outline-none",
                                    isActive
                                        ? "bg-[#F6F8FD] text-primary font-semibold"
                                        : "text-[#A3AED0] hover:bg-gray-100 active:bg-gray-100 active:scale-[0.98]"
                                )}
                            >
                                <Icon
                                    className={clsx(
                                        "w-[22px] h-[22px] transition-colors",
                                        isActive && "text-[#4318FF]"
                                    )}
                                />
                                <span
                                    className={clsx(
                                        "text-[16px] leading-[30px] tracking-[-0.02em] not-italic transition-colors",
                                        isActive
                                            ? "text-primary font-bold"
                                            : "group-hover:text-[#4318FF]"
                                    )}
                                >
                                    {label}
                                </span>
                            </button>
                        </li>
                    );
                })}
            </ul>
        </div>
    );

    return (
        <>
            {/* Burger button (visible only on mobile) */}
            <div className="md:hidden fixed top-4 left-5 z-50">
                <button onClick={() => setOpen(!open)} aria-label="Open sidebar">
                    <BurgerIcon className="w-6 h-6 text-primary" />
                </button>
            </div>

            {/* Static sidebar for desktop */}
            <div className="hidden md:fixed md:inset-y-0 md:left-0 md:w-60 md:block bg-white shadow-md z-40">
                <SidebarContent />
            </div>

            {/* Mobile drawer */}
            <div className="fixed inset-0 z-40 flex md:hidden pointer-events-none">
                {/* Sidebar panel (slide in/out) */}
                <div
                    className={clsx(
                        "w-60 h-full bg-white shadow-xl transform transition-transform duration-300 ease-in-out pointer-events-auto z-40",
                        open ? "translate-x-0" : "-translate-x-full"
                    )}
                >
                    <SidebarContent />
                </div>

                {/* Overlay the background with blur and soft shadow */}
                <div
                    className={clsx(
                        "flex-1 transform transition-transform duration-300 ease-in-out -ml-[80%] z-10",
                        open ? "translate-x-[70%] pointer-events-auto" : "-translate-x-full pointer-events-none"
                    )}
                    style={{
                        background: "linear-gradient(to right, rgba(0,0,0,0.4), transparent)",
                        boxShadow: "inset -40px 0 40px rgba(0,0,0,0.25)",
                        backdropFilter: "blur(2px)"
                    }}
                    onClick={() => setOpen(false)}
                />
            </div>
        </>
    );
};

export default Sidebar;
