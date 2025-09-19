'use client';

/**
 * Select — headless dropdown with custom styling.
 * ------------------------------------------------------------
 * UI: Russian
 * Docs/Comments: English
 */

import React, { useEffect, useRef, useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { ChevronDown } from 'lucide-react';

type Option = { value: string; label: string };

export default function Select({
                                   value,
                                   onChange,
                                   options,
                                   label,
                               }: {
    value: string;
    onChange: (v: string) => void;
    options: Option[];
    label?: string;
}) {
    const [open, setOpen] = useState(false);
    const boxRef = useRef<HTMLDivElement>(null);

    // Close when clicking outside
    useEffect(() => {
        if (!open) return;
        const handler = (e: MouseEvent) => {
            if (boxRef.current && !boxRef.current.contains(e.target as Node)) setOpen(false);
        };
        document.addEventListener('mousedown', handler);
        return () => document.removeEventListener('mousedown', handler);
    }, [open]);

    return (
        <div className="w-full" ref={boxRef}>
            {label && <div className="mb-1 text-xs font-medium text-[#8F9BBA]">{label}</div>}
            <button
                type="button"
                className={[
                    'cursor-pointer group flex w-full items-center justify-between gap-2 rounded-xl border px-3 py-2 text-sm',
                    open ? 'border-[#7144ff]' : 'border-slate-300 bg-slate-50 hover:bg-slate-100',
                ].join(' ')}
                onClick={() => setOpen((v) => !v)}
                aria-haspopup="listbox"
                aria-expanded={open}
                title="Открыть список"
            >
                <span className="truncate">{options.find((o) => o.value === value)?.label ?? '—'}</span>
                <ChevronDown size={16} className={['shrink-0 transition-transform', open && 'rotate-180'].join(' ')} />
            </button>

            <AnimatePresence>
                {open && (
                    <motion.ul
                        initial={{ opacity: 0, y: 6, scale: 0.98 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: 6, scale: 0.98 }}
                        transition={{ duration: 0.12 }}
                        role="listbox"
                        className="absolute z-20 mt-1 w-[min(260px,90vw)] overflow-hidden rounded-xl border border-slate-200 bg-white shadow-xl"
                    >
                        {options.map((o) => (
                            <li
                                key={o.value}
                                role="option"
                                aria-selected={o.value === value}
                                onClick={() => {
                                    onChange(o.value);
                                    setOpen(false);
                                }}
                                className={[
                                    'cursor-pointer px-4 py-2 text-sm transition',
                                    o.value === value ? 'bg-indigo-50 font-medium text-indigo-700' : 'hover:bg-slate-100',
                                ].join(' ')}
                                title={`Выбрать: ${o.label}`}
                            >
                                {o.label}
                            </li>
                        ))}
                    </motion.ul>
                )}
            </AnimatePresence>
        </div>
    );
}
