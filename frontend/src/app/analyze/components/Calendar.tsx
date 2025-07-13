'use client';

import * as React from 'react';
import { DayPicker, DateRange, ClassNames } from 'react-day-picker';
import 'react-day-picker/dist/style.css';
import { useOutsideClick } from '@/lib/hooks/useOutsideClick';

/* ──────────── types ──────────── */
interface SingleCalProps {
    mode?: 'single';
    selected?: Date;
    onSelect?: (date?: Date) => void;
}

interface RangeCalProps {
    mode: 'range';
    selected?: DateRange;
    onSelect?: (range?: DateRange) => void;
    required?: boolean;
}

export type CalendarProps = (SingleCalProps | RangeCalProps) & {
    placeholder?: string;
    label?: string;
};

/* ─────────── styles for DayPicker ─────────── */
const twClasses: ClassNames = {
    caption_label:    'font-medium text-center mb-2',
    nav_button:       'text-[#4B22F4] px-2 rounded hover:bg-[#F0F1F9]',
    table:            'w-full border-collapse',
    head_cell:        'w-8 h-8 text-center font-medium text-[#8F9BBA]',
    cell:             'w-8 h-8 text-center relative',
    day:              'w-8 h-8 inline-flex items-center justify-center rounded-full cursor-pointer select-none',
    day_today:        'font-bold',
    day_outside:      'text-[#D1D4E0] pointer-events-none',
    day_selected:     'bg-[#4B22F4] text-white shadow-md',
    day_range_middle: 'bg-[#F3F3FF] text-[#4B22F4]',
    day_range_start:  'bg-[#F3F3FF] rounded-l-full text-[#4B22F4]',
    day_range_end:    'bg-[#F3F3FF] rounded-r-full text-[#4B22F4]',
};

/* ─────────── component ─────────── */
export const Calendar: React.FC<CalendarProps> = (props) => {
    const [open, setOpen] = React.useState(false);
    const ref = React.useRef<HTMLDivElement>(null);
    useOutsideClick(ref, () => setOpen(false));

    /* label for closed state */
    const renderLabel = () => {
        if (props.mode === 'range') {
            const r = props.selected as DateRange | undefined;
            return r?.from && r?.to
                ? `${r.from.toLocaleDateString()} – ${r.to.toLocaleDateString()}`
                : props.placeholder ?? 'Виберіть період';
        }
        const d = props.selected as Date | undefined;
        return d ? d.toLocaleDateString() : props.placeholder ?? 'Виберіть дату';
    };

    /* handlers */
    const handleSingle = (d?: Date) => {
        (props as SingleCalProps).onSelect?.(d);
        setOpen(false);
    };

    const handleRange = (r?: DateRange) => {
        (props as RangeCalProps).onSelect?.(r);
        /* auto-close, коли вибрано обидві дати */
        if (r?.from && r?.to) setOpen(false);
    };

    return (
        <div ref={ref} className="relative inline-block w-full">
            {/* clickable field */}
            <div
                onClick={() => setOpen(!open)}
                className="w-full px-4 py-2 bg-white border rounded-xl shadow-sm cursor-pointer hover:border-primary text-left"
            >
                {renderLabel()}
            </div>

            {open && (
                <div className="absolute z-50 mt-2 left-0 bg-white border rounded-xl shadow-lg p-3">
                    {props.mode === 'range' ? (
                        <DayPicker
                            mode="range"
                            selected={props.selected as DateRange | undefined}
                            onSelect={handleRange}
                            required={(props as RangeCalProps).required}
                            classNames={twClasses}
                        />
                    ) : (
                        <DayPicker
                            mode="single"
                            selected={props.selected as Date | undefined}
                            onSelect={handleSingle}
                            classNames={twClasses}
                        />
                    )}
                </div>
            )}
        </div>
    );
};
