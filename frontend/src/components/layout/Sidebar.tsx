'use client';

import {useState, useEffect, useMemo, JSX} from 'react';
import {
    AnalyzeIcon,
    HouseIcon,
    LockIcon,
    LogInIcon,
    BurgerIcon,
} from '@/components/icons';
import clsx from 'clsx';
import { usePathname, useRouter } from 'next/navigation';
import UserStorage from '@/services/UserStorage';

/* -------------------------------------------------- */
/* меню в одному місці – легше додавати властивості   */
/* -------------------------------------------------- */
type SidebarItem = {
    label: string;
    href: string;
    icon: (props: React.SVGProps<SVGSVGElement>) => JSX.Element;
    /** коли true – показуємо ТІЛЬКИ авторизованому */
    requireLogin?: boolean;
    /** коли true – показуємо ТІЛЬКИ неавторизованому */
    guestOnly?: boolean;
    /** яким ролям **ховаємо** пункт */
    hideForRoles?: string[];
};

const SIDEBAR_ITEMS: SidebarItem[] = [
    { label: 'Панель управления', href: '/dashboard', icon: HouseIcon },
    {
        label: 'Аналитика',
        href: '/analyze',
        icon: AnalyzeIcon,
        /* ⛔ ховаємо для worker */
        hideForRoles: ['worker'],
    },
    {
        label: 'Авторизация',
        href: '/auth/register',
        icon: LogInIcon,
        guestOnly: true,
    },
    {
        label: 'Выход',
        href: '/logout',
        icon: LockIcon,
        requireLogin: true,
    },
];

/* -------------------------------------------------- */

const MOBILE_BREAKPOINT = 768;

const Sidebar = () => {
    const pathname = usePathname();
    const router = useRouter();

    /* -------------------------------- auth / role ------------------------------- */
    const storedUser = useMemo(() => UserStorage.get(), []);
    const isLogin = Boolean(storedUser);
    const role = storedUser?.role.toLowerCase() ?? null; // 'admin' | 'broker' | 'worker' | null

    /* -------------------------------- responsive -------------------------------- */
    const [open, setOpen] = useState(false);
    const [isMobile, setIsMobile] = useState(false);

    /* detect mobile */
    useEffect(() => {
        const check = () => setIsMobile(window.innerWidth < MOBILE_BREAKPOINT);
        check();
        window.addEventListener('resize', check);
        return () => window.removeEventListener('resize', check);
    }, []);

    /* ---------------------------- фільтрація меню ------------------------------- */
    const visibleItems = useMemo(
        () =>
            SIDEBAR_ITEMS.filter(item => {
                /* умови авторизації */
                if (item.requireLogin && !isLogin) return false;
                if (item.guestOnly && isLogin) return false;
                /* умови ролей */
                if (item.hideForRoles?.includes(role as string)) return false;
                return true;
            }),
        [isLogin, role]
    );

    /* ------------------------------- navigation --------------------------------- */
    const handleNav = (href: string) => {
        setOpen(false);
        /* даємо 300 мс, щоби drawer встиг зачинитись */
        setTimeout(() => router.push(href), 300);
    };

    /* ------------------------------ render item --------------------------------- */
    const renderItems = () =>
        visibleItems.map(({ label, href, icon: Icon }) => {
            const isActive = pathname === href;
            return (
                <li key={href} className="relative group">
                    {isActive && (
                        <span className="absolute -left-4 top-1/2 -translate-y-1/2 w-[5px] h-[80%] bg-[#4318FF] rounded-r-md" />
                    )}

                    <button
                        onClick={() => handleNav(href)}
                        className={clsx(
                            'flex items-center gap-3 px-2 py-2 rounded-md transition duration-150 w-full text-left outline-none cursor-pointer',
                            isActive
                                ? 'bg-[#F6F8FD] text-primary font-semibold'
                                : 'text-[#A3AED0] hover:bg-gray-100 active:bg-gray-100 active:scale-[0.98]'
                        )}
                    >
                        <Icon
                            className={clsx(
                                'w-[22px] h-[22px] transition-colors',
                                isActive && 'text-[#4318FF]'
                            )}
                        />
                        <span
                            className={clsx(
                                'text-[16px] leading-[30px] tracking-[-0.02em] transition-colors',
                                isActive ? 'text-primary font-bold' : 'group-hover:text-[#4318FF]'
                            )}
                        >
              {label}
            </span>
                    </button>
                </li>
            );
        });

    /* ------------------------------ sidebar core -------------------------------- */
    const SidebarContent = () => (
        <div className="grid grid-rows-[70px_1px_1fr] bg-white h-full w-60 shadow-md p-4 z-40 overflow-hidden">
            <div className="flex justify-center items-center">
                <h1 className="text-xl font-bold text-primary font-poppins">FINBOARD</h1>
            </div>
            <div className="w-60 h-[1px] border border-gray-100 -ml-4 mt-3" />
            <ul className="flex flex-col gap-2 mt-5">{renderItems()}</ul>
        </div>
    );

    /* -------------------------------- template ---------------------------------- */
    return (
        <>
            {/* burger – mobile only */}
            {isMobile && (
                <button
                    onClick={() => setOpen(!open)}
                    aria-label="Open sidebar"
                    className="fixed top-4 left-5 z-50 md:hidden"
                >
                    <BurgerIcon className="w-6 h-6 text-primary" />
                </button>
            )}

            {/* desktop sidebar */}
            <div className="hidden md:fixed md:inset-y-0 md:left-0 md:w-60 md:block bg-white shadow-md z-40">
                <SidebarContent />
            </div>

            {/* mobile drawer */}
            <div className="fixed inset-0 z-40 flex md:hidden pointer-events-none">
                {/* panel */}
                <div
                    className={clsx(
                        'w-60 h-full bg-white shadow-xl transform transition-transform duration-300 ease-in-out pointer-events-auto z-40',
                        open ? 'translate-x-0' : '-translate-x-full'
                    )}
                >
                    <SidebarContent />
                </div>

                {/* overlay */}
                <div
                    className={clsx(
                        'flex-1 transform transition-transform duration-300 ease-in-out -ml-[80%] z-10 cursor-pointer',
                        open
                            ? 'translate-x-[70%] pointer-events-auto'
                            : '-translate-x-full pointer-events-none'
                    )}
                    style={{
                        background: 'linear-gradient(to right, rgba(0,0,0,0.4), transparent)',
                        boxShadow: 'inset -40px 0 40px rgba(0,0,0,0.25)',
                        backdropFilter: 'blur(2px)',
                    }}
                    onClick={() => setOpen(false)}
                />
            </div>
        </>
    );
};

export default Sidebar;
