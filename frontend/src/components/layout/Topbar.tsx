'use client';

import { BellIcon, MoonIcon, LoopIcon, UserIcon } from '@/components/icons';
import { useProfileModal } from '@/components/profile/useProfileModal';
import clsx from 'clsx';

const Topbar = () => {
    const { open } = useProfileModal();

    return (
        <div
            className={clsx(
                'absolute top-0 right-0 z-50 border border-gray-100 rounded-full bg-[#F8FAFF] shadow-sm',

                // ширина
                // 'w-full md:w-[340px] lg:w-[380px] xl:w-[420px] 2xl:w-[460px]',

                // 'w-full md:w-[340px] lg:w-[380px] xl:w-[420px] 2xl:w-[460px]',
                // flex-layout
                'flex items-center justify-end gap-4',

                // компактніший vertical padding
                'py-1 md:py-2 lg:py-2 xl:py-2 2xl:py-2',
                'px-2 md:px-3'
            )}
        >

            {/*{[BellIcon, MoonIcon].map((Icon, i) => (*/}
            {/*    <button*/}
            {/*        key={i}*/}
            {/*        className="hover:scale-105 transition-transform duration-300 cursor-pointer"*/}
            {/*    >*/}
            {/*        <Icon className="w-5 h-5 text-[#A3AED0]" />*/}
            {/*    </button>*/}
            {/*))}*/}

            {/* зменшений аватар */}
            <button
                onClick={open}
                className="w-8 h-8 rounded-full overflow-hidden border-2 border-white shadow-md flex items-center justify-center hover:scale-105 transition-transform cursor-pointer"
            >
                <UserIcon className="w-6 h-6 text-[#4B22F4]" />
            </button>
        </div>
    )
};

export default Topbar;
