'use client';

import {
    LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer
} from 'recharts';
import { useState } from 'react';
import PeriodPicker from './PeriodPicker'; // підключення твого компонента

const allData = {
    2024: {
        JAN: { revenue: 105, expenses: 70 },
        FEB: { revenue: 99, expenses: 68 },
        MAR: { revenue: 120, expenses: 72 },
        APR: { revenue: 112, expenses: 69 },
        MAY: { revenue: 130, expenses: 78 },
        JUN: { revenue: 125, expenses: 75 },
        JUL: { revenue: 132, expenses: 80 },
        AUG: { revenue: 128, expenses: 76 },
        SEP: { revenue: 122, expenses: 70 },
        OCT: { revenue: 118, expenses: 68 },
        NOV: { revenue: 135, expenses: 82 },
        DEC: { revenue: 140, expenses: 90 },
    }
};

const IncomeChart = () => {
    const [year, setYear] = useState('2024');

    // 🟪 Масив обʼєднаних даних для графіка
    // @ts-ignore
    const data = Object.entries(allData[year]).map(([month, { revenue, expenses }]) => ({
        name: month,
        revenue,
        expenses,
    }));

    const total = data.reduce((s, d) => s + d.revenue, 0);
    const last = data[data.length - 1].revenue;
    const prev = data[data.length - 2].revenue;
    const delta = +(((last - prev) / prev) * 100).toFixed(2);

    return (
        <div className="bg-white rounded-2xl shadow p-6 w-full h-full">

            {/* Header: заголовок і плашка вибору */}
            <div className="flex justify-between items-center mb-4">
                <div>
                    <h2 className="text-3xl font-bold text-[#2B3674]">${(total / 12).toFixed(2)}k</h2>
                    <div className="text-sm text-[#8F9BBA] flex items-center gap-2">
                        Заработано
                        <span className={delta >= 0 ? 'text-emerald-500' : 'text-red-500'}>
                            {delta >= 0 ? '▲' : '▼'} {Math.abs(delta)}%
                        </span>
                    </div>
                </div>
                <PeriodPicker
                    onChange={({ mode, value }) => {
                        if (mode === 'year') setYear(value);
                    }}
                />
            </div>

            <ResponsiveContainer width="100%" height={240}>
                <LineChart data={data}>
                    <defs>
                        <linearGradient id="rev" x1="0" y1="0" x2="1" y2="0">
                            <stop offset="0%" stopColor="#7144ff" />
                            <stop offset="100%" stopColor="#04befe" />
                        </linearGradient>
                        <linearGradient id="exp" x1="0" y1="0" x2="1" y2="0">
                            <stop offset="0%" stopColor="#a1e0ff" />
                            <stop offset="100%" stopColor="#59d8ff" />
                        </linearGradient>
                    </defs>

                    <XAxis dataKey="name" axisLine={false} tickLine={false} stroke="#A3AED0" tick={{ fontSize: 10 }} />
                    <YAxis hide domain={['dataMin-20', 'dataMax+20']} />

                    <Tooltip
                        cursor={false}
                        contentStyle={{
                            borderRadius: 8,
                            border: 'none',
                            background: '#4318ff',
                            color: '#fff',
                            padding: '4px 8px',
                            fontSize: 12,
                        }}
                        formatter={(v: number) => [`$${v}k`, 'Выручка']}
                    />

                    <Line
                        type="monotone"
                        dataKey="revenue"
                        stroke="url(#rev)"
                        strokeWidth={3}
                        strokeLinecap="round"
                        dot={{ r: 4, stroke: '#fff', strokeWidth: 2, fill: '#7144ff' }}
                        isAnimationActive
                        animationDuration={1200}
                        animationEasing="ease-out"
                    />

                    <Line
                        type="monotone"
                        dataKey="expenses"
                        stroke="url(#exp)"
                        strokeWidth={3}
                        strokeLinecap="round"
                        dot={false}
                        opacity={0.7}
                        isAnimationActive
                        animationDuration={1400}
                        animationEasing="ease-out"
                    />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
};

export default IncomeChart;
