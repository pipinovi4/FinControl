'use client';

import { useEffect, useRef, useState, useCallback } from 'react';
import { useMutation } from '@tanstack/react-query';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown, Copy, Loader2 } from 'lucide-react';

/* --------------------------------------------------- */
/*  CONFIG                                             */
/* --------------------------------------------------- */

const API = process.env.NEXT_PUBLIC_API_URL ?? "";

/** Ролі, яким можна видати інвайт */
enum Role {
    WORKER = 'WORKER',
    BROKER = 'BROKER',
}
const ROLE_LABEL: Record<Role, string> = {
    [Role.WORKER]: 'Работник',
    [Role.BROKER]: 'Брокер',
};

/** Пресети тривалості */
const PRESETS = [
    { h: 1, label: '1 год' },
    { h: 2, label: '2 год' },
    { h: 6, label: '6 год' },
    { h: 10, label: '10 год' },
    { h: 24, label: '24 год' },
] as const;

/* --------------------------------------------------- */
/*  HELPERS                                            */
/* --------------------------------------------------- */

async function fetchJSON<T>(url: string, init?: RequestInit): Promise<T> {
    const res = await fetch(url, {
        credentials: 'include',
        headers: { 'Content-Type': 'application/json', ...(init?.headers || {}) },
        ...init,
    });

    if (!res.ok) {
        // намагаємося дістати осмислене повідомлення
        const payload = await res.json().catch(() => ({}));
        const detail =
            payload?.detail ??
            (Array.isArray(payload?.errors) ? payload.errors.join(', ') : undefined);

        throw new Error(detail ?? res.statusText);
    }
    return res.json() as Promise<T>;
}

function classNames(...cn: (string | false | null | undefined)[]) {
    return cn.filter(Boolean).join(' ');
}

/* --------------------------------------------------- */
/*  RoleSelect                                         */
/* --------------------------------------------------- */

type RoleSelectProps = {
    value: Role;
    onChange: (r: Role) => void;
    disabled?: boolean;
};

const RoleSelect = ({ value, onChange, disabled }: RoleSelectProps) => {
    const [open, setOpen] = useState(false);
    const boxRef = useRef<HTMLDivElement>(null);

    // click-outside → close
    useEffect(() => {
        if (!open) return;
        const handler = (e: MouseEvent) => {
            if (boxRef.current && !boxRef.current.contains(e.target as Node)) setOpen(false);
        };
        document.addEventListener('mousedown', handler);
        return () => document.removeEventListener('mousedown', handler);
    }, [open]);

    // Esc → close
    useEffect(() => {
        if (!open) return;
        const onKey = (e: KeyboardEvent) => {
            if (e.key === 'Escape') setOpen(false);
        };
        window.addEventListener('keydown', onKey);
        return () => window.removeEventListener('keydown', onKey);
    }, [open]);

    return (
        <div ref={boxRef} className="relative select-none">
            <button
                type="button"
                disabled={disabled}
                onClick={() => setOpen(!open)}
                aria-haspopup="listbox"
                aria-expanded={open}
                className={classNames(
                    'group flex w-full items-center justify-between gap-1 rounded-xl border px-3 py-2 text-sm transition cursor-pointer',
                    open ? 'border-[#7144ff]' : 'border-slate-300',
                    disabled
                        ? 'bg-slate-100 opacity-60'
                        : 'bg-slate-50 hover:bg-slate-100 active:bg-slate-200'
                )}
                title="Вибрати роль"
            >
        <span className="flex items-center gap-2">
          <span
              className={classNames(
                  'inline-block h-2.5 w-2.5 rounded-full',
                  value === Role.WORKER ? 'bg-[#7144ff]' : 'bg-[#4318FF]'
              )}
          />
            {ROLE_LABEL[value]}
        </span>

                <ChevronDown
                    size={16}
                    className={classNames(
                        'transition-transform text-slate-600 group-hover:translate-y-[1px]',
                        open && 'rotate-180'
                    )}
                />
            </button>

            <AnimatePresence>
                {open && !disabled && (
                    <motion.ul
                        initial={{ opacity: 0, y: 4, scale: 0.98 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: 4, scale: 0.98 }}
                        transition={{ duration: 0.12 }}
                        role="listbox"
                        aria-label="Список ролей"
                        className="absolute z-20 mt-1 w-full overflow-hidden rounded-xl border border-slate-200 bg-white shadow-xl backdrop-blur"
                    >
                        {Object.values(Role).map((r) => (
                            <li
                                key={r}
                                role="option"
                                aria-selected={r === value}
                                onClick={() => {
                                    onChange(r);
                                    setOpen(false);
                                }}
                                className={classNames(
                                    'cursor-pointer px-4 py-2 text-sm transition',
                                    r === value
                                        ? 'bg-indigo-50 font-medium text-indigo-700'
                                        : 'hover:bg-slate-100'
                                )}
                            >
                                {ROLE_LABEL[r]}
                            </li>
                        ))}
                    </motion.ul>
                )}
            </AnimatePresence>
        </div>
    );
};

/* --------------------------------------------------- */
/*  InviteGenerator                                    */
/* --------------------------------------------------- */

export default function InviteGenerator() {
    const [role, setRole] = useState<Role>(Role.WORKER);
    const [hours, setHours] = useState<number>(24);
    const [link, setLink] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [copied, setCopied] = useState(false);

    /* -------- mutation -------- */
    const { mutate, isPending } = useMutation({
        mutationFn: ({ role, hours }: { role: Role; hours: number }) => {
            const expires_at = new Date(Date.now() + hours * 3_600_000).toISOString();
            return fetchJSON<{ raw: string }>(`${API}/api/dashboard/admin/create-invite`, {
                method: 'POST',
                body: JSON.stringify({ role, expires_at }),
            });
        },
        onSuccess: ({ raw }) => {
            const url = `${window.location.origin}/auth/register/${raw}`;
            setLink(url);
            setError(null);
        },
        onError: (e: any) => {
            setError(e.message);
            setLink(null);
        },
    });

    const popCopyToast = () => {
        setCopied(true);
        setTimeout(() => setCopied(false), 1800);
    };

    const onSubmit = useCallback(
        (e?: React.FormEvent) => {
            e?.preventDefault();
            mutate({ role, hours });
        },
        [mutate, role, hours]
    );

    // Ctrl/Cmd + Enter → submit
    useEffect(() => {
        const handler = (e: KeyboardEvent) => {
            if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'enter') {
                onSubmit();
            }
        };
        window.addEventListener('keydown', handler);
        return () => window.removeEventListener('keydown', handler);
    }, [onSubmit]);

    /* -------- jsx -------- */
    return (
        <div
            className={classNames(
                // градієнтна рамка контейнера
                'relative p-[1px] rounded-3xl',
                'bg-[conic-gradient(from_180deg_at_50%_50%,#ECE9FF,white,#DDE7FF,#ECE9FF)]'
            )}
        >
            {/* декоративні “світлові плями” */}
            <div className="absolute -top-24 -left-20 h-72 w-72 rounded-full blur-2xl opacity-40 bg-[radial-gradient(circle_at_center,rgba(113,68,255,0.18),rgba(255,255,255,0))]" />
            <div className="absolute -bottom-28 -right-24 h-80 w-80 rounded-full blur-2xl opacity-40 bg-[radial-gradient(circle_at_center,rgba(27,37,89,0.14),rgba(255,255,255,0))]" />

            <div className="relative flex h-full flex-col rounded-[calc(theme(borderRadius.3xl)-1px)] bg-white/90 p-6 shadow-xl overflow-hidden min-h-[420px] sm:min-h-[440px] lg:min-h-[460px] backdrop-blur border border-transparent hover:border-[#E5E9F6]">
                <div className="flex flex-col justify-between gap-2">
                    <h2 className="text-lg font-extrabold text-[#2B3674] tracking-tight">
                        Генерация&nbsp;инвайта
                    </h2>

                    {/* міні-бейдж статусу */}
                    <motion.div
                        initial={false}
                        animate={{ opacity: isPending ? 1 : 0.6, scale: isPending ? 1.02 : 1 }}
                        className={classNames(
                            'inline-block w-fit self-start rounded-full px-3 py-1 text-[11px] font-medium',
                            isPending ? 'bg-[#ECE9FF] text-[#7144ff]' : 'bg-slate-100 text-slate-600'
                        )}
                    >
                        {isPending ? 'Генерация...' : 'Ожидание'}
                    </motion.div>
                </div>

                <form onSubmit={(e) => onSubmit(e)} className="mt-5 flex flex-1 flex-col gap-6">
                    {/* select role */}
                    <div className="flex flex-col gap-1 text-sm">
                        <span className="font-medium text-[#8F9BBA]">Роль</span>
                        <RoleSelect value={role} onChange={(r) => { setRole(r); setLink(null); }} disabled={isPending} />
                    </div>

                    {/* presets */}
                    <div className="flex flex-col gap-1 text-sm">
                        <span className="font-medium text-[#8F9BBA]">Действительна</span>
                        <div className="grid grid-cols-5 gap-2">
                            {PRESETS.map((p) => {
                                const active = hours === p.h;
                                return (
                                    <button
                                        key={p.h}
                                        type="button"
                                        disabled={isPending}
                                        onClick={() => {
                                            setHours(p.h);
                                            if (link) setLink(null); // зміна тривалості → ховаємо попередню лінку
                                        }}
                                        className={classNames(
                                            'cursor-pointer rounded-lg border px-2.5 py-1 text-[13px] transition outline-none focus-visible:ring-2 focus-visible:ring-[#7144ff]/30',
                                            active
                                                ? 'border-transparent bg-[#ECE9FF] font-semibold text-[#7144ff] shadow-inner'
                                                : 'border-slate-300 bg-slate-50 hover:bg-slate-100 active:bg-slate-200'
                                        )}
                                        aria-pressed={active}
                                        title={`Зробити інвайт на ${p.label}`}
                                    >
                                        {p.label}
                                    </button>
                                );
                            })}
                        </div>
                    </div>

                    {/* error / link blocks */}
                    <div className="min-h-[28px]">
                        <AnimatePresence>
                            {error && (
                                <motion.div
                                    key="err"
                                    initial={{ opacity: 0, y: -6 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    exit={{ opacity: 0, y: -6 }}
                                    className="mt-2 rounded-md border border-red-300 bg-red-50 px-3 py-2 text-xs text-red-700"
                                    role="alert"
                                    aria-live="assertive"
                                >
                                    {error}
                                </motion.div>
                            )}
                        </AnimatePresence>

                        <AnimatePresence>
                            {link && (
                                <motion.div
                                    key="link"
                                    initial={{ opacity: 0, y: -6 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    exit={{ opacity: 0, y: -6 }}
                                    className="flex items-start gap-2 rounded-md border border-emerald-300 bg-emerald-50 px-3 py-2 text-[11px] leading-5 text-emerald-800"
                                    role="status"
                                    aria-live="polite"
                                >
                                    <span className="break-all font-mono">{link}</span>
                                    <button
                                        type="button"
                                        onClick={() =>
                                            navigator.clipboard.writeText(link).then(popCopyToast).catch(() => null)
                                        }
                                        className="shrink-0 p-1 text-emerald-700 hover:text-emerald-900 cursor-pointer rounded hover:bg-white/50"
                                        title="Скопировать"
                                        aria-label="Скопировать ссылку приглашения"
                                    >
                                        <Copy size={14} />
                                    </button>
                                </motion.div>
                            )}
                        </AnimatePresence>
                    </div>

                    {/* submit */}
                    <motion.button
                        type="submit"
                        disabled={isPending}
                        whileTap={{ scale: isPending ? 1 : 0.98 }}
                        className={classNames(
                            'mt-auto inline-flex w-full items-center justify-center gap-2 rounded-xl bg-[#7144ff] py-3 text-sm font-semibold text-white transition',
                            'hover:brightness-110 disabled:opacity-60 cursor-pointer',
                            'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#7144ff]/40'
                        )}
                        title="Сгенерировать ссылку (Ctrl/Cmd+Enter)"
                    >
                        {isPending && <Loader2 size={16} className="animate-spin" />}
                        {isPending ? 'Генерируем…' : 'Сгенерировать ссылку'}
                    </motion.button>
                </form>

                {/* копі-тост */}
                <AnimatePresence>
                    {copied && (
                        <motion.div
                            key="copied"
                            initial={{ opacity: 0, y: -8 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -8 }}
                            transition={{ duration: 0.18 }}
                            className="fixed top-4 right-4 z-[120] rounded-md bg-[#4318FF] px-4 py-2 text-xs font-medium text-white shadow-lg"
                            role="status"
                            aria-live="polite"
                        >
                            Ссылка скопирована в буфер
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </div>
    );
}
