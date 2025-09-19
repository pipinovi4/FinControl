'use client';

import React, { useEffect, useMemo, useState, useRef } from 'react';
import {
    BarChart,
    Bar,
    XAxis,
    Tooltip,
    ResponsiveContainer,
    Cell,
} from 'recharts';
import { ChevronDown, ChevronUp, X } from 'lucide-react';
import UserStorage from '@/services/UserStorage';

/* ───── Types ───── */
type RawRecord = { taken_at_worker?: string; created_at?: string };
type Point = { hour: string; value: number };
type Item = { label: string; data: Point[]; total: number; yesterday: number };

type Props = {
    labels: string[];
    fetchUrls: string[];
    yesterdayUrls: string[];
    requiresId?: boolean;
};

/* ───── Helpers ───── */
function aggregateByHour(records: RawRecord[]): Point[] {
    const map: Record<string, number> = {};
    records.forEach(r => {
        // @ts-ignore
        const getHour = (r: { taken_at_worker?: string; created_at?: string }): number | null => {
            const taken = r?.taken_at_worker ? new Date(r.taken_at_worker) : null;
            const created = r?.created_at ? new Date(r.created_at) : null;

            if (taken && !isNaN(taken.getTime())) return taken.getHours();
            if (created && !isNaN(created.getTime())) return created.getHours();

            return null;
        };
        const hour = getHour(r);

        // @ts-ignore
        const bin = Math.floor(hour / 2) * 2;
        const label = `${bin.toString().padStart(2, '0')}-${(bin + 1).toString().padStart(2, '0')}`;
        map[label] = (map[label] ?? 0) + 1;
    });

    // 24 / 2 = 12 інтервалів
    return Array.from({ length: 12 }, (_, i) => {
        const bin = i * 2;
        const label = `${bin.toString().padStart(2, '0')}-${(bin + 1).toString().padStart(2, '0')}`;
        return { hour: label, value: map[label] ?? 0 };
    });
}

const CustomTooltip: React.FC<any> = ({ active, payload, label }) => {
    if (!active || !payload?.length) return null;
    const val = payload[0].value;
    return (
        <div
            className="rounded-xl px-3 py-2 text-[12px] leading-snug shadow-lg"
            style={{
                background: '#4318ff',
                color: '#ffffff',
                border: 'none',
                fontWeight: 500,
            }}
        >
            <div className="font-semibold">
                Интервал {label}
            </div>
            <div>
                Кол-во : <span className="font-bold text-white">{val}</span>
            </div>
        </div>
    );
};

const BAR_GRADIENT_ID = 'trafficGradient';
const HOVER_GRADIENT_ID = 'trafficGradientHover';

/* ───── Component ───── */
const DailyTrafficCard: React.FC<Props> = ({
                                               labels,
                                               fetchUrls,
                                               yesterdayUrls,
                                               requiresId,
                                           }) => {
    const [items, setItems] = useState<Item[]>([]);
    const [selected, setSelected] = useState(0);
    const [modalOpen, setModalOpen] = useState(false);
    const [loading, setLoading] = useState(false);
    const [hoverIndex, setHoverIndex] = useState<number | null>(null);

    const current = items[selected] ?? { label: '', data: [], total: 0, yesterday: 0 };
    const total = current.total;

    const delta = useMemo(() => {
        const y = current.yesterday;
        if (!y) return total === 0 ? 0 : 100;
        return +(((total - y) / y) * 100).toFixed(2);
    }, [current]);

    const toggleModal = () => setModalOpen(p => !p);

    /* Fetch */
    useEffect(() => {
        const user = requiresId ? UserStorage.get() : null;
        // @ts-ignore
        const id = user?.id;

        setLoading(true);
        (async () => {
            const loaded: Item[] = await Promise.all(
                fetchUrls.map(async (todayUrl, idx) => {
                    let tUrl = todayUrl;
                    let yUrl = yesterdayUrls[idx];

                    if (requiresId && id) {
                        if (!tUrl.endsWith('/')) tUrl += '/';
                        if (!yUrl.endsWith('/')) yUrl += '/';
                        tUrl += id;
                        yUrl += id;
                    }

                    try {
                        const [todayRes, yesterdayRes] = await Promise.all([
                            fetch(tUrl),
                            fetch(yUrl),
                        ]);
                        const todayJson = await todayRes.json();
                        const yesterdayJson = await yesterdayRes.json();

                        const todayRecords: RawRecord[] = Array.isArray(todayJson)
                            ? todayJson
                            : todayJson.value ?? [];

                        const yesterdayCount: number =
                            typeof yesterdayJson === 'number'
                                ? yesterdayJson
                                : yesterdayJson.value ?? 0;

                        return {
                            label: labels[idx],
                            data: aggregateByHour(todayRecords),
                            total: todayRecords.length,
                            yesterday: yesterdayCount,
                        } as Item;
                    } catch (e) {
                        console.error('[DailyTrafficCard] fetch failed', e);
                        return { label: labels[idx], data: [], total: 0, yesterday: 0 } as Item;
                    }
                })
            );

            setItems(loaded);
            setLoading(false);
        })();
    }, [labels, fetchUrls, yesterdayUrls, requiresId]);

    const isEmpty = !loading && total === 0;

    /* Skeleton */
    const Skeleton = () => (
        <div className="flex flex-col justify-between h-full w-full">
            <div className="flex flex-col gap-2">
                <div className="h-3 w-28 rounded bg-[#EEF3FF] animate-pulse" />
                <div className="h-7 w-16 rounded bg-[#EEF3FF] animate-pulse" />
                <div className="h-3 w-32 rounded bg-[#F0F3FA] animate-pulse" />
            </div>
            <div className="flex-1 flex items-end gap-2 mt-4 pb-2">
                {Array.from({ length: 12 }).map((_, i) => (
                    <div
                        key={i}
                        className="flex-1 bg-gradient-to-b from-[#EEF3FF] to-[#F8FAFF] rounded-md animate-pulse h-10"
                    />
                ))}
            </div>
        </div>
    );

    const hoverResetRef = useRef<number | null>(null);

    return (
        <>
            <div className="bg-white rounded-2xl shadow px-6 py-5 w-full h-full flex flex-col relative overflow-hidden transition border border-transparent hover:border-[#E5E9F9] min-h-[420px] sm:min-h-[440px] lg:min-h-[460px]">
                {/* Decorative spot */}
                <div className="pointer-events-none absolute -top-10 -left-10 w-48 h-48 rounded-full bg-[radial-gradient(circle_at_center,rgba(4,190,254,0.15),rgba(255,255,255,0))]" />

                {/* Header */}
                <div className="flex justify-between items-start relative z-10">
                    <div>
                        <p className="text-sm text-[#8F9BBA] font-bold">{labels[selected] ?? 'Дневной трафик'}</p>
                        <h2 className="text-3xl font-bold text-[#2B3674] leading-tight select-none">
                            {loading ? '—' : total}
                        </h2>
                        <p className="text-sm text-[#8F9BBA]">новые участники</p>
                    </div>

                    {/* Delta badge + series picker */}
                    <div className="flex flex-col items-end gap-1">
                        <div className="relative group">
              <span
                  className={`inline-block font-semibold text-sm mt-1 px-2 py-0.5 rounded-full cursor-pointer select-none transition
                ${delta >= 0 ? 'bg-emerald-50 text-emerald-600' : 'bg-red-50 text-red-600'}`}
              >
                {delta >= 0 ? '+' : ''}{delta}%
              </span>

                            <div
                                className="absolute top-[-60px] right-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none
                  bg-[#2B3674] text-white text-xs font-medium px-3 py-1 rounded-lg shadow-md whitespace-nowrap"
                            >
                                {current.yesterday === 0 && total > 0
                                    ? 'Относительно вчера'
                                    : delta >= 0
                                        ? `На ${delta}% больше чем вчера`
                                        : `Меньше на ${Math.abs(delta)}%`}
                            </div>
                        </div>

                        {items.length > 1 && (
                            <button
                                onClick={toggleModal}
                                aria-label="Выбрать серию"
                                className="text-gray-500 hover:text-gray-700 p-1 rounded-lg transition"
                            >
                                {modalOpen ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                            </button>
                        )}
                    </div>
                </div>

                {/* Chart Area */}
                <div className="mt-4 flex-1 relative z-10">
                    {loading ? (
                        <Skeleton />
                    ) : isEmpty ? (
                        <div className="w-full h-full flex flex-col items-center justify-center text-[#8F9BBA]">
                            <div className="w-12 h-12 rounded-full bg-[#F4F7FE] flex items-center justify-center mb-3 text-[#7144ff] font-semibold">
                                –
                            </div>
                            <p className="text-sm font-medium">Нет данных</p>
                        </div>
                    ) : (
                        <div className="h-full">
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart
                                    data={current.data}
                                    margin={{ top: 10, right: 0, left: -10, bottom: 0 }}
                                >
                                    <defs>
                                        <linearGradient id={BAR_GRADIENT_ID} x1="0" y1="0" x2="0" y2="1">
                                            <stop offset="0%" stopColor="#7144ff" />
                                            <stop offset="100%" stopColor="#04befe" />
                                        </linearGradient>
                                        <linearGradient id={HOVER_GRADIENT_ID} x1="0" y1="0" x2="0" y2="1">
                                            <stop offset="0%" stopColor="#8f6bff" />
                                            <stop offset="100%" stopColor="#34cfff" />
                                        </linearGradient>
                                    </defs>

                                    <XAxis
                                        dataKey="hour"
                                        axisLine={false}
                                        tickLine={false}
                                        stroke="#A3AED0"
                                        tick={{ fontSize: 11 }}
                                        interval={0}
                                    />

                                    <Tooltip cursor={false} content={<CustomTooltip />} />

                                    <Bar
                                        dataKey="value"
                                        radius={[6, 6, 0, 0]}
                                        minPointSize={4}
                                        barSize={28}
                                        isAnimationActive
                                        animationDuration={900}
                                        animationEasing="ease-out"
                                    >
                                        {current.data.map((entry, idx) => {
                                            const isHover = hoverIndex === idx;
                                            return (
                                                <Cell
                                                    key={entry.hour}
                                                    className="cursor-pointer transition-transform"
                                                    fill={`url(#${isHover ? HOVER_GRADIENT_ID : BAR_GRADIENT_ID})`}
                                                    onMouseEnter={() => {
                                                        if (hoverResetRef.current) {
                                                            clearTimeout(hoverResetRef.current);
                                                            hoverResetRef.current = null;
                                                        }
                                                        setHoverIndex(idx);
                                                    }}
                                                    onMouseLeave={() => {
                                                        if (hoverResetRef.current) clearTimeout(hoverResetRef.current);
                                                        hoverResetRef.current = window.setTimeout(() => {
                                                            setHoverIndex(null);
                                                            hoverResetRef.current = null;
                                                        }, 150);
                                                    }}
                                                    style={{
                                                        filter: isHover
                                                            ? 'drop-shadow(0 6px 10px rgba(67,24,255,0.35))'
                                                            : 'drop-shadow(0 2px 4px rgba(67,24,255,0.15))',
                                                        transform: isHover ? 'translateY(-4px)' : 'translateY(0)',
                                                        transition: 'all .25s cubic-bezier(.4,0,.2,1)',
                                                    }}
                                                />
                                            );
                                        })}
                                    </Bar>
                                </BarChart>
                            </ResponsiveContainer>

                            {/* Hover mini labels над стовпчиками */}
                            {hoverIndex !== null && current.data[hoverIndex] && (
                                <div className="pointer-events-none absolute inset-0">
                                    {current.data.map((p, idx) => {
                                        if (idx !== hoverIndex) return null;
                                        return (
                                            <div
                                                key={p.hour}
                                                className="absolute flex flex-col items-center text-[10px] font-semibold text-[#2B3674]"
                                                style={{
                                                    left: `calc(${(idx + 0.5) / current.data.length * 100}% - 10px)`,
                                                    top: 0,
                                                    transform: 'translateY(4px)',
                                                }}
                                            >
                        <span className="bg-white/90 backdrop-blur px-2 py-0.5 rounded-full shadow-sm border border-[#E4E9F5]">
                          {p.value}
                        </span>
                                            </div>
                                        );
                                    })}
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </div>

            {/* Modal */}
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
                    className="bg-white w-full max-w-xs rounded-2xl shadow-lg p-6 flex flex-col gap-5 transition-all duration-300 ease-in-out"
                    onClick={e => e.stopPropagation()}
                >
                    <div className="flex justify-between items-center">
            <span className="text-lg font-semibold text-[#2B3674]">
              Выбор серии
            </span>
                        <button
                            onClick={toggleModal}
                            className="text-gray-500 hover:text-gray-700 p-1 rounded-lg transition"
                            aria-label="Закрыть модальное окно"
                        >
                            <X size={18} />
                        </button>
                    </div>

                    <div className="grid grid-cols-1 gap-2 max-h-[320px] overflow-y-auto pr-1">
                        {items.map((it, idx) => (
                            <button
                                key={it.label}
                                onClick={() => {
                                    setSelected(idx);
                                    toggleModal();
                                }}
                                className={`
                  w-full rounded-xl px-4 py-2 flex justify-between items-center text-sm text-[#2B3674]
                  transition-colors cursor-pointer border
                  ${idx === selected
                                    ? 'bg-[#EEF3FF] border-transparent'
                                    : 'bg-[#F8FAFF] hover:bg-[#EEF3FF] border-transparent'}
                `}
                            >
                                <span>{it.label}</span>
                                <span className="font-bold">{it.total}</span>
                            </button>
                        ))}
                    </div>

                    <div className="flex justify-end">
                        <button
                            onClick={toggleModal}
                            className="px-5 py-2 rounded-lg bg-[#7144ff] text-white text-sm font-medium hover:opacity-90 transition"
                        >
                            Готово
                        </button>
                    </div>
                </div>
            </div>
        </>
    );
};

export default DailyTrafficCard;
