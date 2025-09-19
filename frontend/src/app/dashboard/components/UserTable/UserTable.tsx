'use client';

import React, { useState, useMemo } from 'react';
import {
    UserTableProps,
    defaultMapper,
} from './types';

import CardHeader   from './parts/CardHeader';
import CompactTable from './parts/CompactTable';
import CardFooter   from './parts/CardFooter';
import ExpandedModal from './parts/ExpandedModal';

import { useCompactBucket } from './hooks/useCompactBucket';
import { useModalBuckets   } from './hooks/useModalBuckets';
import { useUserDetails    } from './hooks/useUserDetails';
import {useDebounce} from "@/app/dashboard/components/UserTable/hooks/useDebounce";

const DEFAULT_PAGE_SIZE = 5;

const UserTable: React.FC<UserTableProps> = ({
                                                 labels,
                                                 userBucketURL,
                                                 getFullUserURL,
                                                 tableHeads,
                                                 rowMappers,
                                                 requiresId,
                                                 colKeys,
                                                 pageSize = DEFAULT_PAGE_SIZE,
                                                 fixed = true,
                                                 expandedModalTitle = 'Расширенный поиск',
                                             }) => {
    /* ---------- локальний стан ---------- */
    const [roleIdx, setRoleIdx] = useState(0);
    const [skip   , setSkip   ] = useState(0);
    const [filter , setFilter ] = useState('');

    /* ---------- компактна таблиця ---------- */
    const mapper    = rowMappers?.[roleIdx] ?? defaultMapper;
    const bucketURL = userBucketURL[roleIdx];

    const {
        rows, total, loading, error, refetch,
    } = useCompactBucket(bucketURL, requiresId, skip, DEFAULT_PAGE_SIZE, mapper);

    const headTitles = tableHeads?.[roleIdx];

    /* ---------- модальне вікно ---------- */
    const [modalOpen, setModalOpen] = useState(false);
    const [modalRole, setModalRole] = useState(0);
    const [searchRaw, setSearchRaw] = useState('');
    const search = useDebounce(searchRaw, 400);

    const { buckets, fetchBucket } = useModalBuckets(
        labels,
        userBucketURL,
        requiresId,
        pageSize,
        search,
        modalOpen,
        modalRole,
        rowMappers,
    );

    /* ---------- detail-панель ---------- */
    const [detailId, setDetailId] = useState<string | null>(null);
    const detailURL = getFullUserURL?.[modalRole];
    const { data: detailData, loading: detailLoading, error: detailError, refetch: refetchDetail } =
        useUserDetails(detailURL, detailId, !!detailId);

    /* ---------- обробники ---------- */
    const onRowClick = (r: { id: string }) => {
        if (!r.id) return;
        setModalRole(roleIdx);
        setDetailId(r.id);
        setModalOpen(true);
    };

    const changeRole = (i: number) => {
        if (i === roleIdx) return;
        setRoleIdx(i);
        setSkip(0);
    };

    /* ---------- фільтр таблиці ---------- */
    const filtered = useMemo(
        () =>
            rows.filter((r: any) =>
                Object.values(r)
                    .join(' ')
                    .toLowerCase()
                    .includes(filter.toLowerCase())
            ),
        [rows, filter]
    );

    /* ---------- UI ---------- */
    const containerCls = fixed
        ? 'min-h-[420px] sm:min-h-[440px] lg:min-h-[460px]'
        : '';

    // @ts-ignore
    // @ts-ignore
    return (
        <>
            <div className={`w-full bg-white rounded-2xl shadow px-6 py-6 flex flex-col relative overflow-hidden border border-transparent hover:border-[#E5E9F6] transition ${containerCls}`}>
                <CardHeader
                    title="Таблица"
                    labels={labels}
                    roleIndex={roleIdx}
                    onChangeRole={changeRole}
                    onReload={refetch}
                    loading={loading}
                />

                <div className="flex-1 overflow-auto">
                    <CompactTable
                        rows={filtered}
                        loading={loading}
                        pageSize={DEFAULT_PAGE_SIZE}
                        headTitles={headTitles}
                        onRowClick={onRowClick}
                    />
                </div>

                <CardFooter
                    skip={skip}
                    pageSize={pageSize}
                    total={total}
                    onOpenModal={() => { setModalRole(roleIdx); setModalOpen(true); }}
                />

                {error && (
                    <p className="mt-3 text-xs text-red-500 font-medium">Ошибка: {error}</p>
                )}
            </div>

            <
                ExpandedModal
                open={modalOpen}
                onClose={() => {
                    setModalOpen(false);
                    setDetailId(null);
                }}
                labels={labels}
                activeRole={modalRole}
                onSwitchRole={(i) => {
                    setModalRole(i);
                    setDetailId(null);
                }}
                title={expandedModalTitle}
                modalState={buckets[modalRole]}
                fetchCurrent={(reset) => fetchBucket(modalRole, reset)}
                loadMore={() => fetchBucket(modalRole, false)}
                onRowClick={(r) => setDetailId(r.id)}

                detailData={detailData}
                detailLoading={detailLoading}
                detailError={detailError}
                onCloseDetail={() => setDetailId(null)}
                onRefetchDetail={refetchDetail}
                colHeads={tableHeads}
                colKeys={colKeys ?? []}
            />
        </>
    );
};

// @ts-ignore
export default UserTable;
