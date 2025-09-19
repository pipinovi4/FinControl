'use client';

import React, { useEffect, useState } from 'react';
import { ChevronDown, ChevronUp, X } from 'lucide-react';
import UserStorage from '@/services/UserStorage';

/* ──────── types ──────── */
export type StatCardProps = {
    icon: React.ReactElement<React.SVGProps<SVGSVGElement>>;
    /** Список підписів (у тому ж порядку, що й URL-и) */
    labels: string[];
    /** Список endpoint-ів, з яких тягнемо value. К-сть повинна збігатися з `labels`. */
    fetchUrls: string[];
    /** Якщо потрібно підставити user.id у кожен URL */
    requiresId?: boolean;
};

/* ──────── helpers ──────── */
type Item = { label: string; value: string | number };

const parseValue = (raw: any): string | number => {
    if (Array.isArray(raw)) return raw.join(', ');
    if (raw && typeof raw === 'object') return Object.values(raw)[0] as any;
    return raw ?? '-';
};

/* ──────── component ──────── */
const StatCard: React.FC<StatCardProps> = ({ icon, labels, fetchUrls, requiresId }) => {
    const [items, setItems] = useState<Item[]>([]);
    const [selected, setSelected] = useState(0);
    const [modalOpen, setModalOpen] = useState(false);

    const first = items[selected] ?? { label: labels[0] ?? '', value: '-' };
    const multi = items.length > 1;

    const toggleModal = () => setModalOpen((p) => !p);

    /* ——— fetch усіх значень паралельно ——— */
    useEffect(() => {
        if (!labels.length || labels.length !== fetchUrls.length) {
            console.warn('[StatCard] labels & fetchUrls length mismatch');
            return;
        }

        const load = async () => {
            const user = requiresId ? UserStorage.get() : null;
            // @ts-ignore
            const id = user?.id;

            const promises = fetchUrls.map(async (rawUrl, idx) => {
                let url = rawUrl;
                if (requiresId && id) {
                    url = rawUrl.endsWith('/') ? `${rawUrl}${id}` : `${rawUrl}/${id}`;
                }
                try {
                    const res = await fetch(url);
                    const data = await res.json();
                    return { label: labels[idx], value: parseValue(data?.value) } as Item;
                } catch (e) {
                    console.error(`[StatCard] fetch failed for ${url}`, e);
                    return { label: labels[idx], value: '-' } as Item;
                }
            });

            setItems(await Promise.all(promises));
        };

        load();
    }, [labels, fetchUrls, requiresId]);

    return (
        <>
            {/* ─────────── CARD ─────────── */}
            <div className="bg-white rounded-2xl shadow px-6 py-5 flex items-center justify-between gap-4 transition border border-transparent hover:border-[#E5E9F9]">
                <div className="flex items-center gap-4">
                    <div className="w-12 h-12 rounded-full flex items-center justify-center bg-[#F4F7FE]">
                        {icon}
                    </div>
                    <div className="flex flex-col">
                        <span className="text-sm text-[#8F9BBA] font-medium">{first.label}</span>
                        <span className="text-xl font-bold text-[#2B3674]">{first.value}</span>
                    </div>
                </div>

                {multi && (
                    <button
                        onClick={toggleModal}
                        className="text-gray-500 hover:text-gray-700 cursor-pointer"
                        aria-label="Показати деталі"
                    >
                        {modalOpen ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                    </button>
                )}
            </div>

            {/* ─────────── MODAL (із плавною анімацією) ─────────── */}
            <div
                className={`
          fixed inset-0 z-50 flex items-center justify-center
          bg-black/40 backdrop-blur-sm
          transition-all duration-300 ease-out
          ${modalOpen ? 'visible opacity-100' : 'invisible opacity-0'}
        `}
                onClick={toggleModal}
            >
                <div
                    className="bg-white w-full max-w-xs rounded-2xl shadow-lg p-6 flex flex-col gap-4
                     transition-all duration-300 ease-in-out"
                    onClick={(e) => e.stopPropagation()}
                >
                    <div className="flex justify-between items-center">
            <span className="text-lg font-semibold text-[#2B3674]">
              {labels[selected]}
            </span>
                        <button
                            onClick={toggleModal}
                            className="text-gray-500 hover:text-gray-700"
                            aria-label="Закрити"
                        >
                            <X size={18} />
                        </button>
                    </div>

                    <div className="grid grid-cols-1 gap-2">
                        {items.map((it, idx) => (
                            <button
                                key={it.label}
                                onClick={() => {
                                    setSelected(idx);
                                    toggleModal();
                                }}
                                className={`
                  w-full rounded-xl px-4 py-2 flex justify-between text-sm text-[#2B3674]
                  transition-colors cursor-pointer
                  ${idx === selected
                                    ? 'bg-[#EEF3FF]'
                                    : 'bg-[#F8FAFF] hover:bg-[#EEF3FF]'}
                `}
                            >
                                <span>{it.label}</span>
                                <span className="font-bold">{it.value}</span>
                            </button>
                        ))}
                    </div>
                </div>
            </div>
        </>
    );
};

export default StatCard;
