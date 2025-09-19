/*  CompactTable.tsx
 *  Універсальна «компактна» таблиця:
 *   – skeleton-рядки під час завантаження
 *   – порожній стан
 *   – довільна кількість стовпців (ключі ≠ заголовки)
 *   – мінімум “магії” усередині
 * -------------------------------------------------------------- */

import React from 'react';
import { ROW_HEIGHT, Row } from '../types';
import {formatDate} from "@/app/dashboard/components/UserTable/utils";

/* ------------------------- props ---------------------------- */
export interface CompactTableProps {
    rows: Row[];

    /** чи йде зараз запит — показуємо скелетони */
    loading: boolean;

    /** скільки рядків бажано бачити на сторінці —
     *  використовується для skeleton / filler-рядків */
    pageSize: number;

    /** click-handler по рядку (опційно) */
    onRowClick?: (row: Row) => void;

    /** справжні ключі в об’єкті Row, у тому порядку,
     *  у якому їх треба виводити (✱ якщо не передати —
     *  візьмемо все, що є в rows[0], крім id) */
    colKeys?: string[];

    /** заголовки для <th>; якщо не передати —
     *  prettify(colKeys) → «Full Name», «Phone» … */
    headTitles?: string[];
}

/* prettify('full_name') → 'Full Name' */
const prettify = (k: string) =>
    k
        .replace(/_/g, ' ')
        .replace(/\b\w/g, (c) => c.toUpperCase());

/* ---------------------- компонент --------------------------- */
const CompactTable: React.FC<CompactTableProps> = ({
                                                       rows,
                                                       loading,
                                                       pageSize,
                                                       onRowClick,
                                                       colKeys,
                                                       headTitles,
                                                   }) => {
    /* -------- keys + titles ---------------------------------- */
    const keys =
        colKeys && colKeys.length
            ? colKeys
            : Object.keys(rows[0] ?? {}).filter((k) => k !== 'id');

    const titles =
        headTitles && headTitles.length
            ? headTitles
            : keys.map(prettify);

    const colCount = titles.length;
    const fillerCount = Math.max(0, pageSize - rows.length);

    /* -------- helper частини --------------------------------- */
    const Head = () => (
        <thead className="text-[#8F9BBA] text-left border-b font-bold tracking-tight bg-white sticky top-0 z-10">
        <tr>
            {titles.map((t) => (
                <th key={t} className="py-3 pl-3 text-sm font-bold tracking-tight">
                    {t}
                </th>
            ))}
        </tr>
        </thead>
    );

    const Skeleton = () => (
        <tbody>
        {Array.from({ length: pageSize }).map((_, i) => (
            <tr key={i} className="animate-pulse" style={{ height: ROW_HEIGHT, paddingLeft: 10 }}>
                {Array.from({ length: colCount }).map((__, j) => (
                    <td key={j} className="py-2">
                        <div className="h-4 w-full max-w-[160px] rounded bg-[#EEF3FF]" />
                    </td>
                ))}
            </tr>
        ))}
        </tbody>
    );

    const Empty = () => (
        <tbody>
        <tr style={{ height: ROW_HEIGHT * pageSize }}>
            <td colSpan={colCount}>
                <div className="h-full w-full flex flex-col items-center justify-center text-[#8F9BBA]">
                    <div className="w-12 h-12 rounded-full bg-[#F4F7FE] flex items-center justify-center mb-3 text-[#7144ff] font-semibold">
                        –
                    </div>
                    <p className="text-sm font-medium">Нет данных</p>
                </div>
            </td>
        </tr>
        </tbody>
    );

    /* -------- render-гілки ----------------------------------- */
    if (loading) {
        return (
            <table className="w-full text-sm">
                <Head />
                <Skeleton />
            </table>
        );
    }

    if (rows.length === 0) {
        return (
            <table className="w-full text-sm">
                <Head />
                <Empty />
            </table>
        );
    }

    /* -------- normal table ----------------------------------- */
    return (
        <table className="w-full text-sm">
            <Head />
            <tbody className="text-[#2B3674] font-medium tracking-tight">
            {rows.map((r) => (
                <tr
                    key={r.id}
                    className="border-b border-[#F0F3FA] hover:bg-[#F6F8FD] transition cursor-pointer"
                    style={{ height: ROW_HEIGHT }}
                    onClick={() => onRowClick?.(r)}
                >
                    {keys.map((k) => (
                        <td key={k} className="py-2 pl-3">
                            {k.includes('taken_at') ? formatDate((r as any)[k])
                                : String((r as any)[k] ?? '—')}
                        </td>
                    ))}
                </tr>
            ))}

            {/* filler, щоби завжди було pageSize рядків */}
            {Array.from({ length: fillerCount }).map((_, i) => (
                <tr
                    key={`filler-${i}`}
                    style={{ height: ROW_HEIGHT }}
                    className="border-b border-transparent pointer-events-none"
                >
                    <td colSpan={colCount} />
                </tr>
            ))}
            </tbody>
        </table>
    );
};

export default CompactTable;
