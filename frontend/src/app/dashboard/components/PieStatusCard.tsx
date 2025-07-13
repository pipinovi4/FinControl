'use client';

import {
    PieChart, Pie, Cell, ResponsiveContainer, Tooltip,
} from 'recharts';
import { useState } from 'react';
import { ChevronDown } from 'lucide-react';

type Slice = { name: string; value: number; color: string };

const rawData: Slice[] = [
    { name: 'Закрыто',   value: 63, color: '#7144ff' },
    { name: 'В процессе', value: 25, color: '#45c3ff' },
];

const PieStatusCard = () => {
    const [period] = useState('Месячный');

    /* додаємо "другое", щоб сума = 100 % */
    const sum  = rawData.reduce((s, d) => s + d.value, 0);
    const data = sum < 100
        ? [...rawData, { name: 'Другое', value: 100 - sum, color: '#E4EAF5' }]
        : rawData;

    return (
        <div className="bg-white rounded-2xl shadow px-6 pt-6 pb-8 w-full h-full flex flex-col">
            {/* header */}
            <div className="flex justify-between items-start mb-4">
                <h2 className="text-xl font-bold text-[#2B3674] leading-tight">
                    Ваша диаграмма
                </h2>
                <button className="flex items-center gap-1 text-sm text-[#8F9BBA] hover:text-primary">
                    {period}
                    <ChevronDown className="w-4 h-4" />
                </button>
            </div>

            {/* pie chart: займає увесь "вільний" простір по висоті */}
            <div className="flex-1">
                <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                        <Tooltip
                            cursor={{ fill: 'transparent' }}
                            contentStyle={{
                                background: '#4318ff',
                                border: 'none',
                                borderRadius: 8,
                                color: '#ffffff',
                                padding: '4px 8px',
                                fontSize: 12,
                            }}
                            formatter={(v:number, n)=>[`${v}%`, n]}
                        />
                        <Pie
                            data={data}
                            dataKey="value"
                            innerRadius="55%"
                            outerRadius="80%"
                            startAngle={90}
                            endAngle={-270}
                            stroke="none"
                        >
                            {data.map(s => (
                                <Cell key={s.name} fill={s.color}/>
                            ))}
                        </Pie>
                    </PieChart>
                </ResponsiveContainer>
            </div>

            {/* legend */}
            <div className="mt-6 mx-auto max-w-[300px] flex justify-around items-center bg-[#F6F8FD] rounded-xl py-4">
                {rawData.map(s => (
                    <div key={s.name} className="flex flex-col items-center gap-1">
                        <div className="flex items-center gap-2">
                            <span style={{ background: s.color }} className="inline-block w-2.5 h-2.5 rounded-full" />
                            <span className="text-sm text-[#8F9BBA]">{s.name}</span>
                        </div>
                        <span className="text-xl font-bold text-[#2B3674]">{s.value}%</span>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default PieStatusCard;
