'use client';

/**
 * AdminPromotions — admin block to manage promotions.
 * ---------------------------------------------------
 * - UPPERCASE enum у фільтрах та запитах
 * - Стабільний infinite-scroll
 * - Людські помилки через fetchJSON
 */

import React, { useEffect, useMemo, useRef, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { AnimatePresence, motion } from 'framer-motion';
import {Filter, Plus, RefreshCcw, CheckCircle2, RefreshCw} from 'lucide-react';

import Select from './parts/Select';
import PromotionsList from './parts/PromotionsList';
import CreatePromotionModal, { type PromotionOut, type PromotionType } from './parts/CreatePromotionModal';
import PromotionDetailsModal from './parts/PromotionDetailsModal';
import ConfirmDialog from './parts/ConfirmDialog';
import { fetchJSON } from './utils';

const API = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';
const PAGE_STEP = 8 as const;

export default function AdminPromotions() {
    // filters
    const [ptype, setPtype] = useState<'all' | PromotionType>('all');
    const [status, setStatus] = useState<'all' | 'active' | 'inactive'>('all');

    // paging
    const [limit, setLimit] = useState<number>(PAGE_STEP);
    const loadMoreRef = useRef<HTMLDivElement>(null);
    const listScrollRef = useRef<HTMLDivElement>(null);

    const lastScrollTopRef = useRef<number>(0);
    const loadingMoreRef = useRef<boolean>(false);

    // modals / banners
    const [createOpen, setCreateOpen] = useState(false);
    const [details, setDetails] = useState<PromotionOut | null>(null);
    const [createdOk, setCreatedOk] = useState(false);
    const [deletedOk, setDeletedOk] = useState(false);

    const qc = useQueryClient();

    // URL & query
    const listUrl = useMemo(() => {
        const u = new URL(`${API}/api/dashboard/admin/promotions`);
        u.searchParams.set('limit', String(limit));
        if (ptype !== 'all') u.searchParams.set('ptype', ptype); // вже UPPERCASE
        if (status !== 'all') u.searchParams.set('is_active', String(status === 'active'));
        return u.toString();
    }, [limit, ptype, status]);

    const { data, isLoading, isFetching, error, refetch } = useQuery<PromotionOut[], Error>({
        queryKey: ['promotions', { limit, ptype, status }],
        queryFn: () => fetchJSON<PromotionOut[]>(listUrl),
        staleTime: 5000,
        keepPreviousData: true,
    });

    // reset page on filter change
    useEffect(() => setLimit(PAGE_STEP), [ptype, status]);

    const items = data ?? [];
    const hasMore = items.length >= limit;

    // IO inside scroll container; trigger only when sentinel is fully visible
    useEffect(() => {
        const sentinel = loadMoreRef.current;
        const rootEl = listScrollRef.current;
        if (!sentinel || !rootEl) return;

        const io = new IntersectionObserver(
            ([entry]) => {
                if (!entry.isIntersecting) return;
                if (isFetching) return;
                if (!hasMore) return;

                lastScrollTopRef.current = rootEl.scrollTop;
                loadingMoreRef.current = true;
                setLimit((n) => n + PAGE_STEP);
            },
            { root: rootEl, threshold: 1, rootMargin: '0px' }
        );

        io.observe(sentinel);
        return () => io.disconnect();
    }, [isFetching, hasMore]);

    // restore scroll after page append
    useEffect(() => {
        if (!loadingMoreRef.current) return;
        const el = listScrollRef.current;
        if (el) el.scrollTop = lastScrollTopRef.current;
        loadingMoreRef.current = false;
    }, [items.length]);

    const resetFilters = () => {
        setPtype('all');
        setStatus('all');
    };

    // delete mutation (row + confirm dialog here)
    const del = useMutation({
        mutationFn: (id: string) =>
            fetchJSON<void>(`${API}/api/dashboard/admin/promotions/${id}`, { method: 'DELETE' }),
        onMutate: async (id) => {
            // optimistic removal from all cached lists
            const queries = qc.getQueriesData<PromotionOut[]>({ queryKey: ['promotions'] });
            queries.forEach(([key, list]) => {
                qc.setQueryData(key, (list ?? []).filter((p) => p.id !== id));
            });
        },
        onSettled: () => {
            qc.invalidateQueries({ queryKey: ['promotions'], refetchType: 'active' });
            setDeletedOk(true);
            setTimeout(() => setDeletedOk(false), 1600);
        },
    });

    return (
        <section className="relative rounded-3xl p-[1px] overflow-hidden bg-[conic-gradient(from_180deg_at_50%_50%,#ECE9FF,white,#DDE7FF,#ECE9FF)]">
            {/* decorative glows */}
            <div className="pointer-events-none absolute -top-24 -left-20 h-72 w-72 rounded-full blur-2xl opacity-40 bg-[radial-gradient(circle_at_center,rgba(113,68,255,0.18),rgba(255,255,255,0))]" />
            <div className="pointer-events-none absolute -bottom-28 -right-24 h-80 w-80 rounded-full blur-2xl opacity-40 bg-[radial-gradient(circle_at_center,rgba(27,37,89,0.14),rgba(255,255,255,0))]" />

            {/* fixed-height card like other panels */}
            <div className="relative flex h-[420px] sm:h-[440px] lg:h-[460px] flex-col rounded-[calc(theme(borderRadius.3xl)-1px)] bg-white/90 p-6 shadow-xl overflow-hidden backdrop-blur border border-transparent hover:border-[#E5E9F6]">
                {/* header */}
                <div className="mb-4 flex items-center justify-between gap-3">
                    <div>
                        <h2 className="text-lg font-extrabold text-[#2B3674] tracking-tight">Промоакции</h2>
                        <div className="mt-1 text-xs text-slate-500">Управление промо и статусами</div>
                    </div>
                    <div className="flex items-center gap-2">
                        <button
                            onClick={() => refetch()}
                            title="Обновить"
                            className="cursor-pointer p-2 rounded-lg text-[#7144ff] hover:bg-[#F4F7FE] transition"
                        >
                            <RefreshCw size={18} className={isLoading ? 'animate-spin' : ''} />
                        </button>
                    </div>
                </div>

                {/* success banners */}
                <AnimatePresence>
                    {createdOk && (
                        <motion.p
                            key="ok-created"
                            initial={{ opacity: 0, y: -6 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -6 }}
                            transition={{ duration: 0.18 }}
                            className="mb-3 flex items-center justify-center gap-2 rounded-xl border border-emerald-300 bg-emerald-50 px-4 py-2 text-sm text-emerald-700"
                            role="status"
                        >
                            <CheckCircle2 size={16} aria-hidden="true" /> Промоакция успешно создана!
                        </motion.p>
                    )}
                </AnimatePresence>
                <AnimatePresence>
                    {deletedOk && (
                        <motion.p
                            key="ok-deleted"
                            initial={{ opacity: 0, y: -6 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -6 }}
                            transition={{ duration: 0.18 }}
                            className="mb-3 flex items-center justify-center gap-2 rounded-xl border border-rose-300 bg-rose-50 px-4 py-2 text-sm text-rose-700"
                            role="status"
                        >
                            <CheckCircle2 size={16} aria-hidden="true" /> Промоакция удалена.
                        </motion.p>
                    )}
                </AnimatePresence>

                {/* filters */}
                <div className="mb-4 grid grid-cols-1 gap-3 sm:grid-cols-3">
                    <Select
                        label="Тип"
                        value={ptype}
                        onChange={(v) => setPtype((typeof v === 'string' ? v : (v as any)?.value) as any)}
                        options={[
                            { value: 'all', label: 'Все' },
                            { value: 'HELIX', label: 'Helix' },
                            { value: 'UNION', label: 'Union' },
                            { value: 'GENERAL', label: 'General' },
                        ]}
                    />
                    <Select
                        label="Статус"
                        value={status}
                        onChange={(v) => setStatus((typeof v === 'string' ? v : (v as any)?.value) as any)}
                        options={[
                            { value: 'all', label: 'Все' },
                            { value: 'active', label: 'Активные' },
                            { value: 'inactive', label: 'Неактивные' },
                        ]}
                    />
                    <div className="flex items-end">
                        <button
                            onClick={resetFilters}
                            className="cursor-pointer inline-flex w-full items-center justify-center gap-2 rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm hover:bg-slate-50"
                            title="Сбросить фильтры"
                        >
                            <Filter size={16} /> Сбросить
                        </button>
                    </div>
                </div>

                {/* list (takes remaining height) */}
                <div className="min-h-0 flex-1 pb-4">
                    <PromotionsList
                        items={items}
                        isLoading={isLoading}
                        isFetching={isFetching}
                        error={error}
                        onItemClick={(p) => setDetails(p)}
                        loadMoreRef={loadMoreRef}
                        scrollRef={listScrollRef}
                    />
                </div>

                <div className="flex items-center justify-end">
                    <button
                        onClick={() => setCreateOpen(true)}
                        className="cursor-pointer inline-flex items-center gap-2 rounded-xl bg-[#7144ff] px-3 py-2 text-sm font-semibold text-white hover:brightness-110"
                        title="Создать промоакцию"
                    >
                        <Plus size={16} /> Создать промо
                    </button>
                </div>
            </div>

            {/* create modal */}
            <CreatePromotionModal
                open={createOpen}
                onClose={() => setCreateOpen(false)}
                onCreated={() => {
                    setCreatedOk(true);
                    setTimeout(() => setCreatedOk(false), 1800);
                }}
            />

            {/* details modal */}
            <PromotionDetailsModal
                promo={details}
                open={!!details}
                onClose={() => setDetails(null)}
                onDeleted={() => {
                    setDeletedOk(true);
                    setTimeout(() => setDeletedOk(false), 1600);
                }}
            />

            {/* row delete confirm (якщо використовуєш окремо) */}
            <ConfirmDialog
                open={false}
                onClose={() => {}}
                onConfirm={() => {}}
                loading={false}
                title="Удалить промоакцию?"
                subtitle=""
                confirmText="Удалить"
                cancelText="Отмена"
            />
        </section>
    );
}
