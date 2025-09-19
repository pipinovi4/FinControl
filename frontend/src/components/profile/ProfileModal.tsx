// src/parts/profile/ProfileModal.tsx
'use client';

import { useEffect, useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { Pencil, Check, X } from 'lucide-react';
import { useProfileModal } from './useProfileModal';
import { roleBasedCrudService } from '@/services/crudService';

/* ──────────────────────────── 1. Константи ──────────────────────────── */

type Role    = 'admin' | 'worker' | 'broker';
type UserRec = Record<string, any>;

/** глобально приховані — взагалі не рендеримо */
const HIDDEN_GLOBAL = [
    'password', 'accessToken', 'refreshToken', 'deleted',
    'created_at', 'updated_at', 'deleted_at', 'id'
];

/** які поля показувати / редагувати в залежності від ролі */
const VIEWABLE_FIELDS:  Record<Role, string[]> = {
    admin : ['email', 'display_name'],
    worker: ['email', 'username'],
    broker: ['email', 'company_name', 'region'],
};

const EDITABLE_FIELDS: Record<Role, string[]> = {
    admin : ['display_name'],
    worker: ['username'],
    broker: ['company_name', 'region'],
};

/** RU-label’и — дописуй свої при потребі */
const FIELD_LABELS: Record<string, string> = {
    email          : 'Почта',
    username       : 'Логин',
    display_name   : 'Логин',
    company_name   : 'Компания',
    region         : 'Регион',
};

/** prettify: snake_case → «Snake case» (якщо немає власного label) */
const prettify = (k: string) =>
    FIELD_LABELS[k] ?? k.replace(/_/g, ' ').replace(/^\w/, c => c.toUpperCase());

/* ──────────────────────────── 2. Компонент ──────────────────────────── */

export default function ProfileModal() {
    /* modal state */
    const { isOpen, close }       = useProfileModal();
    const [user, setUser]         = useState<UserRec>({});
    const [editing, setEditing]   = useState<string | null>(null);
    const [temp, setTemp]         = useState('');

    /* роль витягуємо одразу ( може бути null ) */
    const role: Role | null = (() => {
        try { return JSON.parse(localStorage.getItem('user') ?? '{}').role?.toLowerCase(); }
        catch { return null; }
    })();

    /* завантажуємо user при відкритті */
    useEffect(() => {
        if (!isOpen) { setEditing(null); return; }
        try  { setUser(JSON.parse(localStorage.getItem('user') ?? '{}')); }
        catch{ setUser({}); }
    }, [isOpen]);

    /* ─── helper’и редагування ─── */
    const beginEdit = (k: string) => {
        if (!role || !EDITABLE_FIELDS[role].includes(k)) return; // read-only
        setEditing(k);
        setTemp(String(user[k] ?? ''));
    };
    const cancelEdit = () => setEditing(null);

    const saveEdit = async () => {
        if (!editing || !user.id) return;

        const valueToSend =
            editing === 'region'
                ? temp.split(',').map(s => s.trim()).filter(Boolean)
                : temp;

        const updated = { ...user, [editing]: valueToSend };
        setUser(updated);
        localStorage.setItem('user', JSON.stringify(updated));

        try {
            await roleBasedCrudService.update(user.id, {
                [editing]: valueToSend,
            });
        } catch (e) {
            console.error('❌ Не вдалося оновити на сервері:', e);
        }
        setEditing(null);
    };

    /* відбираємо поля під роль */
    const viewable = role ? VIEWABLE_FIELDS[role] : [];
    const entries  = Object.entries(user)
        .filter(([k]) => !HIDDEN_GLOBAL.includes(k) && viewable.includes(k));

    /* ──────────────────────────── 3. JSX ──────────────────────────── */
    return (
        <AnimatePresence>
            {isOpen && (
                <>
                    {/* backdrop */}
                    <motion.div
                        className="fixed inset-0 z-[100] bg-black/50 backdrop-blur-sm"
                        initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                        onClick={close}
                    />

                    {/* card */}
                    <motion.div
                        className="fixed left-1/2 top-1/2 z-[101] w-[90vw] max-w-md max-h-[90vh]
                       -translate-x-1/2 -translate-y-1/2 overflow-y-auto
                       rounded-3xl bg-white p-6 shadow-2xl flex flex-col gap-5"
                        initial={{ scale: 0.8, opacity: 0 }}
                        animate={{ scale: 1,  opacity: 1 }}
                        exit={{   scale: 0.8, opacity: 0 }}
                        transition={{ type: 'spring', stiffness: 260, damping: 18 }}
                    >
                        {/* header */}
                        <div className="flex items-center justify-between">
                            <h2 className="flex items-center gap-2 text-lg font-bold text-[#2B3674]">
                                <span>👤</span>{user.role?.toUpperCase()}
                            </h2>
                            <button onClick={close} className="text-gray-500 hover:text-gray-800">
                                <X size={22} />
                            </button>
                        </div>

                        {/* body */}
                        <div className="space-y-4">
                            {entries.map(([k, v]) => {
                                const isEdit   = editing === k;
                                const editable = role ? EDITABLE_FIELDS[role].includes(k) : false;

                                return (
                                    <div key={k}
                                         className="group relative flex flex-col gap-1 rounded-xl p-2
                                  transition-colors hover:bg-[#F5F7FD]">
                                        {/* label */}
                                        <span className="text-[11px] tracking-wide text-[#8F9BBA] uppercase">
                      {prettify(k)}
                    </span>

                                        {/* value / input */}
                                        {isEdit ? (
                                            <input autoFocus value={temp}
                                                   onChange={e => setTemp(e.target.value)}
                                                   className="rounded-lg border bg-white px-3 py-1 text-sm
                                        focus:border-[#4B22F4] focus:ring-0" />
                                        ) : (
                                            <p className="break-all text-sm font-medium text-[#2B3674]">
                                                {Array.isArray(v) ? v.join(', ') : String(v ?? '—')}
                                            </p>
                                        )}

                                        {/* edit icon (тільки якщо поле editable) */}
                                        {!isEdit && editable && (
                                            <button onClick={() => beginEdit(k)}
                                                    className="absolute right-2 top-2 hidden rounded-full bg-white p-1
                                         text-[#4B22F4] shadow group-hover:block
                                         hover:bg-[#ECECFF]"
                                                    title="Редагувати">
                                                <Pencil size={16} />
                                            </button>
                                        )}

                                        {/* save / cancel */}
                                        {isEdit && (
                                            <div className="mt-2 flex gap-2">
                                                <button onClick={saveEdit}
                                                        className="flex items-center gap-1 rounded-lg bg-[#4B22F4]
                                           px-3 py-1 text-xs font-medium text-white
                                           hover:bg-[#3718c6]">
                                                    <Check size={14} /> Зберегти
                                                </button>
                                                <button onClick={cancelEdit}
                                                        className="flex items-center gap-1 rounded-lg border border-[#A3AED0]
                                           px-3 py-1 text-xs text-[#2B3674] hover:bg-[#F3F4F8]">
                                                    <X size={14} /> Скасувати
                                                </button>
                                            </div>
                                        )}
                                    </div>
                                );
                            })}

                            {entries.length === 0 && (
                                <p className="text-center text-sm text-[#8F9BBA]">
                                    Немає доступних полів для перегляду
                                </p>
                            )}
                        </div>
                    </motion.div>
                </>
            )}
        </AnimatePresence>
    );
}
