'use client';

/**
 * PromotionDetailsModal — view + actions (activate/deactivate/delete).
 * -------------------------------------------------------------------
 * - Russian UI, English docs.
 * - Delete uses a custom ConfirmDialog (no window.confirm).
 * - On delete: closes confirm, closes modal, optimistic cache removal,
 *   then invalidates active promotion queries.
 */

import React from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { Check, Loader2, Trash2, Users, X } from 'lucide-react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import ConfirmDialog from './ConfirmDialog';
import type { PromotionOut } from './CreatePromotionModal';
import { fetchJSON } from '../utils';

const API = process.env.NEXT_PUBLIC_API_URL ?? "";

type TopWorker = { worker_id: string; username: string; credits_count: number };

// @ts-ignore
const TYPE_DOT: Record<PromotionOut['promotion_type'], string> = {
    Helix: 'bg-[#7144ff]',
    Union: 'bg-[#4318FF]',
    General: 'bg-slate-400',
};
const TYPE_LABEL = { Helix: 'Helix', Union: 'Union', General: 'General' };

export default function PromotionDetailsModal({
                                                  promo,
                                                  open,
                                                  onClose,
                                                  onDeleted,
                                              }: {
    promo: PromotionOut | null;
    open: boolean;
    onClose: () => void;
    onDeleted?: () => void;
}) {
    const qc = useQueryClient();
    const pid = promo?.id ?? '';

    const { data: workers, isLoading } = useQuery<TopWorker[]>({
        queryKey: ['top-workers', { pid }],
        queryFn: () => fetchJSON<TopWorker[]>(`${API}/api/dashboard/admin/promotions/top-workers?limit=3`),
        enabled: open && Boolean(pid),
        staleTime: 5000,
    });

    const activate = useMutation({
        mutationFn: () =>
            fetchJSON<PromotionOut>(
                `${API}/api/dashboard/admin/promotions/${pid}/activate`,
                { method: 'PATCH' }
            ),
        onSuccess: () => {
            qc.invalidateQueries({ queryKey: ['promotions'] });
            onClose(); // закриваємо модалку після активації
        },
    });

    const deactivate = useMutation({
        mutationFn: () =>
            fetchJSON<{ status: string; id: string }>(`${API}/api/dashboard/admin/promotions/${pid}/deactivate`, {
                method: 'PATCH',
            }),
        onSuccess: () => {
            qc.invalidateQueries({ queryKey: ['promotions'] });
            onClose(); // закриваємо модалку після деактивації
        },
    });

    const [confirmOpen, setConfirmOpen] = React.useState(false);

    const remove = useMutation({
        mutationFn: (id: string) =>
            fetchJSON<void>(`${API}/api/dashboard/admin/promotions/${id}`, { method: 'DELETE' }),
        onMutate: async (id) => {
            const queries = qc.getQueriesData<PromotionOut[]>({ queryKey: ['promotions'] });
            queries.forEach(([key, list]) => {
                qc.setQueryData(key, (list ?? []).filter((p) => p.id !== id));
            });
        },
        onSettled: () => {
            qc.invalidateQueries({ queryKey: ['promotions'], refetchType: 'active' });
            onDeleted?.();
        },
    });

    const handleConfirmDelete = React.useCallback(() => {
        const id = promo?.id;
        if (!id) return; // safety

        // можна спочатку стартувати мутацію,
        // а потім закривати діалоги — або навпаки, id уже збережено:
        remove.mutate(id);
        setConfirmOpen(false);
        onClose();
    }, [promo, onClose, remove]);

    return (
        <AnimatePresence>
            {open && promo && (
                <motion.div
                    key="overlay-details"
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
                        key="dialog-details"
                        initial={{ scale: 0.94, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        exit={{ scale: 0.94, opacity: 0 }}
                        transition={{ duration: 0.2 }}
                        onClick={(e) => e.stopPropagation()}
                        className="w-[min(820px,94vw)] rounded-3xl border border-slate-200 bg-white p-5 shadow-2xl"
                    >
                        {/* Header */}
                        <div className="mb-4 flex items-center justify-between">
                            <div className="flex items-center">
                                <span className={['h-2.5 w-2.5 rounded-full', TYPE_DOT[promo.promotion_type]].join(' ')} />
                                <h3 className="text-xl font-extrabold text-[#2B3674]">Промоакция {promo.promotion_type}</h3>
                                <span
                                    className={[
                                        'ml-2 rounded-full px-2 py-0.5 text-xs',
                                        promo.is_active ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-slate-600',
                                    ].join(' ')}
                                >
                  {promo.is_active ? 'Активна' : 'Неактивна'}
                </span>
                            </div>
                            <button onClick={onClose} className="cursor-pointer rounded-full p-1 text-slate-500 hover:bg-slate-100" title="Закрыть">
                                <X size={18} />
                            </button>
                        </div>

                        {/* Body */}
                        <div className="rounded-2xl border border-slate-200 bg-slate-50/60 p-4 text-sm">
                            <div className="mb-1 text-xs font-medium text-[#8F9BBA]">Описание</div>
                            <p className="whitespace-pre-wrap text-slate-700">{promo.description}</p>
                        </div>

                        <div className="mt-5">
                            <div className="mb-2 flex items-center gap-2 text-sm font-semibold text-[#2B3674]">
                                <Users size={16} /> ТОП-3 работника
                            </div>
                            <div className="rounded-2xl border border-slate-200 bg-white">
                                <div className="grid grid-cols-3 gap-0 px-4 py-2 text-xs text-slate-500">
                                    <div>Пользователь</div>
                                    <div className="text-center">Кол-во кредитов</div>
                                    <div className="text-right">ID</div>
                                </div>
                                <div className="divide-y">
                                    {isLoading ? (
                                        <div className="flex items-center justify-center gap-2 py-6 text-slate-500">
                                            <Loader2 className="animate-spin" size={16} /> Загрузка…
                                        </div>
                                    ) : workers?.length ? (
                                        workers.map((w) => (
                                            <div key={w.worker_id} className="grid grid-cols-3 items-center px-4 py-2 text-sm">
                                                <div className="truncate">{w.username}</div>
                                                <div className="text-center font-medium">{w.credits_count}</div>
                                                <div className="truncate text-right text-slate-500">{w.worker_id}</div>
                                            </div>
                                        ))
                                    ) : (
                                        <div className="py-6 text-center text-sm text-slate-500">Пока пусто</div>
                                    )}
                                </div>
                            </div>
                        </div>

                        {/* Actions */}
                        <div className="mt-6 flex flex-wrap justify-between gap-2">
                            <button
                                onClick={() => setConfirmOpen(true)}
                                disabled={remove.isPending}
                                className="cursor-pointer inline-flex items-center gap-2 rounded-xl border border-rose-300 bg-rose-50 px-4 py-2 text-sm text-rose-700 hover:bg-rose-100 disabled:opacity-50"
                                title="Удалить (soft delete)"
                            >
                                {remove.isPending ? <Loader2 size={16} className="animate-spin" /> : <Trash2 size={16} />}
                                Удалить
                            </button>

                            {promo.is_active ? (
                                <button
                                    onClick={() => deactivate.mutate()}
                                    disabled={deactivate.isPending}
                                    className="cursor-pointer inline-flex items-center gap-2 rounded-xl border border-slate-300 bg-white px-4 py-2 text-sm hover:bg-slate-50 disabled:opacity-50"
                                    title="Деактивировать"
                                >
                                    {deactivate.isPending ? <Loader2 size={16} className="animate-spin" /> : <X size={16} />}
                                    Деактивировать
                                </button>
                            ) : (
                                <button
                                    onClick={() => activate.mutate()}
                                    disabled={activate.isPending}
                                    className="cursor-pointer inline-flex items-center gap-2 rounded-xl bg-[#7144ff] px-4 py-2 text-sm font-semibold text-white hover:brightness-110 disabled:opacity-50"
                                    title="Активировать"
                                >
                                    {activate.isPending ? <Loader2 size={16} className="animate-spin" /> : <Check size={16} />}
                                    Активировать
                                </button>
                            )}
                        </div>
                    </motion.div>

                    {/* Confirm dialog */}
                    <ConfirmDialog
                        open={confirmOpen}
                        onClose={() => setConfirmOpen(false)}
                        onConfirm={handleConfirmDelete}
                        loading={remove.isPending}
                        title="Удалить промоакцию?"
                        subtitle={
                            promo
                                ? `Эта промоакция будет мягко удалена (soft delete) и исчезнет из списка. Описание: “${(promo.description || '')
                                    .slice(0, 120)}${(promo.description || '').length > 120 ? '…' : ''}”.`
                                : ''
                        }
                        confirmText="Удалить"
                        cancelText="Отмена"
                    />
                </motion.div>
            )}
        </AnimatePresence>
    );
}
