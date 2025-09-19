/* ------------------------------------------------------------------
 * ExpandedModal.tsx
 * Production-ready модалка: пагінація «бочки» + профайл + CompactTable
 * ------------------------------------------------------------------ */

'use client';

import React, {
    useCallback,
    useEffect,
    useMemo,
    useRef,
    useState,
} from 'react';
import {
    ArrowLeft,
    ChevronDown,
    Loader2,
    Pencil,
    X,
} from 'lucide-react';

import CompactTable              from './CompactTable';
import SearchInput               from './SearchInput';
import type { ModalBucketState, Row } from '../types';

/*  shared hooks  */
import { useDebounce            } from '../hooks/useDebounce';
import UserStorage from "@/services/UserStorage";

/* -------------------------- props --------------------------- */
export interface ExpandedModalProps {
    open: boolean;
    onClose: () => void;

    /* таби / ролі */
    labels: string[];
    activeRole: number;
    onSwitchRole: (idx: number) => void;

    /* список */
    title: string;
    modalState: ModalBucketState;
    fetchCurrent: (reset?: boolean) => void;
    loadMore: () => void;
    pageSize?: number;
    onRowClick: (row: Row) => void;
    colHeads: string[][];
    colKeys : string[][];

    /* профайл */
    detailData: Record<string, unknown> | null;
    detailLoading: boolean;
    detailError: string | null;
    onCloseDetail: () => void;
    onRefetchDetail: () => void;
}

/* -------------------------- helpers ------------------------- */
const SpinnerRow = () => (
    <div className="py-4 flex items-center justify-center text-[#8F9BBA]">
        <Loader2 size={16} className="animate-spin mr-2" /> Загрузка…
    </div>
);

type ViewMode = 'list' | 'detail';

/* ============================================================ */
const ExpandedModal: React.FC<ExpandedModalProps> = ({
                                                         /* 외부 props */
                                                         open,
                                                         onClose,
                                                         labels,
                                                         activeRole,
                                                         onSwitchRole,
                                                         title,
                                                         modalState,
                                                         fetchCurrent,
                                                         loadMore,
                                                         pageSize = 6,
                                                         onRowClick,
                                                         colHeads,
                                                         colKeys,
                                                         detailData,
                                                         detailLoading,
                                                         detailError,
                                                         onCloseDetail,
                                                         onRefetchDetail,
                                                     }) => {
    /* ---------------- local state ---------------- */
    const [viewMode,  setViewMode ] = useState<ViewMode>('list');
    const [searchRaw, setSearchRaw] = useState('');
    const debouncedSearch           = useDebounce(searchRaw, 400);

    /* поле, по якому шукаємо */
    const [searchField, setSearchField] =
        useState<string>(colKeys[activeRole]?.[0] ?? '');

    /* reset search-field при зміні ролі */
    useEffect(() => {
        setSearchField(colKeys[activeRole]?.[0] ?? '');
        setSearchRaw('');
    }, [activeRole, colKeys]);

    /* ---------------- derived data ---------------- */
    const keys  = colKeys [activeRole] ?? [];
    const heads = colHeads[activeRole] ?? keys;

    const filteredRows = useMemo<Row[]>(() => {
        const term = debouncedSearch.trim().toLowerCase();
        if (!term) return modalState.data;

        return modalState.data.filter((row) => {
            const val = String((row as any)[searchField] ?? '').toLowerCase();
            return val.includes(term);
        });
    }, [modalState.data, debouncedSearch, searchField]);

    const hasMore = !modalState.loading && !modalState.done;

    /* ---------------- scroll sentinel ---------------- */
    // const sentinelRef = useRef<HTMLDivElement | null>(null);
    // const hitBottom   = useIntersectionObserver(sentinelRef, {
    //     rootMargin: '200px',
    //     threshold : 0,
    // });

    /* ---------- refs ---------- */
    const wrapperRef  = useRef<HTMLDivElement | null>(null);   // scroll-box
    const sentinelRef = useRef<HTMLDivElement | null>(null);   // «хвост» таблиці

    /* ---------------- view-mode sync ---------------- */
    useEffect(() => {
        setViewMode(detailData || detailLoading ? 'detail' : 'list');
    }, [detailData, detailLoading]);

    /* ---------------- body-scroll lock -------------- */
    useEffect(() => {
        document.body.style.overflow = open ? 'hidden' : '';
        return () => { document.body.style.overflow = ''; };
    }, [open]);

    /* ---------------- helpers ----------------------- */
    const closeAll = useCallback(() => {
        onCloseDetail();
        setSearchRaw('');
        onClose();
    }, [onClose, onCloseDetail]);

    /* ============================================================ */
    return (
        <div
            className={`fixed inset-0 z-[100] flex items-center justify-center bg-black/40 backdrop-blur-sm transition-opacity duration-300 ${
                open ? 'visible opacity-100' : 'invisible opacity-0'
            }`}
            onClick={closeAll}
        >
            {/* card */}
            <div
                onClick={(e) => e.stopPropagation()}
                className={`w-full max-w-6xl bg-white rounded-2xl shadow-xl flex flex-col transform transition-all duration-300 ${
                    open ? 'scale-100 translate-y-0' : 'scale-95 translate-y-4'
                }`}
                style={{ minHeight: 520, maxHeight: '80vh' }}
            >
                {/* -------- HEADER -------- */}
                <header className="px-6 pt-6 pb-4 border-b flex items-center justify-between">
                    <div className="flex flex-col gap-1">
                        <div className="flex items-center gap-2">
                            {viewMode === 'detail' && (
                                <button
                                    className="p-2 -ml-2 rounded-lg text-[#7144ff] hover:bg-[#F4F7FE]"
                                    onClick={() => setViewMode('list')}
                                >
                                    <ArrowLeft size={18} />
                                </button>
                            )}
                            <h3 className="text-xl font-bold text-[#2B3674]">
                                {viewMode === 'detail' ? 'Профиль' : title}
                            </h3>
                        </div>

                        {viewMode === 'list' && labels.length > 1 && (
                            <div className="flex flex-wrap gap-2 mt-1">
                                {labels.map((l, i) => (
                                    <button
                                        key={l}
                                        onClick={() => onSwitchRole(i)}
                                        className={`px-3 py-1.5 rounded-lg text-sm font-medium transition ${
                                            i === activeRole
                                                ? 'bg-[#7144ff] text-white shadow'
                                                : 'bg-[#F4F7FE] hover:bg-[#EEF3FF] text-[#2B3674]'
                                        }`}
                                    >
                                        {l}
                                    </button>
                                ))}
                            </div>
                        )}
                    </div>

                    <button
                        className="p-2 rounded-lg text-[#8F9BBA] hover:text-[#2B3674] hover:bg-[#F4F7FE]"
                        onClick={closeAll}
                    >
                        <X size={20} />
                    </button>
                </header>

                {/* -------- BODY -------- */}
                <section className="flex-1 flex flex-col overflow-auto px-6 pb-6">
                    {/* ================= LIST ================= */}
                    {viewMode === 'list' && (
                        <>
                            {/* search / refresh */}
                            <div className="mt-4 mb-3 flex items-center gap-3">
                                <SearchInput
                                    value={searchRaw}
                                    onChange={setSearchRaw}
                                    placeholder="Поиск…"
                                    className="flex-1"
                                />

                                {keys.length > 0 && (
                                    <div className="relative w-fit">
                                        <select
                                            value={searchField}
                                            onChange={(e) => setSearchField(e.target.value)}
                                            className="appearance-none w-40 pl-3 pr-8 py-2 rounded-lg bg-[#F4F7FE] hover:bg-[#EEF3FF] text-sm text-[#2B3674] border border-transparent focus:border-[#7144ff] outline-none cursor-pointer"
                                        >
                                            {keys.map((k) => (
                                                <option key={k} value={k}>
                                                    {k}
                                                </option>
                                            ))}
                                        </select>
                                        <ChevronDown
                                            size={14}
                                            className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-[#2B3674]"
                                        />
                                    </div>
                                )}

                                <button
                                    onClick={() => fetchCurrent(true)}
                                    className="px-4 py-2 rounded-lg bg-[#F4F7FE] text-[#2B3674] text-sm font-medium hover:bg-[#EEF3FF]"
                                >
                                    Обновить
                                </button>
                            </div>

                            {/* таблиця */}
                            <div
                                ref={wrapperRef}
                                className="flex-1 overflow-auto rounded-md border border-[#EEF0F6]"
                            >
                                <CompactTable
                                    rows={filteredRows}
                                    loading={modalState.loading && modalState.skip === 0}
                                    pageSize={pageSize}
                                    colKeys={keys}
                                    headTitles={heads}
                                    onRowClick={onRowClick}
                                />

                                {modalState.loading && modalState.skip > 0 && <SpinnerRow />}
                                {!modalState.loading && modalState.done && (
                                    <div className="py-4 text-center text-[#A3AED0] text-sm">
                                        Это всё
                                    </div>
                                )}

                                {/* sentinel — точка, куди догортаємо */}
                                <div ref={sentinelRef} />
                            </div>

                            {/* footer */}
                            <div className="mt-4 flex justify-between text-[12px] text-[#8F9BBA]">
                                <div>
                                    Показано:{' '}
                                    <span className="font-semibold text-[#2B3674]">
                    {filteredRows.length}
                  </span>
                                    {modalState.total > 0 && (
                                        <>
                                            {' '}из{' '}
                                            <span className="font-semibold text-[#2B3674]">
                        {modalState.total}
                      </span>
                                        </>
                                    )}
                                </div>

                                {hasMore && (
                                    <button
                                        disabled={modalState.loading}
                                        onClick={loadMore}
                                        className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                                            modalState.loading
                                                ? 'bg-[#F4F7FE] text-[#A3AED0] cursor-not-allowed'
                                                : 'bg-[#7144ff] text-white hover:opacity-90'
                                        }`}
                                    >
                                        {modalState.loading ? '…' : 'Загрузить ещё'}
                                    </button>
                                )}
                            </div>

                            {modalState.error && (
                                <div className="mt-3 text-xs text-red-500 font-medium">
                                    Ошибка: {modalState.error}
                                </div>
                            )}
                        </>
                    )}

                    {/* ================= DETAIL ================= */}
                    {viewMode === 'detail' && (
                        <ProfileView
                            loading={detailLoading}
                            error={detailError}
                            data={detailData}
                            onBack={() => setViewMode('list')}
                            onRefresh={onRefetchDetail}
                        />
                    )}
                </section>
            </div>
        </div>
    );
};

export default ExpandedModal;

/* ------------------------------------------------------------------
 * ProfileView
 * ------------------------------------------------------------------ */
interface ProfileViewProps {
    loading: boolean;
    error: string | null;
    data: Record<string, unknown> | null;
    onBack: () => void;
    onRefresh: () => void;
}

const ProfileView: React.FC<ProfileViewProps> = ({
                                                     loading,
                                                     error,
                                                     data,
                                                     onBack,
                                                     onRefresh,
                                                 }) => {
    const role = UserStorage.get()?.role | null;
    const prettify = useCallback(
        (k: string) => k.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase()),
        [],
    );

    const formatVal = useCallback((v: unknown) => {
        if (v === null || v === undefined) return '—';
        if (typeof v === 'object') {
            try {
                return JSON.stringify(v, null, 2);
            } catch {
                return String(v);
            }
        }
        return String(v);
    }, []);

    return (
        <div className="flex-1 flex flex-col">
            <div className="flex-1 overflow-auto">
                {loading && (
                    <div className="space-y-4 animate-pulse p-1">
                        {Array.from({ length: 8 }).map((_, i) => (
                            <div key={i} className="h-4 w-2/3 rounded bg-[#EEF3FF]" />
                        ))}
                    </div>
                )}

                {!loading && error && (
                    <div className="text-sm text-red-500 font-medium">{error}</div>
                )}

                {!loading && !error && data && (
                    <div className="space-y-5 pt-2">
                        {Object.entries(data).map(([k, v]) => (
                            <div
                                key={k}
                                className="rounded-xl border border-[#EEF0F6] px-4 py-3 bg-[#FCFCFE] hover:border-[#D9DFF0] transition flex justify-between"
                            >
                                <div>
                                    <div className="text-[11px] uppercase tracking-wide text-[#8F9BBA] font-semibold mb-1">
                                        {prettify(k)}
                                    </div>
                                    <div className="text-sm font-medium text-[#2B3674] whitespace-pre-wrap break-words">
                                        {formatVal(v)}
                                    </div>
                                </div>

                                {role === 'admin' &&
                                    <button
                                    onClick={() => console.log(k)}
                                    className="rounded-full bg-white p-1 my-auto text-[#4B22F4] shadow hover:bg-[#ECECFF]"
                                    title="Редактировать"
                                    >
                                    <Pencil size={16} />
                                    </button>
                                }
                            </div>
                        ))}
                    </div>
                )}

                {!loading && !error && !data && (
                    <div className="text-sm text-[#8F9BBA]">Нет данных</div>
                )}
            </div>

            {/* footer */}
            <div className="pt-4 flex gap-3">
                <button
                    onClick={onBack}
                    className="px-4 py-2 rounded-lg bg-[#F4F7FE] hover:bg-[#EEF3FF] text-[#2B3674] text-sm font-medium"
                >
                    Назад
                </button>
                <button
                    onClick={onRefresh}
                    className="px-4 py-2 rounded-lg bg-[#7144ff] text-white text-sm font-medium hover:opacity-90"
                >
                    Обновить
                </button>
            </div>
        </div>
    );
};
