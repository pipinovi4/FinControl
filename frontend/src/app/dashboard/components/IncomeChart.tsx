'use client';

import React, { useEffect, useMemo, useState, useRef } from 'react';
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer,
    Area,
    ReferenceLine
} from 'recharts';
import { ChevronDown, ChevronUp, X, Download, RefreshCw } from 'lucide-react';
import UserStorage from '@/services/UserStorage';
import PeriodPicker from './PeriodPicker';

/* ---------- Types ---------- */
type DayPoint = { date: string; amount: number };
type MonthPoint = { month: string; amount: number };
type SeriesPoint = { name: string; value: number };
type SeriesItem = {
    label: string;
    data: SeriesPoint[];
    total: number;
};

type Props = {
    labels: string[];
    monthUrls: string[];
    yearUrls: string[];
    requiresId?: boolean;
};

const MONTH_ABBR_MAP: Record<string, string> = {
    JAN: '01', FEB: '02', MAR: '03', APR: '04', MAY: '05', JUN: '06',
    JUL: '07', AUG: '08', SEP: '09', OCT: '10', NOV: '11', DEC: '12',
};

const ALLOWED_YEARS = [2024, 2025, 2026, 2027, 2028];

/* ---------- Helpers ---------- */
function normalizePicked(mode: 'month' | 'year', raw: string): string {
    if (mode === 'year') {
        if (/^\d{4}$/.test(raw)) return raw;
        const maybeYear = raw.slice(0, 4);
        return /^\d{4}$/.test(maybeYear) ? maybeYear : new Date().getFullYear().toString();
    }
    if (/^\d{4}-\d{2}$/.test(raw)) return raw;
    if (/^\d{4}-[A-Z]{3}$/.test(raw)) {
        const [y, abbr] = raw.split('-');
        return `${y}-${MONTH_ABBR_MAP[abbr.toUpperCase()] ?? '01'}`;
    }
    if (/^[A-Z]{3}-\d{4}$/.test(raw)) {
        const [abbr, y] = raw.split('-');
        return `${y}-${MONTH_ABBR_MAP[abbr.toUpperCase()] ?? '01'}`;
    }
    if (/^[A-Z]{3}$/.test(raw)) {
        const year = new Date().getFullYear().toString();
        return `${year}-${MONTH_ABBR_MAP[raw.toUpperCase()] ?? '01'}`;
    }
    const now = new Date();
    return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
}

function formatCompact(n: number): string {
    if (n === 0) return '0';
    if (Math.abs(n) >= 1_000_000_000) return (n / 1_000_000_000).toFixed(2) + 'B';
    if (Math.abs(n) >= 1_000_000) return (n / 1_000_000).toFixed(2) + 'M';
    if (Math.abs(n) >= 1_000) return (n / 1_000).toFixed(2) + 'k';
    return n.toFixed(2);
}

/* ---------- Skeleton ---------- */
const Skeleton: React.FC = () => (
    <div className="flex flex-col h-full w-full animate-pulse gap-4">
        <div className="h-6 w-32 rounded bg-[#EEF3FF]" />
        <div className="flex-1 relative">
            <div className="absolute inset-0 bg-gradient-to-br from-[#F6F8FD] to-[#ffffff] rounded-xl" />
            <div className="absolute left-6 right-6 top-6 h-40 rounded bg-[#EEF3FF]" />
            <div className="absolute left-10 right-10 bottom-10 h-3 rounded bg-[#EEF3FF]" />
        </div>
    </div>
);

/* ---------- Main Component ---------- */
const IncomeChart: React.FC<Props> = ({
                                          labels,
                                          monthUrls,
                                          yearUrls,
                                          requiresId=false,
                                      }) => {
    const [periodMode, setPeriodMode] = useState<'month' | 'year'>('year');
    const [pickedValue, setPickedValue] = useState<string>(new Date().getFullYear().toString());
    const [series, setSeries] = useState<SeriesItem[]>([]);
    const [selected, setSelected] = useState(0);
    const [modalOpen, setModalOpen] = useState(false);
    const [loading, setLoading] = useState(false);
    const [focusIndex, setFocusIndex] = useState<number | null>(null);
    const [metricTab, setMetricTab] = useState<'total' | 'avg' | 'delta'>('total');
    const fadeRef = useRef<HTMLDivElement | null>(null);

    const toggleModal = () => setModalOpen(p => !p);

    const current = series[selected] ?? { label: '', data: [], total: 0 };
    const total = current.total;

    const average = useMemo(
        () => current.data.length ? total / current.data.length : 0,
        [current, total]
    );

    const delta = useMemo(() => {
        const arr = current.data;
        if (arr.length < 2) return 0;
        const last = arr[arr.length - 1].value;
        const prev = arr[arr.length - 2].value || 1;
        if (prev === 0) return last > 0 ? 100 : 0;
        return +(((last - prev) / prev) * 100).toFixed(2);
    }, [current]);

    const buildMonthSeries = (raw: DayPoint[]): SeriesPoint[] =>
        raw.map(r => ({
            name: r.date?.slice(-2) ?? '',
            value: Number(r.amount) || 0,
        }));

    const buildYearSeries = (raw: MonthPoint[]): SeriesPoint[] =>
        raw.map(r => ({
            name: r.month,
            value: Number(r.amount) || 0,
        }));

    /* Fetch */
    useEffect(() => {
        const user = requiresId ? UserStorage.get() : null;
        // @ts-ignore
        const id = user?.id;
        const urls = periodMode === 'month' ? monthUrls : yearUrls;
        if (!urls.length || !labels.length) return;

        setLoading(true);
        (async () => {
            const loaded: SeriesItem[] = await Promise.all(
                urls.map(async (baseUrl, idx) => {
                    let url = baseUrl;
                    if (requiresId && id) {
                        if (!url.endsWith('/')) url += '/';
                        url += id;
                    }
                    const paramKey = periodMode === 'month' ? 'month' : 'year';
                    const normalized = normalizePicked(periodMode, pickedValue);
                    const qp = new URLSearchParams({ [paramKey]: normalized }).toString();
                    url += `?${qp}`;

                    try {
                        const res = await fetch(url);
                        if (!res.ok) throw new Error(await res.text());
                        const json = await res.json();

                        let raw: any[] = [];
                        if (Array.isArray(json)) raw = json;
                        else if (Array.isArray(json.items)) raw = json.items;
                        else raw = json.value ?? [];

                        const points =
                            periodMode === 'month'
                                ? buildMonthSeries(raw as DayPoint[])
                                : buildYearSeries(raw as MonthPoint[]);

                        const total = points.reduce((s, p) => s + p.value, 0);
                        return { label: labels[idx], data: points, total } as SeriesItem;
                    } catch (e) {
                        console.error('[IncomeChart] fetch failed for', url, e);
                        return { label: labels[idx], data: [], total: 0 } as SeriesItem;
                    }
                })
            );
            setSeries(loaded);
            setSelected(0);
            setFocusIndex(null);
            setLoading(false);

            // fade animation trigger
            if (fadeRef.current) {
                fadeRef.current.classList.remove('opacity-0');
                void fadeRef.current.offsetWidth;
                fadeRef.current.classList.add('opacity-100');
            }
        })();
    }, [labels, monthUrls, yearUrls, periodMode, pickedValue, requiresId]);

    const yearTickFormatter = (value: string) =>
        value.split('-').pop() ?? value;

    const shownValue = useMemo(
        () => normalizePicked(periodMode, pickedValue),
        [periodMode, pickedValue]
    );

    const isEmptySeries = useMemo(
        () =>
            current.data.length === 0 ||
            current.data.every(p => p.value === 0),
        [current]
    );

    const metricValue = (() => {
        switch (metricTab) {
            case 'avg':
                return formatCompact(average) + '$';
            case 'delta':
                return `${delta >= 0 ? '+' : ''}${delta}%`;
            default:
                return formatCompact(total) + '₽ ';
        }
    })();

    const metricSubtitle = {
        total: periodMode === 'month' ? `Месяц: ${shownValue}` : `Год: ${shownValue}`,
        avg: 'Среднее за точки',
        delta: 'Δ останні дві точки'
    }[metricTab];

    const onReset = () => {
        setMetricTab('total');
        setFocusIndex(null);
    };

    /* Filter ticks (не захаращує 30+ днів) */
    const ticks = useMemo(() => {
        if (current.data.length <= 20) return current.data.map(p => p.name);
        return current.data
            .filter((_, i) => i % 2 === 0)
            .map(p => p.name);
    }, [current.data]);

    /* Custom tooltip */
    const CustomTooltip = ({ active, payload, label }: any) => {
        if (!active || !payload || !payload.length) return null;
        const v = payload[0].value;
        return (
            <div className="px-3 py-2 rounded-lg shadow-md bg-[#4318ff] text-white text-xs font-medium">
                <div className="mb-0.5">
                    {periodMode === 'year' ? label : `День ${label}`}
                </div>
                <div className="font-semibold text-sm">${v}</div>
            </div>
        );
    };

    /* Export mock */
    const exportCSV = () => {
        const rows = [['name', 'value'], ...current.data.map(d => [d.name, d.value])];
        const csv = rows.map(r => r.join(',')).join('\n');
        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `income_${periodMode}_${shownValue}.csv`;
        a.click();
        URL.revokeObjectURL(url);
    };

    return (
        <>
            <div
                className="relative bg-white rounded-2xl shadow p-8 w-full h-full flex flex-col border border-transparent hover:border-[#E5E9F6] min-h-[420px] sm:min-h-[440px] lg:min-h-[460px] overflow-hidden"
            >
                {/* decorative spotlight */}
                <div className="pointer-events-none absolute -top-16 -left-10 w-64 h-64 bg-[radial-gradient(circle_at_center,rgba(113,68,255,0.12),rgba(255,255,255,0))]" />

                {/* Header */}
                <div className="flex justify-between items-start mb-6 relative z-10">
                    <div className="space-y-1">
                        <div className="text-sm text-[#8F9BBA] font-bold">
                            {current.label || (labels[0] ?? 'Заработано')}
                        </div>

                        <div className="flex items-center gap-4 flex-wrap">
                            {/* Tabs */}
                            <div className="flex items-center gap-1 bg-[#F4F7FE] rounded-xl p-1">
                                {([
                                    { key: 'total', label: 'Всего' },
                                    { key: 'avg', label: 'В среднем' },
                                ] as const).map(t => (
                                    <button
                                        key={t.key}
                                        onClick={() => setMetricTab(t.key)}
                                        className={`px-3 py-1 rounded-lg text-xs font-medium transition ${
                                            metricTab === t.key
                                                ? 'bg-white shadow text-[#2B3674]'
                                                : 'text-[#6A7691] hover:text-[#2B3674]'
                                        }`}
                                    >
                                        {t.label}
                                    </button>
                                ))}
                            </div>

                            <div className="flex items-baseline gap-2">
                                <h2
                                    className={`text-3xl font-bold tracking-tight text-[#2B3674] ${
                                        metricTab === 'delta'
                                            ? delta >= 0
                                                ? 'text-emerald-500'
                                                : 'text-red-500'
                                            : ''
                                    }`}
                                >
                                    {metricValue}
                                </h2>
                            </div>
                        </div>

                        <div className="text-[11px] text-[#A3AED0]">
                            {metricSubtitle}
                        </div>
                    </div>

                    <div className="flex items-start gap-2">
                        <button
                            onClick={exportCSV}
                            className="cursor-pointer p-2 rounded-lg bg-[#F4F7FE] hover:bg-[#EEF3FF] text-[#2B3674] transition"
                            title="Экспорт CSV"
                        >
                            <Download size={16} />
                        </button>
                        {series.length > 1 && (
                            <button
                                onClick={toggleModal}
                                className="p-2 rounded-lg bg-[#F4F7FE] hover:bg-[#EEF3FF] text-[#2B3674] transition"
                                title="Выбор серии"
                            >
                                {modalOpen ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
                            </button>
                        )}
                        <PeriodPicker
                            years={ALLOWED_YEARS}
                            onChange={({ mode, value }) => {
                                setPeriodMode(mode as 'month' | 'year');
                                setPickedValue(value);
                            }}
                        />
                    </div>
                </div>

                {/* Chart / Empty */}
                <div ref={fadeRef} className="flex-1 opacity-100 transition-opacity duration-400">
                    {loading ? (
                        <Skeleton />
                    ) : isEmptySeries ? (
                        <div className="w-full h-full flex flex-col items-center justify-center text-[#8F9BBA] gap-3">
                            <div className="w-12 h-12 rounded-xl bg-[#F4F7FE] flex items-center justify-center text-[#7144ff] text-xl font-bold">
                                ∅
                            </div>
                            <p className="text-sm font-medium">Нет данных за период</p>
                            <button
                                onClick={onReset}
                                className="inline-flex items-center gap-1 text-xs px-3 py-1.5 rounded-lg bg-[#EEF3FF] hover:bg-[#E0E8FF] text-[#2B3674] font-medium transition"
                            >
                                <RefreshCw size={12} /> Сбросить
                            </button>
                        </div>
                    ) : (
                        <ResponsiveContainer width="100%" height={260}>
                            <LineChart
                                data={current.data}
                                onMouseLeave={() => setFocusIndex(null)}
                            >
                                <defs>
                                    <linearGradient id="incomeLine" x1="0" y1="0" x2="1" y2="0">
                                        <stop offset="0%" stopColor="#7144ff" />
                                        <stop offset="100%" stopColor="#04befe" />
                                    </linearGradient>
                                    <linearGradient id="incomeFill" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#7144ff" stopOpacity={0.28} />
                                        <stop offset="50%" stopColor="#5b6bff" stopOpacity={0.10} />
                                        <stop offset="100%" stopColor="#ffffff" stopOpacity={0} />
                                    </linearGradient>
                                    <filter id="glow">
                                        <feGaussianBlur stdDeviation="3.5" result="coloredBlur" />
                                        <feMerge>
                                            <feMergeNode in="coloredBlur" />
                                            <feMergeNode in="SourceGraphic" />
                                        </feMerge>
                                    </filter>
                                </defs>

                                {/* baseline grid */}
                                <ReferenceLine y={0} stroke="#ECEFF7" strokeDasharray="3 6" />

                                <XAxis
                                    dataKey="name"
                                    ticks={ticks}
                                    axisLine={false}
                                    tickLine={false}
                                    stroke="#A3AED0"
                                    tick={{ fontSize: 11 }}
                                    interval={0}
                                    padding={{ left: 20, right: 20 }}
                                    tickFormatter={periodMode === 'year' ? yearTickFormatter : undefined}
                                />
                                <YAxis hide domain={['dataMin-10', 'dataMax+10']} />

                                <Tooltip
                                    cursor={{
                                        stroke: '#CCD5EE',
                                        strokeWidth: 1,
                                        strokeDasharray: '4 4'
                                    }}
                                    content={<CustomTooltip />}
                                />

                                <Area
                                    type="monotone"
                                    dataKey="value"
                                    stroke="none"
                                    fill="url(#incomeFill)"
                                    isAnimationActive
                                    animationDuration={1000}
                                />

                                <Line
                                    type="monotone"
                                    dataKey="value"
                                    stroke="url(#incomeLine)"
                                    strokeWidth={3}
                                    strokeLinecap="round"
                                    dot={(p: any) => {
                                        const active = focusIndex === p.index;
                                        return (
                                            <circle
                                                key={p.payload?.name ?? p.index}
                                                cx={p.cx}
                                                cy={p.cy}
                                                r={active ? 6 : 4}
                                                stroke="#fff"
                                                strokeWidth={2}
                                                fill="#7144ff"
                                                style={{
                                                    transition: 'r .25s'
                                                }}
                                                onMouseEnter={() => setFocusIndex(p.index)}
                                            />
                                        );
                                    }}
                                    activeDot={false}
                                    isAnimationActive
                                    animationDuration={1100}
                                    animationEasing="ease-out"
                                    filter="url(#glow)"
                                />
                            </LineChart>
                        </ResponsiveContainer>
                    )}
                </div>
            </div>

            {/* Modal choose series */}
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
                    className="bg-white w-full max-w-xs rounded-2xl shadow-lg p-6 flex flex-col gap-4 transition-all duration-300 ease-in-out"
                    onClick={e => e.stopPropagation()}
                >
                    <div className="flex justify-between items-center">
                        <span className="text-lg font-semibold text-[#2B3674]">Серії</span>
                        <button
                            onClick={toggleModal}
                            className="text-gray-500 hover:text-gray-700"
                        >
                            <X size={18} />
                        </button>
                    </div>

                    <div className="grid grid-cols-1 gap-2">
                        {series.map((it, idx) => (
                            <button
                                key={it.label}
                                onClick={() => {
                                    setSelected(idx);
                                    toggleModal();
                                }}
                                className={`
                    w-full rounded-xl px-4 py-2 flex justify-between items-center text-sm
                    transition-colors cursor-pointer border
                    ${
                                    idx === selected
                                        ? 'bg-[#EEF3FF] border-transparent'
                                        : 'bg-[#F8FAFF] border-transparent hover:bg-[#EEF3FF]'
                                }
                  `}
                            >
                                <span className="text-[#2B3674]">{it.label}</span>
                                <span className="font-bold text-[#2B3674]">
                    {formatCompact(it.total)}$
                  </span>
                            </button>
                        ))}
                    </div>
                </div>
            </div>
        </>
    );
};

export default IncomeChart;
