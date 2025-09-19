'use client';

/**
 * PromotionsList — scrollable, non-stretching table-like list with actions.
 * ------------------------------------------------------------------------
 * - Keeps its own scroll (parent controls height).
 * - Exposes `scrollRef` so parent can set it as IntersectionObserver's root.
 * - Russian UI.
 */

import React, { Ref } from 'react';
import { Loader2, Trash2 } from 'lucide-react';
import type { PromotionOut } from './CreatePromotionModal';

const TYPE_DOT: Record<PromotionOut['promotion_type'], string> = {
    HELIX: 'bg-[#7144ff]',
    UNION: 'bg-[#4318FF]',
    GENERAL: 'bg-slate-400',
};
const TYPE_LABEL = { HELIX: 'Helix', UNION: 'Union', GENERAL: 'General' };

export default function PromotionsList({
                                           items,
                                           isLoading,
                                           isFetching,
                                           error,
                                           onItemClick,
                                           loadMoreRef,
                                           scrollRef,
                                       }: {
    items: PromotionOut[];
    isLoading: boolean;
    isFetching: boolean;
    error: Error | null;
    onItemClick: (p: PromotionOut) => void;
    loadMoreRef?: Ref<HTMLDivElement>;
    scrollRef?: Ref<HTMLDivElement>;
}) {
    return (
        <div className="flex h-full flex-col rounded-2xl border border-slate-200 bg-white">
            <div className="grid grid-cols-11 px-4 py-3 text-xs font-medium text-slate-500">
                <div className="col-span-2">Тип</div>
                <div className="col-span-6">Описание</div>
                <div className="col-span-1 text-center">Статус</div>
                <div className="col-span-2 text-center">Создано</div>
            </div>

            <div ref={scrollRef} className="custom-scrollbars min-h-0 flex-1 overflow-y-auto divide-y">
                {error && <div className="py-8 text-center text-sm text-red-600">{(error as Error)?.message}</div>}

                {items.map((p) => (
                    <div key={p.id} className="grid grid-cols-11 items-center px-4 py-3 transition hover:bg-indigo-50/50">
                        <button
                            onClick={() => onItemClick(p)}
                            className="col-span-9 grid grid-cols-9 text-left cursor-pointer"
                            title="Открыть"
                        >
                            <div className="col-span-2 flex items-center gap-2">
                                <span className={['h-2.5 w-2.5 rounded-full', TYPE_DOT[p.promotion_type]].join(' ')} />
                                <span className="font-medium text-[#2B3674]">{TYPE_LABEL[p.promotion_type]}</span>
                            </div>
                            <div className="col-span-6 text-sm text-slate-700 line-clamp-2">{p.description?.trim() || '—'}</div>
                            <div className="col-span-1 text-center">
                <span
                    className={[
                        'rounded-full px-2 py-0.5 text-xs',
                        p.is_active ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-slate-600',
                    ].join(' ')}
                >
                  {p.is_active ? '✔' : '—'}
                </span>
                            </div>
                        </button>

                        <div className="col-span-2 text-right text-xs text-slate-500">
                            {new Date(p.created_at).toLocaleDateString()}
                        </div>
                    </div>
                ))}

                {isLoading && (
                    <div className="flex items-center justify-center gap-2 py-8 text-slate-500">
                        <Loader2 className="animate-spin" size={16} /> Загрузка…
                    </div>
                )}

                {!isLoading && !items.length && (
                    <div className="py-10 text-center text-sm text-slate-500">Пока нет промоакций</div>
                )}

                {/* sentinel for IO */}
                <div ref={loadMoreRef} className="h-6 w-full" />
            </div>

            {isFetching && !!items.length && (
                <div className="flex items-center justify-center gap-2 py-2 text-xs text-slate-500">
                    <Loader2 className="animate-spin" size={14} /> Подгружаем…
                </div>
            )}

            <style jsx>{`
                .custom-scrollbars::-webkit-scrollbar {
                    width: 10px;
                }
                .custom-scrollbars::-webkit-scrollbar-thumb {
                    background: rgba(148, 163, 184, 0.6);
                    border-radius: 9999px;
                }
                .custom-scrollbars::-webkit-scrollbar-track {
                    background: transparent;
                }
            `}</style>
        </div>
    );
}
