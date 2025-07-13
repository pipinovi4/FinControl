'use client';

import { useState } from 'react';
import { Calendar } from 'lucide-react';          // npm i lucide-react
import clsx from 'clsx';                          // npm i clsx

const months = [
    'JAN','FEB','MAR','APR','MAY','JUN',
    'JUL','AUG','SEP','OCT','NOV','DEC'
];
const years  = ['2022','2023','2024','2025'];

export default function PeriodPicker({
                                         onChange,
                                     }: { onChange?: (payload:{ mode:'month'|'year', value:string }) => void }) {

    const [mode, setMode]   = useState<'month'|'year'>('month');
    const [value, setValue] = useState('FEB');

    const handleSelect = (val:string) => {
        setValue(val);
        onChange?.({ mode, value: val });
        setOpen(false);
    };

    const [open, setOpen] = useState(false);

    return (
        <div className="relative">
            {/* pill button */}
            <button
                onClick={() => setOpen(!open)}
                className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-[#F0F4FF]
                   text-xs font-semibold text-[#2B3674] shadow-sm"
            >
                <Calendar className="w-4 h-4 text-[#2B3674]" />
                {mode === 'month' && `${value} ${new Date().getFullYear()}`}
                {mode === 'year'  && value}
            </button>

            {/* dropdown */}
            {open && (
                <div className="absolute z-50 mt-2 w-40 rounded-lg bg-white shadow-lg p-3">
                    {/* tabs Month / Year */}
                    <div className="flex mb-2 border-b pb-1">
                        {['month','year'].map(t => (
                            <button
                                key={t}
                                onClick={() => { setMode(t as any); setValue(t==='month' ? 'JAN' : '2024'); }}
                                className={clsx(
                                    'flex-1 text-xs py-1 rounded-md',
                                    mode===t ? 'bg-[#E9ECFF] text-[#2B3674]' : 'text-[#8F9BBA] hover:bg-gray-50'
                                )}
                            >
                                {t==='month' ? 'Month' : 'Year'}
                            </button>
                        ))}
                    </div>

                    <div className="grid grid-cols-3 gap-2 max-h-48 overflow-y-auto">
                        {(mode==='month'? months : years).map(opt => (
                            <button
                                key={opt}
                                onClick={() => handleSelect(opt)}
                                className={clsx(
                                    'py-1 text-xs rounded-md',
                                    opt===value
                                        ? 'bg-[#4318FF] text-white'
                                        : 'hover:bg-gray-100 text-[#2B3674]'
                                )}
                            >
                                {opt}
                            </button>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}
