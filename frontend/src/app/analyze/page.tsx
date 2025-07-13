'use client';

import React, { useState } from 'react';
import {
    BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer
} from 'recharts';
import { format } from 'date-fns';
import { cn } from "@/lib/utils"
import {
    Input,
    Button,
    Calendar,
    Popover,
    PopoverTrigger,
    PopoverContent,
} from './components';           // ← свій barrel-index

/* ---------------- MOCK ---------------- */
const mockData = [
    { name: '01.06', income: 320 },
    { name: '02.06', income: 580 },
    { name: '03.06', income: 430 },
    { name: '04.06', income: 200 },
    { name: '05.06', income: 650 },
    { name: '06.06', income: 390 },
    { name: '07.06', income: 720 },
];

/* ---------------- PAGE ---------------- */
export default function AnalyzePage() {
    const [startOpen, setStartOpen] = useState(false);
    const [endOpen, setEndOpen]     = useState(false);

    const [startDate, setStartDate] = useState<Date>();
    const [endDate, setEndDate]     = useState<Date>();
    const [clientFilter, setClient] = useState('');
    const [minIncome, setMin]       = useState('');

    return (
        <div className="md:ml-60 p-6 min-h-screen font-[var(--font-dm-sans)] bg-[#F8FAFF]">
            <h1 className="text-2xl font-bold text-[#2B3674] mb-6">Аналітика</h1>

            {/* ─── filters ───────────────────────── */}
            <div className="grid gap-4 md:grid-cols-[repeat(4,minmax(0,210px))] mb-6">
                {/* from */}
                <Popover open={startOpen} onOpenChange={setStartOpen}>
                    <PopoverTrigger>
                        <Button variant="outline" className="w-full justify-start">
                            {startDate ? format(startDate, 'dd.MM.yyyy') : 'Дата початку'}
                        </Button>
                    </PopoverTrigger>
                    <PopoverContent align="start" className="p-0">
                        <Calendar
                            selected={startDate}
                            onSelect={(d) => {
                                setStartDate(d);
                                setStartOpen(false);
                            }}
                        />
                    </PopoverContent>
                </Popover>

                {/* to */}
                <Popover open={endOpen} onOpenChange={setEndOpen}>
                    <PopoverTrigger asChild>
                        <Button variant="outline">Выбрать дату</Button>
                    </PopoverTrigger>
                    <PopoverContent align="start" className="p-0">
                        <Calendar
                            selected={endDate}
                            onSelect={(d) => {
                                setEndDate(d);
                                setEndOpen(false);
                            }}
                        />
                    </PopoverContent>
                </Popover>

                <Input
                    placeholder="Фільтр по клієнту"
                    value={clientFilter}
                    onChange={(e) => setClient(e.target.value)}
                />
                <Input
                    placeholder="Мін. прибуток"
                    value={minIncome}
                    onChange={(e) => setMin(e.target.value)}
                    type="number"
                />
            </div>

            {/* ─── chart ─────────────────────────── */}
            <div className="bg-white shadow rounded-2xl p-6 mb-6">
                <h2 className="text-lg font-semibold mb-4">Прибуток за дні</h2>

                <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={mockData}>
                        <defs>
                            <linearGradient id="barGrad" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="0%" stopColor="#4B22F4" />
                                <stop offset="100%" stopColor="#04befe" />
                            </linearGradient>
                        </defs>

                        <XAxis dataKey="name" stroke="#A3AED0" tick={{ fontSize: 12 }} />
                        <YAxis tick={{ fontSize: 12 }} />

                        <Tooltip
                            cursor={{ fill: 'transparent' }}
                            contentStyle={{
                                background: '#4318ff',
                                color: '#fff',
                                borderRadius: 8,
                                border: 'none',
                                fontSize: 12,
                                padding: '6px 8px',
                            }}
                            formatter={(v: number) => [`$${v}`, 'Прибуток']}
                        />

                        <Bar dataKey="income" fill="url(#barGrad)" radius={[4, 4, 0, 0]} />
                    </BarChart>
                </ResponsiveContainer>
            </div>

            {/* ─── stats ─────────────────────────── */}
            <div className="grid gap-6 lg:grid-cols-3">
                {[
                    { label: 'Загальна кількість клієнтів', val: 157 },
                    { label: 'Заявок сьогодні', val: 14 },
                    { label: 'Несплачені клієнти', val: 42, red: true },
                ].map(({ label, val, red }) => (
                    <div key={label} className="bg-white shadow rounded-2xl p-6">
                        <h3 className="text-lg font-semibold mb-2">{label}</h3>
                        <p className={cn('text-3xl font-bold', red ? 'text-red-500' : 'text-[#2B3674]')}>
                            {val}
                        </p>
                    </div>
                ))}
            </div>
        </div>
    );
}
