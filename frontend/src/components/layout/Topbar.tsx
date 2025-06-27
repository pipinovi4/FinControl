'use client';

import { BellIcon, MoonIcon, LoopIcon } from '@/components/icons';
import clsx from 'clsx';
import Image from 'next/image';

const Topbar = () => (
    <div
        className={clsx(
            'fixed top-0 right-0 z-50 border border-gray-100 rounded-full bg-[#F8FAFF] shadow-sm',
            /* Width per breakpoint */
            'w-full md:w-[340px] lg:w-[380px] xl:w-[420px] 2xl:w-[460px]',
            /* Layout */
            'flex items-center justify-end gap-4',
            /* Height / y-padding */
            'py-2 md:py-[10px] lg:py-3 xl:py-3.5 2xl:py-4',
            'px-2 md:px-4'
        )}
    >
        {/* Search */}
        <div
            className={clsx(
                'flex items-center gap-2 bg-[#F1F4FA] rounded-full',
                /* slower, softer expansion */
                'transition-all duration-500 ease-[cubic-bezier(.25,.8,.4,1)]',
                'w-10 md:flex-1 md:px-3 md:py-2 lg:px-4 lg:py-2.5 xl:px-5 xl:py-3'
            )}
        >
            {/* Icons a bit bigger on mobile, smaller on xl+ */}
            <LoopIcon className="w-6 h-6 md:w-5 md:h-5 xl:w-5 xl:h-5 2xl:w-4.5 2xl:h-4.5 text-[#2B3674]" />

            <input
                type="text"
                placeholder="Поиск"
                className={clsx(
                    'hidden md:block w-full bg-transparent outline-none',
                    'font-dmSans text-[14px] lg:text-[15px] xl:text-[15px] 2xl:text-[15px]',
                    'text-[#8F9BBA] placeholder-[#9CA3AF]'
                )}
            />
        </div>

        {/* Action icons – larger first, taper on large screens */}
        {[BellIcon, MoonIcon].map((Icon, i) => (
            <button key={i} className="hover:scale-105 transition-transform duration-300">
                <Icon className="w-6 h-6 md:w-5 md:h-5 xl:w-5 xl:h-5 2xl:w-4.5 2xl:h-4.5 text-[#A3AED0]" />
            </button>
        ))}

        {/* Avatar – shrink a hair on huge screens */}
        <div className="w-9 h-9 md:w-8 md:h-8 xl:w-8 xl:h-8 2xl:w-7.5 2xl:h-7.5 rounded-full overflow-hidden border-2 border-white shadow-md">
            <Image
                src="/avatar.jpg"
                alt="User avatar"
                width={44}
                height={44}
                className="object-cover w-full h-full"
            />
        </div>
    </div>
);

export default Topbar;
