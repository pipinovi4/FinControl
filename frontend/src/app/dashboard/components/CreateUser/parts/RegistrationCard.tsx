// =============================================
// File: parts/CreateUser/RegistrationCard.tsx
// Polished, responsive, a11y-friendly version
// =============================================
/* eslint-disable react/no-unescaped-entities */
'use client';

import { useEffect, useMemo, useState, useId, FormEvent } from 'react';
import { Loader2, CheckCircle2, AlertTriangle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

// ---------- helpers ----------
const cx = (...c: (string | false | null | undefined)[]) => c.filter(Boolean).join(' ');

// ---------- types ----------
export type FieldType = 'text' | 'email' | 'password' | 'array' | 'int' | 'select';
export interface RegistrationField {
    name: string;
    label: string;
    type?: FieldType;
    options?: string[]; // for select
    placeholder?: string;
    optional?: boolean;
}

export interface RegistrationCardProps {
    title: string;
    fields: RegistrationField[];
    onClose?: () => void;
    onSubmit?: (vals: Record<string, any>) => Promise<void>;
    error?: string | null;
    /**
     * When true, the header + footer stay visible while the fields scroll.
     * Recommended when the form has many inputs.
     */
    stickyChrome?: boolean;
}

export default function RegistrationCard({ title, fields, onClose, onSubmit, error, stickyChrome = true }: RegistrationCardProps) {
    // Build initial shape once per fields set
    const initial = useMemo(
        () => Object.fromEntries(fields.map((f) => [f.name, ''])) as Record<string, string>,
        [fields]
    );

    const [vals, setVals] = useState(initial);
    const [busy, setBusy] = useState(false);
    const [done, setDone] = useState(false);

    // if a new error arrives — clear success banner
    useEffect(() => {
        if (error && done) setDone(false);
    }, [error, done]);

    // when the fields list changes — reset the form
    useEffect(() => {
        setVals(initial);
    }, [initial]);

    const change = (k: string, v: string) => setVals((p) => ({ ...p, [k]: v }));

    const handle = async (e: FormEvent) => {
        e.preventDefault();
        if (!onSubmit) return;
        setBusy(true);
        setDone(false);
        try {
            await onSubmit(vals);
            setVals(initial);
            setDone(true);
        } finally {
            setBusy(false);
        }
    };

    // Ctrl/Cmd + Enter → submit
    useEffect(() => {
        const hk = (e: KeyboardEvent) => {
            if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'enter') {
                (document.getElementById('reg-submit-btn') as HTMLButtonElement | null)?.click();
            }
        };
        window.addEventListener('keydown', hk);
        return () => window.removeEventListener('keydown', hk);
    }, []);

    // Stable IDs for inputs to link <label htmlFor>
    const formUid = useId();
    const idFor = (name: string) => `${formUid}-${name}`;

    return (
        <form
            onSubmit={handle}
            className={cx(
                'relative w-full max-w-4xl rounded-3xl border border-slate-200/80 bg-white/95 shadow-2xl backdrop-blur',
                'p-4 sm:p-6 md:p-8'
            )}
            aria-labelledby={`${formUid}-title`}
        >
            {/* close */}
            {onClose && (
                <button
                    type="button"
                    onClick={onClose}
                    disabled={busy}
                    className="cursor-pointer absolute top-3 right-3 rounded-full p-1 text-slate-500 hover:bg-slate-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-[#7144ff] disabled:opacity-50"
                    aria-label="Закрити"
                >
                    <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true">
                        <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                    </svg>
                </button>
            )}

            {/* header */}
            <div className={cx(stickyChrome && 'sticky top-0 z-10 -mx-4 sm:-mx-6 md:-mx-8 px-4 sm:px-6 md:px-8 pt-1 pb-3 bg-white/95 backdrop-blur')}>
                <h2 id={`${formUid}-title`} className="text-center text-2xl sm:text-3xl font-extrabold tracking-tight text-[#2B3674]">
                    {title}
                </h2>
            </div>

            {/* fields */}
            <div className={cx('mt-4', stickyChrome && 'max-h-[60vh] overflow-y-auto overscroll-contain pr-1 sm:pr-2', 'custom-scrollbars')}
                 aria-live="off"
            >
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 sm:gap-5">
                    {fields.map((f, idx) => {
                        const required = !f.optional;
                        const common = {
                            id: idFor(f.name),
                            name: f.name,
                            placeholder: f.placeholder,
                            value: vals[f.name] ?? '',
                            onChange: (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) =>
                                change(f.name, e.target.value),
                            required,
                        } as const;

                        return (
                            <div key={f.name} className="flex flex-col gap-1">
                                <label htmlFor={idFor(f.name)} className="flex items-center gap-1 text-sm font-medium text-[#8F9BBA]">
                                    <span>{f.label}</span>
                                    {!required && <span className="ml-0.5 rounded bg-slate-100 px-1 py-0.5 text-[10px] leading-none text-slate-500">optional</span>}
                                </label>

                                {f.type === 'array' ? (
                                    <textarea
                                        {...common}
                                        rows={3}
                                        className="min-h-[2.75rem] resize-y rounded-xl border border-slate-300 bg-slate-50 px-3 py-2 text-sm focus:border-[#7144ff] focus:outline-none"
                                    />
                                ) : f.type === 'select' && f.options ? (
                                    <select
                                        {...common}
                                        className="min-h-[2.75rem] cursor-pointer rounded-xl border border-slate-300 bg-slate-50 px-3 py-2 text-sm focus:border-[#7144ff] focus:outline-none"
                                    >
                                        <option value="" disabled>
                                            {f.placeholder ?? 'Выберите вариант'}
                                        </option>
                                        {f.options.map((opt) => (
                                            <option key={opt} value={opt}>
                                                {opt}
                                            </option>
                                        ))}
                                    </select>
                                ) : (
                                    <input
                                        {...common}
                                        autoComplete={f.type === 'password' ? 'new-password' : 'off'}
                                        inputMode={f.type === 'int' ? 'numeric' : undefined}
                                        pattern={f.type === 'int' ? "\\d*" : undefined}
                                        type={f.type === 'int' ? 'number' : f.type ?? 'text'}
                                        className="h-11 rounded-xl border border-slate-300 bg-slate-50 px-3 py-2 text-sm focus:border-[#7144ff] focus:outline-none"
                                        {...(idx === 0 ? { autoFocus: true } : {})}
                                    />
                                )}
                            </div>
                        );
                    })}
                </div>
            </div>

            {/* banners */}
            <div className="mt-4 min-h-[40px]" aria-live="polite" aria-atomic="true">
                <AnimatePresence>
                    {error && (
                        <motion.p
                            key="err"
                            initial={{ opacity: 0, y: -6 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -6 }}
                            className="flex items-center justify-center gap-2 rounded-xl border border-red-300 bg-red-50 px-4 py-2 text-sm text-red-700"
                            role="alert"
                        >
                            <AlertTriangle size={16} aria-hidden="true" /> {error}
                        </motion.p>
                    )}
                </AnimatePresence>
                <AnimatePresence>
                    {done && !error && (
                        <motion.p
                            key="ok"
                            initial={{ opacity: 0, y: -6 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -6 }}
                            className="flex items-center justify-center gap-2 rounded-xl border border-emerald-300 bg-emerald-50 px-4 py-2 text-sm text-emerald-700"
                            role="status"
                        >
                            <CheckCircle2 size={16} aria-hidden="true" /> Юзер успешно создан!
                        </motion.p>
                    )}
                </AnimatePresence>
            </div>

            {/* footer */}
            <div className={cx('mt-6', stickyChrome && 'sticky bottom-0 -mx-4 sm:-mx-6 md:-mx-8 px-4 sm:px-6 md:px-8 pt-3 pb-2 bg-white/95 backdrop-blur')}>
                <button
                    id="reg-submit-btn"
                    type="submit"
                    disabled={busy}
                    className={cx(
                        'cursor-pointer flex w-full items-center justify-center gap-2 rounded-xl py-3 text-base font-semibold text-white transition',
                        'bg-gradient-to-r from-[#7144ff] to-[#47338E] hover:brightness-110 disabled:opacity-60'
                    )}
                >
                    {busy && <Loader2 size={18} className="animate-spin" aria-hidden="true" />}
                    Создать пользователя
                </button>
            </div>

            {/* local styles for subtle custom scrollbars (Tailwind-safe) */}
            <style jsx>{`
        .custom-scrollbars::-webkit-scrollbar { height: 10px; width: 10px; }
        .custom-scrollbars::-webkit-scrollbar-thumb { background: rgba(148,163,184,.6); border-radius: 9999px; }
        .custom-scrollbars::-webkit-scrollbar-track { background: transparent; }
      `}</style>
        </form>
    );
}
