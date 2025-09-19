'use client';

import React, { useState, useEffect } from 'react';
import { Calendar } from 'lucide-react';

type PeriodMode = 'month' | 'year';

type PeriodPickerProps = {
    /** callback наверх */
    onChange: (payload: { mode: PeriodMode; value: string }) => void;
    /** допустимі роки */
    years?: number[];
    /** стартовий режим */
    initialMode?: PeriodMode;
    /** стартове значення (YYYY або YYYY-MM) */
    initialValue?: string;
};

const DEFAULT_YEARS = [2024, 2025, 2026, 2027, 2028];

const MONTHS = [
    { label: 'JAN', value: '01' },
    { label: 'FEB', value: '02' },
    { label: 'MAR', value: '03' },
    { label: 'APR', value: '04' },
    { label: 'MAY', value: '05' },
    { label: 'JUN', value: '06' },
    { label: 'JUL', value: '07' },
    { label: 'AUG', value: '08' },
    { label: 'SEP', value: '09' },
    { label: 'OCT', value: '10' },
    { label: 'NOV', value: '11' },
    { label: 'DEC', value: '12' },
];

const PeriodPicker: React.FC<PeriodPickerProps> = ({
                                                       onChange,
                                                       years = DEFAULT_YEARS,
                                                       initialMode = 'year',
                                                       initialValue,
                                                   }) => {
    const currentYear = new Date().getFullYear();
    const safeInitialYear = years.includes(currentYear) ? currentYear : years[0];

    const [mode, setMode] = useState<PeriodMode>(initialMode);
    const [year, setYear] = useState<number>(
        initialValue && /^\d{4}/.test(initialValue)
            ? Number(initialValue.slice(0, 4))
            : safeInitialYear
    );
    const [month, setMonth] = useState<string>(
        initialValue && /^\d{4}-\d{2}$/.test(initialValue)
            ? initialValue.slice(5, 7)
            : new Date().toISOString().slice(5, 7)
    );
    const [open, setOpen] = useState(false);

    // пушимо початкове значення вгору
    useEffect(() => {
        if (mode === 'year') {
            onChange({ mode, value: `${year}` });
        } else {
            onChange({ mode, value: `${year}-${month}` });
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    const toggleOpen = () => setOpen(o => !o);

    const apply = (newMode: PeriodMode, newYear = year, newMonth = month) => {
        setMode(newMode);
        setYear(newYear);
        setMonth(newMonth);
        const value = newMode === 'year' ? `${newYear}` : `${newYear}-${newMonth}`;
        onChange({ mode: newMode, value });
        setOpen(false);
    };

    return (
        <div className="relative">
            <button
                onClick={toggleOpen}
                className="cursor-pointer flex items-center gap-2 px-3 py-2 text-xs font-semibold rounded-lg bg-[#F4F7FE] hover:bg-[#EEF3FF] transition-colors"
            >
                <Calendar size={16} />
                {mode === 'year'
                    ? `${String(year)}`
                    : `${MONTHS.find(m => m.value === month)?.label} ${year}`}
            </button>

            {open && (
                <div
                    className="absolute right-0 mt-2 w-60 bg-white rounded-xl shadow-lg border border-[#E9EDF7] p-4 z-50"
                >
                    {/* Mode switch */}
                    <div className="flex gap-2 mb-3">
                        <button
                            onClick={() => apply('year', year, month)}
                            className={`cursor-pointer flex-1 py-1.5 rounded-md text-xs font-medium ${
                                mode === 'year' ? 'bg-[#4318ff] text-white' : 'bg-[#F4F7FE] text-[#2B3674] hover:bg-[#EEF3FF]'
                            }`}
                        >
                            Год
                        </button>
                        <button
                            onClick={() => apply('month', year, month)}
                            className={`cursor-pointer flex-1 py-1.5 rounded-md text-xs font-medium ${
                                mode === 'month' ? 'bg-[#4318ff] text-white' : 'bg-[#F4F7FE] text-[#2B3674] hover:bg-[#EEF3FF]'
                            }`}
                        >
                            Месяц
                        </button>
                    </div>

                    {/* Year selector */}
                    <div className="mb-3">
            <span className="block text-[11px] font-semibold text-[#8F9BBA] mb-1">
              Выбери год
            </span>
                        <div className="flex flex-wrap gap-2">
                            {years.map(y => (
                                <button
                                    key={y}
                                    onClick={() => {
                                        setYear(y);
                                        if (mode === 'year') apply('year', y, month);
                                    }}
                                    className={`cursor-pointer px-2 py-1 rounded-md text-xs font-medium border transition-colors ${
                                        y === year
                                            ? 'bg-[#4318ff] text-white border-[#4318ff]'
                                            : 'bg-[#F8FAFF] text-[#2B3674] border-[#E4E9F2] hover:bg-[#EEF3FF]'
                                    }`}
                                >
                                    {y}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Month selector (only when month mode) */}
                    {mode === 'month' && (
                        <div>
              <span className="block text-[11px] font-semibold text-[#8F9BBA] mb-1">
                Выбери месяц
              </span>
                            <div className="grid grid-cols-4 gap-2">
                                {MONTHS.map(m => (
                                    <button
                                        key={m.value}
                                        onClick={() => apply('month', year, m.value)}
                                        className={`cursor-pointer py-1 rounded-md text-[11px] font-medium border transition-colors ${
                                            m.value === month
                                                ? 'bg-[#4318ff] text-white border-[#4318ff]'
                                                : 'bg-[#F8FAFF] text-[#2B3674] border-[#E4E9F2] hover:bg-[#EEF3FF]'
                                        }`}
                                    >
                                        {m.label}
                                    </button>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default PeriodPicker;
