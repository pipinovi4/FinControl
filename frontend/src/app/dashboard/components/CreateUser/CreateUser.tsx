// =============================================
// File: parts/CreateUser/CreateUser.tsx
// =============================================
'use client';

import { useEffect, useRef, useState } from 'react';
import { UserPlus, ChevronDown } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import FullscreenModal from '@/components/ui/FullScreenModal';
import RegistrationCard, { RegistrationField } from './parts/RegistrationCard';

// ---------- helpers ----------
const cx2 = (...c: (string | false | null | undefined)[]) => c.filter(Boolean).join(' ');

// ---------- roles ----------
const ROLES = ['WORKER', 'BROKER', 'CLIENT', 'ADMIN'] as const;
export type Role = (typeof ROLES)[number];
const ROLE_LABEL: Record<Role, string> = {
    ADMIN: 'Админ',
    WORKER: 'Работник',
    BROKER: 'Брокер',
    CLIENT: 'Клиент',
};

// simple POST helper
async function postJson(url: string, body: unknown) {
    const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(body),
    });
    if (!res.ok) {
        let msg = `HTTP ${res.status}`;
        try {
            msg = (await res.json())?.detail ?? msg;
        } catch {}
        throw new Error(msg);
    }
}

/* ---------- Role Select (inline) ---------- */
function RoleSelect({ value, onChange, disabled }: { value: Role; onChange: (r: Role) => void; disabled?: boolean }) {
    const [open, setOpen] = useState(false);
    const ref = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (!open) return;
        const handler = (e: MouseEvent) => {
            if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
        };
        document.addEventListener('mousedown', handler);
        return () => document.removeEventListener('mousedown', handler);
    }, [open]);

    useEffect(() => {
        if (!open) return;
        const onKey = (e: KeyboardEvent) => e.key === 'Escape' && setOpen(false);
        window.addEventListener('keydown', onKey);
        return () => window.removeEventListener('keydown', onKey);
    }, [open]);

    return (
        <div ref={ref} className="relative select-none">
            <button
                type="button"
                disabled={disabled}
                onClick={() => setOpen((v) => !v)}
                aria-haspopup="listbox"
                aria-expanded={open}
                className={cx2(
                    'cursor-pointer group flex w-full items-center justify-between gap-1 rounded-xl border px-3 py-2 text-sm transition',
                    open ? 'border-[#7144ff]' : 'border-slate-300',
                    disabled ? 'bg-slate-100 opacity-60' : 'bg-slate-50 hover:bg-slate-100 active:bg-slate-200'
                )}
            >
        <span className="flex items-center gap-2">
          <span className={cx2('inline-block h-2.5 w-2.5 rounded-full', value === 'WORKER' ? 'bg-[#7144ff]' : 'bg-[#4318FF]')} />
            {ROLE_LABEL[value]}
        </span>
                <ChevronDown size={16} className={cx2('text-slate-600 transition-transform', open && 'rotate-180')} />
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
                        className="absolute z-20 mt-1 w-full overflow-hidden rounded-xl border border-slate-200 bg-white shadow-xl"
                    >
                        {ROLES.map((r) => (
                            <li
                                key={r}
                                role="option"
                                aria-selected={r === value}
                                onClick={() => {
                                    onChange(r);
                                    setOpen(false);
                                }}
                                className={cx2(
                                    'cursor-pointer px-4 py-2 text-sm transition',
                                    r === value ? 'bg-indigo-50 font-medium text-indigo-700' : 'hover:bg-slate-100'
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
}

/* ---------- Main CreateUser component ---------- */
export interface CreateUserProps {
    defaultRole?: Role;
    fieldsList?: RegistrationField[][]; // [worker, broker, client, admin]
    registrationUrls?: string[]; // same order as above
    onSubmit?: (p: { url: string; role: Role; values: Record<string, unknown> }) => Promise<void> | void;
}

const EMPTY_F: RegistrationField[][] = [[], [], [], []];
const EMPTY_U = ['/worker', '/broker', '/client', '/admin'];

export default function CreateUser({ defaultRole = 'WORKER', fieldsList, registrationUrls, onSubmit }: CreateUserProps) {
    const [step, setStep] = useState<'pick' | 'form'>('pick');
    const [role, setRole] = useState<Role>(defaultRole);
    const [error, setError] = useState<string | null>(null);

    const FIELDS = fieldsList?.length === 4 ? fieldsList : EMPTY_F;
    const URLS = registrationUrls?.length === 4 ? registrationUrls : EMPTY_U;

    const activeFields = FIELDS[ROLES.indexOf(role)];
    const activeUrl = URLS[ROLES.indexOf(role)];

    const handleSubmit = async (raw: Record<string, unknown>) => {
        setError(null);

        const values = activeFields.reduce<Record<string, unknown>>((acc, f) => {
            const v0 = (raw as any)[f.name];
            if (v0 === undefined || v0 === '') return acc;
            let v: unknown = v0;
            if (f.type === 'array') v = String(v0).split(',').map((s) => s.trim()).filter(Boolean);
            else if (f.type === 'int') {
                const n = Number(v0);
                if (!Number.isNaN(n)) v = n;
            }
            acc[f.name] = v;
            return acc;
        }, {});

        try {
            if (onSubmit) await onSubmit({ url: activeUrl, role, values });
            else await postJson(activeUrl, values);
        } catch (e) {
            setError((e as Error).message);
            throw e; // щоб RegistrationCard показав помилку
        }
    };

    return (
        <section
        >
            {/* decorative glows */}
            <div className="pointer-events-none absolute -top-24 -left-20 h-72 w-72 rounded-full blur-2xl opacity-40 bg-[radial-gradient(circle_at_center,rgba(113,68,255,0.18),rgba(255,255,255,0))]" />
            <div className="pointer-events-none absolute -bottom-28 -right-24 h-80 w-80 rounded-full blur-2xl opacity-40 bg-[radial-gradient(circle_at_center,rgba(27,37,89,0.14),rgba(255,255,255,0))]" />

            <div className="relative flex min-h-[420px] sm:min-h-[440px] lg:min-h-[460px] flex-col rounded-[calc(theme(borderRadius.3xl)-1px)] bg-white/90 p-6 shadow-xl backdrop-blur border border-transparent hover:border-[#E5E9F6] overflow-hidden">
                {/* Header */}
                <header className="flex flex-col justify-between gap-2">
                    <h2 className="text-lg font-extrabold text-[#2B3674] tracking-tight">Создать пользователя</h2>
                    <motion.span
                        initial={false}
                        animate={{ opacity: step === 'form' ? 1 : 0.65 }}
                        className="inline-block w-fit self-start rounded-full px-3 py-1 text-[11px] font-medium bg-slate-100 text-slate-600"
                    >
                        {step === 'form' ? 'Заполнение формы' : 'Выбор роли'}
                    </motion.span>
                </header>

                {/* Content */}
                <div className="mt-4 flex flex-1 flex-col gap-6 md:max-w-md md:self-center w-full">
                    {/* Icon */}
                    <div className="flex items-center justify-center pt-2">
                        <UserPlus className="h-14 w-14 text-primary" />
                    </div>

                    {/* Role on top */}
                    <div className="flex flex-col gap-1 text-sm">
                        <span className="font-medium text-[#8F9BBA]">Роль</span>
                        <RoleSelect value={role} onChange={setRole} />
                    </div>

                    {/* CTA at the bottom */}
                    {step === 'pick' && (
                        <button
                            type="button"
                            onClick={() => setStep('form')}
                            className="mt-auto cursor-pointer w-full rounded-xl bg-[#7144ff] py-3 text-sm font-semibold text-white hover:brightness-110 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#7144ff]/40"
                        >
                            Перейти до создания {ROLE_LABEL[role]}
                        </button>
                    )}
                </div>

                {/* Modal */}
                <FullscreenModal modalOpen={step === 'form'} toggleModal={() => setStep('pick')}>
                    <RegistrationCard
                        title={`Новый ${ROLE_LABEL[role]}`}
                        fields={activeFields}
                        onClose={() => setStep('pick')}
                        onSubmit={handleSubmit}
                        error={error}
                    />
                </FullscreenModal>
            </div>
        </section>
    );
}
