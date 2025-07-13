'use client';

import {
    BarChart,
    Bar,
    XAxis,
    Tooltip,
    ResponsiveContainer,
    Cell,
} from 'recharts';

const trafficData = [
    { hour: '00', value: 6 },
    { hour: '04', value: 5 },
    { hour: '08', value: 9 },
    { hour: '12', value: 7 },
    { hour: '14', value: 8 },
    { hour: '16', value: 10 },
    { hour: '18', value: 3 },
];

const DailyTrafficCard = () => {
    const total = trafficData.reduce((sum, d) => sum + d.value, 0);
    const delta = 2.45;

    return (
        <div className="bg-white rounded-2xl shadow px-6 py-5 w-full h-full flex flex-col justify-between">
            {/* ── Header ───────────────────────────── */}
            <div className="flex justify-between items-start">
                <div>
                    <p className="text-sm text-[#8F9BBA] font-bold">Дневной трафик</p>
                    <h2 className="text-3xl font-bold text-[#2B3674] leading-tight">{total}</h2>
                    <p className="text-sm text-[#8F9BBA]">новые участники</p>
                </div>
                <span className="text-emerald-500 font-semibold text-sm mt-1">+{delta}%</span>
            </div>

            {/* ── Bar Chart ────────────────────────── */}
            <div className="h-[280px] mt-3">
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={trafficData}>
                        <defs>
                            <linearGradient id="trafficGradient" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="0%" stopColor="#7144ff" />
                                <stop offset="100%" stopColor="#04befe" />
                            </linearGradient>
                        </defs>

                        <XAxis
                            dataKey="hour"
                            axisLine={false}
                            tickLine={false}
                            stroke="#A3AED0"
                            tick={{ fontSize: 14 }}
                        />

                        <Tooltip
                            cursor={{ fill: 'transparent' }}
                            contentStyle={{
                                background: '#4318ff',
                                border: 'none',
                                borderRadius: 8,
                                color: '#fff',
                                padding: '4px 8px',
                                fontSize: 12,
                            }}
                            formatter={(v: number) => [`${v} участн.`, 'Трафик']}
                        />

                        <Bar
                            dataKey="value"
                            radius={[6, 6, 0, 0]}
                            barSize={22}
                            fill="url(#trafficGradient)"
                            isAnimationActive
                        >
                            {trafficData.map((_, index) => (
                                <Cell key={index} />
                            ))}
                        </Bar>
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

export default DailyTrafficCard;
