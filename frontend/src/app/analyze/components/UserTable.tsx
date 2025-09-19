/* ----------------------------------------------------------------
 *  Универсальная таблица з динамічними колонками
 * ----------------------------------------------------------------*/
'use client';

import React from 'react';
import type { UserRow } from '../hooks/useUserSearch';

export type Column = { label: string; key: keyof UserRow | string };

type Props = {
    rows?:    UserRow[];
    loading:  boolean;
    pageSize: number;
    columns?: Column[];
};

const UserTable: React.FC<Props> = ({
                                        rows     = [],
                                        loading,
                                        pageSize,
                                        columns  = []
                                    }) => {

    const skeletonRows = Array.from({ length: pageSize });

    const renderCell = (row: UserRow, col: Column) => {
        const val = (row as any)[col.key];
        if (col.key === 'created_at' && val) {
            try { return new Date(val).toLocaleDateString(); }
            catch { return val; }
        }
        if (Array.isArray(val)) return val.join(', ');
        return val ?? '—';
    };

    return (
        <div className="border rounded-xl overflow-hidden ring-1 ring-slate-200/70">
            <table className="w-full text-sm">
                <thead className="bg-slate-50 text-slate-500 font-semibold">
                <tr>{columns.map(c=>(
                    <th key={String(c.key)} className="px-4 py-3 text-left">{c.label}</th>
                ))}</tr>
                </thead>

                <tbody className="text-slate-800 divide-y">
                {/* skeleton */}
                {loading && skeletonRows.map((_,i)=>(
                    <tr key={`sk-${i}`} className="h-[48px]">
                        {columns.map((_,j)=>(
                            <td key={j} className="px-4">
                                <div className="relative h-4 w-full max-w-[140px] bg-slate-200 rounded overflow-hidden">
                    <span className="absolute inset-0 -translate-x-full
                                     animate-[shimmer_1.6s_infinite]
                                     bg-gradient-to-r from-transparent via-white/60 to-transparent"/>
                                </div>
                            </td>
                        ))}
                    </tr>
                ))}

                {/* empty */}
                {!loading && rows.length === 0 && (
                    <tr>
                        <td colSpan={columns.length} className="py-10 text-center text-slate-500">
                            Ничего не найдено
                        </td>
                    </tr>
                )}

                {/* data */}
                {!loading && rows.map(r=>(
                    <tr key={r.id}
                        className="hover:bg-primary/5 hover:shadow-sm transition cursor-pointer">
                        {columns.map(col=>(
                            <td key={String(col.key)} className="px-4 py-2.5">
                                {renderCell(r,col)}
                            </td>
                        ))}
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );
};

export default UserTable;
