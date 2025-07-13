'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';

/* ---------- Wrapper ---------- */
export const Popover: React.FC<
    React.PropsWithChildren<{ open?: boolean; onOpenChange?: (o: boolean) => void }>
> = ({ open, onOpenChange, children }) => (
    <div
        className="relative inline-flex w-full"
        data-open={open}
        onClick={() => onOpenChange?.(!open)}
    >
        {children}
    </div>
);

/* ---------- Trigger ---------- */
interface TriggerProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    asChild?: boolean; // підтримуємо API shadcn
}
export const PopoverTrigger = React.forwardRef<HTMLButtonElement, TriggerProps>(
    ({ className, children, ...props }, ref) => (
        <button ref={ref} className={cn('z-10 w-full', className)} {...props}>
            {children}
        </button>
    )
);
PopoverTrigger.displayName = 'PopoverTrigger';

/* ---------- Content ---------- */
interface ContentProps extends React.HTMLAttributes<HTMLDivElement> {
    align?: 'start' | 'center' | 'end';
}
export const PopoverContent = React.forwardRef<HTMLDivElement, ContentProps>(
    ({ className, align = 'center', children, ...props }, ref) => {
        const pos =
            align === 'start'
                ? 'left-0'
                : align === 'end'
                    ? 'right-0'
                    : 'left-1/2 -translate-x-1/2';

        return (
            <div
                ref={ref}
                className={cn(
                    'absolute top-full mt-2 rounded-xl border bg-white p-3 shadow-lg z-50',
                    pos,
                    className
                )}
                {...props}
            >
                {children}
            </div>
        );
    }
);
PopoverContent.displayName = 'PopoverContent';
