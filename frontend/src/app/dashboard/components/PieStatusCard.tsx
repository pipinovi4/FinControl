'use client';

import React, { useEffect, useState, useMemo } from 'react';
import {
    PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Sector
} from 'recharts';
import UserStorage from '@/services/UserStorage';

type Props = {
    labels: string[];
    labelsActive: string[];
    labelsCompleted: string[];
    activeUrls: string[];
    completedUrls: string[];
    requiresId?: boolean;
};

type FetchedPair = { active: number; completed: number };

const COLORS = {
    active: '#45c3ff',
    completed: '#7144ff',
};

const GRADIENTS = {
    active: { from: '#45c3ff', to: '#7dd9ff' },
    completed: { from: '#7144ff', to: '#9d6bff' },
};

const PieStatusCard: React.FC<Props> = ({
                                            labels,
                                            labelsActive,
                                            labelsCompleted,
                                            activeUrls,
                                            completedUrls,
                                            requiresId
                                        }) => {
    const [dataRaw, setDataRaw] = useState<FetchedPair>({ active: 0, completed: 0 });
    const [loading, setLoading] = useState(false);
    const [hoverKey, setHoverKey] = useState<string | null>(null);
    const [lockedKey, setLockedKey] = useState<string | null>(null); // для фіксації по кліку

    const title = labels[0] ?? 'Статус';
    const activeLabel = labelsActive[0] ?? 'Active';
    const completedLabel = labelsCompleted[0] ?? 'Completed';

    /* ---------- fetch ---------- */
    useEffect(() => {
        const user = requiresId ? UserStorage.get() : null;
        // @ts-ignore
        const id = user?.id;

        const activeUrl = activeUrls[0];
        const completedUrl = completedUrls[0];
        if (!activeUrl || !completedUrl) return;

        setLoading(true);
        (async () => {
            try {
                const makeUrl = (base: string) =>
                    requiresId && id
                        ? base.endsWith('/') ? base + id : `${base}/${id}`
                        : base;

                const finalActive = makeUrl(activeUrl);
                const finalCompleted = makeUrl(completedUrl);

                const [ra, rc] = await Promise.all([
                    fetch(finalActive).then(r => r.json()).catch(() => ({})),
                    fetch(finalCompleted).then(r => r.json()).catch(() => ({})),
                ]);

                const aVal = (ra.value ?? ra.count ?? 0) as number;
                const cVal = (rc.value ?? rc.count ?? 0) as number;

                setDataRaw({ active: aVal, completed: cVal });
            } catch (e) {
                console.error('[PieStatusCard] fetch error', e);
                setDataRaw({ active: 0, completed: 0 });
            } finally {
                setLoading(false);
            }
        })();
    }, [activeUrls, completedUrls, requiresId]);

    /* ---------- derived ---------- */
    const total = dataRaw.active + dataRaw.completed;

    const pieData = useMemo(() => {
        if (total === 0) return [];
        return [
            { name: activeLabel, key: 'active', value: dataRaw.active, color: COLORS.active, grad: GRADIENTS.active },
            { name: completedLabel, key: 'completed', value: dataRaw.completed, color: COLORS.completed, grad: GRADIENTS.completed },
        ];
    }, [dataRaw, activeLabel, completedLabel, total]);

    const percentNum = (val: number) =>
        total === 0 ? 0 : (val / total) * 100;

    const percent = (val: number) =>
        total === 0 ? '0%' : percentNum(val).toFixed(0) + '%';

    const labelForSlice = (val: number) => {
        if (total === 0) return '0%';
        const p = percentNum(val);
        return p < 3 && p > 0 ? '<3%' : p.toFixed(0) + '%';
    };

    const isEmpty = total === 0;

    const handleSliceEnter = (key: string) => {
        if (!lockedKey) setHoverKey(key);
    };
    const handleSliceLeave = () => {
        if (!lockedKey) setHoverKey(null);
    };
    const toggleLock = (key: string) => {
        setLockedKey(prev => prev === key ? null : key);
        setHoverKey(null);
    };

    /* ---------- skeleton ---------- */
    const Skeleton = () => (
        <div className="flex flex-col items-center justify-center h-full gap-4 animate-pulse">
            <div className="w-24 h-24 rounded-full bg-gradient-to-br from-[#EEF3FF] to-[#F8FAFF]" />
            <div className="h-3 w-32 rounded bg-[#EEF3FF]" />
            <div className="h-3 w-20 rounded bg-[#F0F3FA]" />
        </div>
    );

    return (
        <div className="relative flex min-h-[420px] sm:min-h-[440px] lg:min-h-[460px] flex-col rounded-[calc(theme(borderRadius.3xl)-1px)] bg-white/90 p-6 shadow-xl backdrop-blur border border-transparent hover:border-[#E5E9F6] overflow-hidden">
            <div className="pointer-events-none absolute -top-8 -right-8 w-40 h-40 rounded-full bg-[radial-gradient(circle_at_center,rgba(113,68,255,0.15),rgba(255,255,255,0))]" />

            <div className="flex justify-between items-start mb-4 relative z-10">
                <h2 className="text-lg font-extrabold text-[#2B3674] tracking-tight">
                    {title}
                </h2>
            </div>

            <div className="flex-1 relative z-10 select-none">
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
                    <div className="relative h-full">
                        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                            <div className="flex flex-col items-center">
                <span className="text-xs tracking-wide text-[#8F9BBA] uppercase font-semibold">
                  Всего
                </span>
                                <span className="text-2xl font-bold text-[#2B3674] leading-snug">
                  {total}
                </span>
                            </div>
                        </div>

                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <defs>
                                    {pieData.map(s => (
                                        <linearGradient key={s.key} id={`grad-${s.key}`} x1="0" y1="0" x2="1" y2="1">
                                            <stop offset="0%" stopColor={s.grad.from} />
                                            <stop offset="100%" stopColor={s.grad.to} />
                                        </linearGradient>
                                    ))}
                                </defs>

                                <Tooltip
                                    cursor={{ fill: 'transparent' }}
                                    contentStyle={{
                                        background: '#ffffff',
                                        border: '1px solid #E2E8F4',
                                        borderRadius: 12,
                                        color: '#2B3674',
                                        padding: '6px 10px',
                                        fontSize: 12,
                                        boxShadow: '0 6px 18px rgba(67,24,255,0.15)'
                                    }}
                                    labelStyle={{ color: '#8F9BBA' }}
                                />

                                <Pie
                                    data={pieData}
                                    dataKey="value"
                                    nameKey="name"
                                    innerRadius="56%"
                                    outerRadius="82%"
                                    startAngle={90}
                                    endAngle={-270}
                                    stroke="none"
                                    paddingAngle={1.5}
                                    onMouseLeave={handleSliceLeave}
                                    labelLine={false}
                                >
                                    {pieData.map(s => {
                                        const isHover = (hoverKey === s.key) || (lockedKey === s.key);
                                        return (
                                            <Cell
                                                key={s.key}
                                                fill={`url(#grad-${s.key})`}
                                                className="cursor-pointer"
                                                onMouseEnter={() => handleSliceEnter(s.key)}
                                                onClick={() => toggleLock(s.key)}
                                                style={{
                                                    filter: isHover
                                                        ? 'drop-shadow(0 4px 8px rgba(0,0,0,0.25))'
                                                        : 'drop-shadow(0 2px 4px rgba(0,0,0,0.12))',
                                                    transition: 'filter .25s ease, transform .25s ease',
                                                    transform: isHover ? 'scale(1.015)' : 'scale(1)'
                                                }}
                                            />
                                        );
                                    })}
                                </Pie>
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                )}
            </div>

            {!isEmpty && !loading && (
                <div className="mt-6 mx-auto w-full max-w-[320px] flex flex-col gap-4">
                    <div className="flex justify-around items-stretch bg-[#F6F8FD] rounded-xl py-4 px-3">
                        {pieData.map(s => {
                            const pct = percentNum(s.value);
                            const hover = (hoverKey === s.key) || (lockedKey === s.key);
                            return (
                                <div
                                    key={s.key}
                                    className={`flex flex-col items-center gap-1 min-w-[90px] transition ${
                                        hover ? 'scale-[1.04]' : ''
                                    } cursor-pointer`}
                                    onMouseEnter={() => handleSliceEnter(s.key)}
                                    onMouseLeave={handleSliceLeave}
                                    onClick={() => toggleLock(s.key)}
                                >
                                    <div className="flex items-center gap-1">
                    <span
                        className="inline-block w-2.5 h-2.5 rounded-full"
                        style={{ background: s.color }}
                    />
                                        <span className="text-[11px] text-[#2B3674] font-medium">
                      {s.name}
                    </span>
                                    </div>
                                    <span className="text-xl font-bold text-[#2B3674] leading-none">
                    {percent(s.value)}
                  </span>
                                    <span className="text-[10px] text-[#A3AED0]">
                    {s.value} из {total}
                  </span>

                                    <div className="w-full h-1.5 rounded-full bg-white/70 mt-1 overflow-hidden">
                                        <div
                                            className="h-full rounded-full transition-all"
                                            style={{
                                                width: `${pct}%`,
                                                background: s.color,
                                                opacity: 0.9
                                            }}
                                        />
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </div>
            )}
        </div>
    );
};

export default PieStatusCard;
