'use client';

/**
 * CreatePromotionModal — create new promotion modal.
 * ------------------------------------------------------------
 * - Завжди відправляє UPPERCASE enum: 'HELIX' | 'UNION' | 'GENERAL'
 * - Акуратно показує помилки (в т.ч. масиви 422 detail)
 */

import React, { useEffect, useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { Loader2, X } from 'lucide-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import Select from './Select'; // шлях залиш як у тебе в проекті
import { fetchJSON } from '../utils';

export type PromotionType = 'HELIX' | 'UNION' | 'GENERAL';

export type PromotionOut = {
    id: string;
    promotion_type: PromotionType;
    description: string;
    is_active: boolean;
    created_at: string;
    updated_at: string;
};

const API = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

function normalizeType(v: unknown): PromotionType {
    const raw = typeof v === 'string' ? v : (v as any)?.value ?? '';
    const up = String(raw).toUpperCase();
    if (up !== 'HELIX' && up !== 'UNION' && up !== 'GENERAL') {
        throw new Error('Невідомий тип промо');
    }
    return up as PromotionType;
}

function toErrorMessage(e: any): string {
    if (!e) return 'Помилка';
    if (typeof e === 'string') return e;
    if (typeof e.message === 'string') return e.message;
    try { return JSON.stringify(e); } catch { return 'Помилка'; }
}

export default function CreatePromotionModal({
                                                 open,
                                                 onClose,
                                                 onCreated,
                                             }: {
    open: boolean;
    onClose: () => void;
    onCreated?: () => void;
}) {
    const qc = useQueryClient();
    const [type, setType] = useState<PromotionType>('HELIX');
    const [desc, setDesc] = useState('');
    const [active, setActive] = useState(true);
    const [err, setErr] = useState<string | null>(null);

    useEffect(() => {
        if (!open) {
            setType('HELIX');
            setDesc('');
            setActive(true);
            setErr(null);
        }
    }, [open]);

    const { mutate, isPending } = useMutation({
        mutationFn: () =>
            fetchJSON<PromotionOut>(`${API}/api/dashboard/admin/promotions`, {
                method: 'POST',
                body: JSON.stringify({
                    promotion_type: type,             // вже UPPERCASE
                    description: desc.trim(),
                    is_active: active,
                }),
            }),
        onSuccess: () => {
            qc.invalidateQueries({ queryKey: ['promotions'] });
            onCreated?.();
            onClose();
        },
        onError: (e: any) => setErr(toErrorMessage(e)),
    });

    return (
        <AnimatePresence>
            {open && (
                <motion.div
                    key="overlay-create"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 0.2 }}
                    className="fixed inset-0 z-[60] flex items-center justify-center bg-black/40 backdrop-blur-sm"
                    onClick={onClose}
                    role="dialog"
                    aria-modal
                >
                    <motion.div
                        key="dialog-create"
                        initial={{ scale: 0.94, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        exit={{ scale: 0.94, opacity: 0 }}
                        transition={{ duration: 0.2 }}
                        onClick={(e) => e.stopPropagation()}
                        className="w-[min(680px,92vw)] rounded-3xl border border-slate-200 bg-white p-5 shadow-2xl"
                    >
                        <div className="mb-4 flex items-center justify-between">
                            <h3 className="text-xl font-extrabold text-[#2B3674]">Создать промоакцию</h3>
                            <button
                                onClick={onClose}
                                className="cursor-pointer rounded-full p-1 text-slate-500 hover:bg-slate-100"
                                title="Закрыть"
                            >
                                <X size={18} />
                            </button>
                        </div>

                        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                            <Select
                                label="Тип промо"
                                value={type}
                                onChange={(v) => {
                                    try {
                                        setType(normalizeType(v));
                                        setErr(null);
                                    } catch (e) {
                                        setErr(toErrorMessage(e));
                                    }
                                }}
                                options={[
                                    { value: 'HELIX', label: 'Helix' },
                                    { value: 'UNION', label: 'Union' },
                                    { value: 'GENERAL', label: 'General' },
                                ]}
                            />

                            <div>
                                <div className="mb-1 text-xs font-medium text-[#8F9BBA]">Статус</div>
                                <button
                                    type="button"
                                    onClick={() => setActive((s) => !s)}
                                    className={[
                                        'cursor-pointer inline-flex items-center gap-2 rounded-xl border px-3 py-2 text-sm',
                                        active
                                            ? 'border-transparent bg-emerald-50 text-emerald-700'
                                            : 'border-slate-300 bg-slate-50 text-slate-600 hover:bg-slate-100',
                                    ].join(' ')}
                                    title={active ? 'Сделать неактивной' : 'Сделать активной'}
                                >
                                    <span className={['h-2.5 w-2.5 rounded-full', active ? 'bg-emerald-500' : 'bg-slate-400'].join(' ')} />
                                    {active ? 'Активна' : 'Неактивна'}
                                </button>
                            </div>

                            <div className="sm:col-span-2">
                                <div className="mb-1 text-xs font-medium text-[#8F9BBA]">Описание</div>
                                <textarea
                                    value={desc}
                                    onChange={(e) => setDesc(e.target.value)}
                                    rows={5}
                                    maxLength={4000}
                                    placeholder="Коротко опишите условия промо…"
                                    className="w-full resize-y rounded-xl border border-slate-300 bg-slate-50 px-3 py-2 text-sm focus:border-[#7144ff] focus:outline-none"
                                />
                            </div>
                        </div>

                        <div className="mt-4 min-h-[28px] text-sm">
                            {err && (
                                <div className="rounded-md border border-red-300 bg-red-50 px-3 py-2 text-red-700" role="alert">
                                    {err}
                                </div>
                            )}
                        </div>

                        <div className="mt-3 flex justify-end gap-2">
                            <button
                                onClick={onClose}
                                disabled={isPending}
                                className="cursor-pointer rounded-xl border border-slate-300 bg-white px-4 py-2 text-sm hover:bg-slate-50 disabled:opacity-50"
                                title="Отменить"
                            >
                                Отменить
                            </button>
                            <button
                                onClick={() => mutate()}
                                disabled={isPending || !desc.trim()}
                                className="cursor-pointer inline-flex items-center gap-2 rounded-xl bg-[#7144ff] px-4 py-2 text-sm font-semibold text-white hover:brightness-110 disabled:opacity-50"
                                title="Создать промоакцию"
                            >
                                {isPending && <Loader2 size={16} className="animate-spin" />}
                                Создать
                            </button>
                        </div>
                    </motion.div>
                </motion.div>
            )}
        </AnimatePresence>
    );
}
