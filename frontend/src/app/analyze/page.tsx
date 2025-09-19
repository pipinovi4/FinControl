/* eslint-disable react-hooks/exhaustive-deps */
'use client';

import React, { useState, useEffect, useCallback, useRef } from 'react';
import { ChevronDown, Search as SearchIcon, ArrowLeft, Pencil, UserMinus, UserPlus, Trash2, Shuffle, RotateCw } from 'lucide-react';
import { ANALYZE_CFG, RoleKey, EntityKey, Column as ColCfg } from './config/analyzeConfig';
import { useUserSearch, UserRow } from './hooks/useUserSearch';
import { notFound } from 'next/navigation';

import {
    getRole,
    getUserId,
    brokerSignClient,
    brokerUnsignClient,
    adminAssignBrokerByEmail,
    adminAssignWorkerByEmail,
    adminEditClient,
    adminEditBroker,
    adminEditWorker,
    adminSoftDeleteUser, adminRestoreUser,
} from './api';

import ConfirmDialog from './components/ConfirmDialog';
import EditDialog from './components/EditDialog';

/* ─────────────────────────────────────────── */
const getCurrentUserClients = (): string[] => {
    try {
        return (JSON.parse(localStorage.getItem('user') ?? '{}').clients ?? []).map((c: { id: string }) => c.id);
    } catch {
        return [];
    }
};
const ROLE: RoleKey = getRole();

/* ─────────────────────────────────────────── */
/* persistent UI state                        */
/* ─────────────────────────────────────────── */
interface PersistedUI { entity: number; field: number; query: string; status: 'all'|'active'|'deleted'; }
const LS_STATE_KEY = 'analyzeState';
const loadUIState = (): PersistedUI | null => {
    try { return JSON.parse(localStorage.getItem(LS_STATE_KEY) ?? 'null'); } catch { return null; }
};
const saveUIState = (s: PersistedUI) => localStorage.setItem(LS_STATE_KEY, JSON.stringify(s));

/* persistent cache */
const LS_CACHE_KEY = 'analyzeCache';
const loadCache = (): Map<string, any[]> => {
    try {
        const raw: Record<string, any[]> = JSON.parse(localStorage.getItem(LS_CACHE_KEY) ?? '{}');
        return new Map(Object.entries(raw));
    } catch { return new Map(); }
};
const saveCache = (cache: Map<string, any[]>) => {
    const obj: Record<string, any[]> = {};
    cache.forEach((v, k) => { obj[k] = v; });
    try { localStorage.setItem(LS_CACHE_KEY, JSON.stringify(obj)); } catch {}
};

/* ─────────────────────────────────────────── */
/* Helpers                                    */
/* ─────────────────────────────────────────── */
function StatusBadge({ deleted, inactive }: { deleted?: boolean; inactive?: boolean }) {
    if (deleted) return <span className="inline-flex items-center rounded-full bg-rose-100 text-rose-700 px-2 py-0.5 text-[11px] font-semibold">Удалён</span>;
    if (inactive) return <span className="inline-flex items-center rounded-full bg-amber-100 text-amber-700 px-2 py-0.5 text-[11px] font-semibold">Неактивен</span>;
    return <span className="inline-flex items-center rounded-full bg-emerald-100 text-emerald-700 px-2 py-0.5 text-[11px] font-semibold">Активен</span>;
}

/* ─────────────────────────────────────────── */
/* Generic DataTable                          */
/* ─────────────────────────────────────────── */
interface DataTableProps {
    rows: UserRow[];
    loading: boolean;
    pageSize: number;
    columns: ColCfg[];
    onRowClick: (row: UserRow) => void;
    currentEntity: EntityKey;
    onAction: (action: string, row: UserRow) => void;
}

const DataTable: React.FC<DataTableProps> = ({ rows, loading, pageSize, columns, onRowClick, currentEntity, onAction }) => {
    const skeletonRows = Array.from({ length: pageSize });
    const attachedIds = useRef<string[]>(getCurrentUserClients()).current;
    const isAttached = (id: string) => attachedIds.includes(id);

    const renderCell = (row: UserRow, col: ColCfg) => {
        if (col.key === '__status') {
            return <StatusBadge deleted={row.is_deleted} inactive={row.is_active === false} />;
        }
        const val = (row as any)[col.key];
        if (col.key === 'created_at' && val) {
            try { return new Date(val).toLocaleDateString(); } catch { return val; }
        }
        if (Array.isArray(val)) return val.join(', ');
        return val ?? '—';
    };

    const renderActions = (row: UserRow) => {
        switch (ROLE) {
            case 'broker':
                return (
                    <div className="flex gap-2">
                        {!isAttached(row.id) ? (
                            <button
                                className="cursor-pointer px-3 py-1.5 rounded bg-green-600 hover:bg-green-700 text-white text-xs inline-flex items-center gap-1"
                                title="Подписать клиента"
                                onClick={(e) => { e.stopPropagation(); onAction('broker:sign', row); }}
                            >
                                <UserPlus size={14} /> Подписать
                            </button>
                        ) : (
                            <button
                                className="cursor-pointer px-3 py-1.5 rounded bg-red-600 hover:bg-red-700 text-white text-xs inline-flex items-center gap-1"
                                title="Отписать клиента"
                                onClick={(e) => { e.stopPropagation(); onAction('broker:unsign', row); }}
                            >
                                <UserMinus size={14} /> Отписать
                            </button>
                        )}
                    </div>
                );
            case 'admin':
                return (
                    <div className="flex flex-wrap gap-2">
                        {currentEntity === 'clients' && (
                            <>
                                <button
                                    className="cursor-pointer px-3 py-1.5 rounded bg-blue-600 hover:bg-blue-700 text-white text-xs inline-flex items-center gap-1"
                                    title="Изменить работника"
                                    onClick={(e) => { e.stopPropagation(); onAction('admin:assign-worker', row); }}
                                >
                                    <Shuffle size={14} /> Работник
                                </button>
                                <button
                                    className="cursor-pointer px-3 py-1.5 rounded bg-blue-600 hover:bg-blue-700 text-white text-xs inline-flex items-center gap-1"
                                    title="Изменить брокера"
                                    onClick={(e) => { e.stopPropagation(); onAction('admin:assign-broker', row); }}
                                >
                                    <Shuffle size={14} /> Брокер
                                </button>
                            </>
                        )}
                        <button
                            className="cursor-pointer px-3 py-1.5 rounded bg-amber-600 hover:bg-amber-700 text-white text-xs inline-flex items-center gap-1"
                            title="Редактировать запись"
                            onClick={(e) => { e.stopPropagation(); onAction('admin:edit', row); }}
                        >
                            <Pencil size={14} /> Редактировать
                        </button>

                        {row.is_deleted ? (
                            <button
                                className="cursor-pointer px-3 py-1.5 rounded bg-emerald-600 hover:bg-emerald-700 text-white text-xs inline-flex items-center gap-1"
                                title="Восстановить пользователя"
                                onClick={(e) => { e.stopPropagation(); onAction('admin:restore', row); }}
                            >
                                <RotateCw size={14} /> Восстановить
                            </button>
                        ) : (
                            <button
                                className="cursor-pointer px-3 py-1.5 rounded bg-rose-600 hover:bg-rose-700 text-white text-xs inline-flex items-center gap-1"
                                title="Мягко удалить пользователя"
                                onClick={(e) => { e.stopPropagation(); onAction('admin:delete', row); }}
                            >
                                <Trash2 size={14} /> Удалить
                            </button>
                        )}
                    </div>
                );
            default:
                return null;
        }
    };

    return (
        <div className="border rounded-xl overflow-hidden ring-1 ring-slate-200/70">
            <table className="w-full text-sm">
                <thead className="bg-slate-50 text-slate-500 font-semibold">
                <tr>
                    {columns.map((c) => (
                        <th key={String(c.key)} className="px-4 py-3 text-left">{c.label}</th>
                    ))}
                    <th className="px-4 py-3 text-left w-1/6">Действия</th>
                </tr>
                </thead>
                <tbody className="text-slate-800 divide-y">
                {loading && Array.from({ length: pageSize }).map((_, i) => (
                    <tr key={`sk-${i}`} className="h-[48px]">
                        {columns.map((_, j) => (
                            <td key={j} className="px-4">
                                <div className="relative h-4 w-full max-w-[140px] bg-slate-200 rounded overflow-hidden">
                                    <span className="absolute inset-0 -translate-x-full animate-[shimmer_1.6s_infinite] bg-gradient-to-r from-transparent via-white/60 to-transparent" />
                                </div>
                            </td>
                        ))}
                        <td className="px-4" />
                    </tr>
                ))}
                {!loading && rows.length === 0 && (
                    <tr><td colSpan={columns.length + 1} className="py-10 text-center text-slate-500">Ничего не найдено</td></tr>
                )}
                {!loading && rows.map((r) => (
                    <tr key={r.id} className="hover:bg-primary/5 hover:shadow-sm transition cursor-pointer" onClick={() => onRowClick(r)}>
                        {columns.map((col) => (
                            <td key={String(col.key)} className="px-4 py-2.5">{renderCell(r, col)}</td>
                        ))}
                        <td className="px-4 py-2.5">{renderActions(r)}</td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );
};

/* ─────────────────────────────────────────── */
/* ProfileView                                */
/* ─────────────────────────────────────────── */
const ProfileView: React.FC<{
    loading: boolean;
    error: string | null;
    data: Record<string, any> | null;
    onBack: () => void;
    onRefresh: () => void;
    onEdit: () => void;
    onDelete: () => void;
    onAssignWorker?: () => void;
    onAssignBroker?: () => void;
}> = ({ loading, error, data, onBack, onRefresh, onEdit, onDelete, onAssignWorker, onAssignBroker }) => {
    const prettify = useCallback((k: string) => k.replace(/_/g, ' ').replace(/\b\w/g, (ch) => ch.toUpperCase()), []);
    const formatVal = useCallback((v: any) => {
        if (v === null || v === undefined) return '—';
        if (typeof v === 'object') {
            try { return JSON.stringify(v, null, 2); } catch { return String(v); }
        }
        return String(v);
    }, []);

    return (
        <div className="flex flex-col gap-6">
            <div className="flex items-center gap-2">
                <button onClick={onBack} className="p-2 -ml-2 rounded-lg text-primary hover:bg-primary/10"><ArrowLeft size={18} /></button>
                <h2 className="text-xl font-bold text-slate-800">Профиль</h2>
                <button onClick={onRefresh} className="ml-auto px-4 py-2 rounded-lg bg-primary text-white text-sm font-medium hover:opacity-90">Обновить</button>
            </div>

            {loading && (
                <div className="space-y-4 animate-pulse p-1">
                    {Array.from({ length: 8 }).map((_, i) => (<div key={i} className="h-4 w-2/3 rounded bg-slate-200" />))}
                </div>
            )}
            {!loading && error && <div className="text-sm text-red-500 font-medium">{error}</div>}

            {!loading && !error && data && (
                <div className="space-y-5">
                    {Object.entries(data).map(([k, v]) => (
                        <div key={k} className="rounded-xl border border-slate-200 px-4 py-3 bg-slate-50 hover:bg-slate-100 transition">
                            <div className="text-[11px] uppercase tracking-wide text-slate-500 font-semibold mb-1">{prettify(k)}</div>
                            <div className="text-sm font-medium text-slate-800 whitespace-pre-wrap break-words">{formatVal(v)}</div>
                        </div>
                    ))}
                </div>
            )}

            {!loading && !error && (
                <div className="pt-4 flex flex-wrap gap-3">
                    <button onClick={onEdit} className="px-4 py-2 rounded-lg bg-blue-600 text-white text-sm font-medium hover:opacity-90 inline-flex items-center gap-2">
                        <Pencil size={16} /> Редактировать
                    </button>

                    {data?.is_deleted ? (
                        <button
                            onClick={async () => {
                                try {
                                    await adminRestoreUser(String(data.id));
                                    onRefresh();
                                } catch (e: any) {
                                    alert(e.message || 'Ошибка восстановления');
                                }
                            }}
                            className="px-4 py-2 rounded-lg bg-emerald-600 text-white text-sm font-medium hover:opacity-90 inline-flex items-center gap-2"
                        >
                            Восстановить
                        </button>
                    ) : (
                        <button onClick={onDelete} className="px-4 py-2 rounded-lg bg-rose-600 text-white text-sm font-medium hover:opacity-90 inline-flex items-center gap-2">
                            <Trash2 size={16} /> Удалить
                        </button>
                    )}

                    {onAssignWorker && (
                        <button onClick={onAssignWorker} className="px-4 py-2 rounded-lg bg-indigo-600 text-white text-sm font-medium hover:opacity-90">
                            Изменить работника
                        </button>
                    )}
                    {onAssignBroker && (
                        <button onClick={onAssignBroker} className="px-4 py-2 rounded-lg bg-indigo-600 text-white text-sm font-medium hover:opacity-90">
                            Изменить брокера
                        </button>
                    )}
                </div>
            )}
        </div>
    );
};

/* ─────────────────────────────────────────── */
/* Main Analyze Page                           */
/* ─────────────────────────────────────────── */
const AnalyzePage: React.FC = () => {
    const roleCfg = ANALYZE_CFG[ROLE];
    if (ROLE === 'worker') return notFound();

    const entityKeys = Object.keys(roleCfg.entities) as EntityKey[];

    const persisted = loadUIState();
    const [entityIx, setEntityIx] = useState(Math.max(0, Math.min(persisted?.entity ?? 0, entityKeys.length - 1)));
    const [fieldIx, setFieldIx] = useState(persisted?.field ?? 0);
    const [query, setQuery] = useState(persisted?.query ?? '');

    // status filter (Admin only): all | active | deleted
    const [status, setStatus] = useState<'all'|'active'|'deleted'>(persisted?.status ?? 'all');

    const [viewMode, setViewMode] = useState<'list' | 'detail'>('list');
    const [detailData, setDetailData] = useState<Record<string, any> | null>(null);
    const [detailLoading, setDetailLoading] = useState(false);
    const [detailError, setDetailError] = useState<string | null>(null);
    const [selectedId, setSelectedId] = useState<string | null>(null);

    const [confirmOpen, setConfirmOpen] = useState(false);
    const [assignOpen, setAssignOpen] = useState<null | 'worker' | 'broker'>(null);
    const [editOpen, setEditOpen] = useState(false);

    const entityCfg = roleCfg.entities[entityKeys[entityIx]]!;
    const field = entityCfg.fields[fieldIx];

    const cacheRef = useRef<Map<string, any[]>>(loadCache());
    const { loading, rows, error, setRows, runSearch: rawRun } = useUserSearch(entityCfg.endpoint, field);

    const statusKey = ROLE === 'admin' ? status : 'all';

    const makeKey = useCallback(
        (val: string) => `${entityKeys[entityIx]}|${field.param}|${statusKey}|${val.trim()}`,
        [entityIx, field, statusKey]
    );

    const runSearch = (val: string) => {
        const key = makeKey(val);
        const cached = cacheRef.current.get(key);
        if (cached) setRows(cached);

        const is_deleted =
            ROLE !== 'admin' ? null :
                status === 'deleted' ? true :
                    status === 'active' ? false :
                        null;

        rawRun(val, { is_deleted }).then((list) => {
            cacheRef.current.set(key, list);
            saveCache(cacheRef.current);
            setRows(list);
        });
    };

    const detailBase: string = (entityCfg as any).detailEndpoint ?? entityCfg.endpoint.replace('filter/bucket/', '');

    const fetchDetail = async (id: string) => {
        setViewMode('detail');
        setSelectedId(id);
        setDetailLoading(true);
        setDetailError(null);
        try {
            const res = await fetch(detailBase + id, { credentials: 'include' });
            if (!res.ok) throw new Error(res.statusText);
            const json = await res.json();
            setDetailData(json);
        } catch (e: any) {
            setDetailError(e.message || 'Network error');
            setDetailData(null);
        } finally {
            setDetailLoading(false);
        }
    };

    useEffect(() => {
        if (!query.trim()) { setRows([]); return; }
        const key = makeKey(query);
        setRows(cacheRef.current.get(key) ?? []);
    }, [entityIx, fieldIx, statusKey]);

    useEffect(() => { saveUIState({ entity: entityIx, field: fieldIx, query, status }); }, [entityIx, fieldIx, query, status]);

    const onSubmit = (e: React.FormEvent) => { e.preventDefault(); query.trim() && runSearch(query); };
    const refetchDetail = () => { if (selectedId) fetchDetail(selectedId); };

    /* ────────────── Actions wiring ────────────── */
    const userId = getUserId();

    const handleTableAction = async (action: string, row: UserRow) => {
        try {
            if (action === 'broker:sign') {
                if (!userId) throw new Error('Нет id брокера');
                await brokerSignClient(row.id, userId);
                const user = JSON.parse(localStorage.getItem('user') ?? '{}');
                user.clients = [...(user.clients ?? []), { id: row.id }];
                localStorage.setItem('user', JSON.stringify(user));
            }
            if (action === 'broker:unsign') {
                await brokerUnsignClient(row.id);
                const user = JSON.parse(localStorage.getItem('user') ?? '{}');
                user.clients = (user.clients ?? []).filter((c: any) => c.id !== row.id);
                localStorage.setItem('user', JSON.stringify(user));
            }
            if (action === 'admin:assign-worker') {
                setSelectedId(row.id);
                setAssignOpen('worker');
                return;
            }
            if (action === 'admin:assign-broker') {
                setSelectedId(row.id);
                setAssignOpen('broker');
                return;
            }
            if (action === 'admin:edit') {
                setSelectedId(row.id);
                await fetchDetail(row.id);
                setEditOpen(true);
                return;
            }
            if (action === 'admin:delete') {
                setSelectedId(row.id);
                setConfirmOpen(true);
                return;
            }
            if (action === 'admin:restore') {
                await adminRestoreUser(row.id);
                setRows(prev => prev.map(r => r.id === row.id ? { ...r, is_deleted: false } : r));
                return;
            }
        } catch (e: any) {
            alert(e.message || 'Ошибка');
        }
    };

    const handleDelete = async () => {
        if (!selectedId) return;
        try {
            await adminSoftDeleteUser(selectedId);
            setRows((prev) => prev.map((r) => (r.id === selectedId ? { ...r, is_deleted: true } : r)));
            setConfirmOpen(false);
            setViewMode('list');
        } catch (e: any) {
            alert(e.message || 'Ошибка удаления');
        }
    };

    // простое модальное «перепризначити» — вводим email или пусто
    const AssignDialog = () =>
        !assignOpen ? null : (
            <div
                className="fixed inset-0 z-[92] flex items-center justify-center bg-black/40 backdrop-blur-sm"
                onClick={() => setAssignOpen(null)}
            >
                <div
                    className="w-[min(520px,92vw)] rounded-2xl border border-slate-200 bg-white p-5 shadow-2xl"
                    onClick={(e) => e.stopPropagation()}
                >
                    <h3 className="text-base font-bold text-[#2B3674] mb-1">
                        {assignOpen === 'worker' ? 'Изменить работника' : 'Изменить брокера'}
                    </h3>
                    <p className="text-sm text-slate-600 mb-3">
                        Введите <b>email</b> (оставьте пустым, чтобы снять привязку).
                    </p>
                    <input
                        id="assign-input"
                        type="email"
                        className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:ring-2 focus:ring-primary/40 focus:border-primary"
                        placeholder={assignOpen === 'worker' ? 'worker@email' : 'broker@email'}
                    />
                    <div className="mt-4 flex justify-end gap-2">
                        <button
                            className="rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm hover:bg-slate-50"
                            onClick={() => setAssignOpen(null)}
                        >
                            Отмена
                        </button>
                        <button
                            className="rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-white"
                            onClick={async () => {
                                const val = (document.getElementById('assign-input') as HTMLInputElement).value.trim();
                                const email = val === '' ? null : val;
                                try {
                                    if (!selectedId) return;
                                    if (assignOpen === 'worker') {
                                        await adminAssignWorkerByEmail(selectedId, email);
                                    } else {
                                        await adminAssignBrokerByEmail(selectedId, email);
                                    }
                                    setAssignOpen(null);
                                    if (viewMode === 'detail') refetchDetail();
                                } catch (e: any) {
                                    alert(e.message || 'Ошибка назначения');
                                }
                            }}
                        >
                            Сохранить
                        </button>
                    </div>
                </div>
            </div>
        );

    const handleSaveEdit = async (patch: Record<string, any>) => {
        if (!selectedId || !detailData) return;
        const entity = entityKeys[entityIx];
        if (Object.keys(patch).length === 0) return;

        if (entity === 'clients') await adminEditClient(selectedId, patch);
        if (entity === 'brokers') await adminEditBroker(selectedId, patch);
        if (entity === 'workers') await adminEditWorker(selectedId, patch);

        await refetchDetail();
        setRows((prev) => prev.map((r) => (r.id === selectedId ? { ...r, ...patch } : r)));
    };

    /* ───────────────────────── UI ───────────────────────── */
    return (
        <div className="md:ml-60 min-h-screen font-[var(--font-dm-sans)]">
            <header className="px-6 py-4 text-primary">
                <div className="text-sm opacity-80">Pages / Analytic</div>
                <h1 className="text-2xl font-bold mt-1 opacity-95">Аналитика</h1>
            </header>

            <main className="p-4 flex flex-col gap-6">
                {viewMode === 'list' ? (
                    <>
                        {/* Search card */}
                        <form onSubmit={onSubmit} className="relative isolate bg-white/80 backdrop-blur-lg shadow ring-1 ring-slate-200/70 rounded-xl px-4 py-5 flex flex-col lg:flex-row gap-4">
                            <div className="relative w-full sm:w-48">
                                <select
                                    value={entityIx}
                                    onChange={(e) => { setEntityIx(+e.target.value); setFieldIx(0); }}
                                    className="appearance-none w-full pl-10 pr-8 py-2.5 rounded-lg border border-slate-300 bg-white text-sm text-slate-700 font-medium focus:ring-2 focus:ring-primary/40 focus:border-primary"
                                >
                                    {entityKeys.map((k, i) => (<option key={k} value={i}>{roleCfg.entities[k]!.entityLabel}</option>))}
                                </select>
                                <SearchIcon size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                                <ChevronDown size={16} className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400" />
                            </div>

                            <div className="relative w-full sm:w-56">
                                <select
                                    value={fieldIx}
                                    onChange={(e) => setFieldIx(+e.target.value)}
                                    className="appearance-none w-full pl-3 pr-8 py-2.5 rounded-lg border border-slate-300 bg-white text-sm text-slate-700 font-medium focus:ring-2 focus:ring-primary/40 focus:border-primary"
                                >
                                    {roleCfg.entities[entityKeys[entityIx]]!.fields.map((f, i) => (<option key={f.param} value={i}>{f.label}</option>))}
                                </select>
                                <ChevronDown size={16} className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400" />
                            </div>

                            {/* NEW: фильтр статуса для Admin */}
                            {ROLE === 'admin' && (
                                <div className="relative w-full sm:w-56">
                                    <select
                                        value={status}
                                        onChange={(e) => setStatus(e.target.value as any)}
                                        className="appearance-none w-full pl-3 pr-8 py-2.5 rounded-lg border border-slate-300 bg-white text-sm text-slate-700 font-medium focus:ring-2 focus:ring-primary/40 focus:border-primary"
                                        title="Статус аккаунта"
                                    >
                                        <option value="all">Все</option>
                                        <option value="active">Активные</option>
                                        <option value="deleted">Удалённые</option>
                                    </select>
                                    <ChevronDown size={16} className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400" />
                                </div>
                            )}

                            <input
                                value={query}
                                onChange={(e) => setQuery(e.target.value)}
                                placeholder={`Введите ${roleCfg.entities[entityKeys[entityIx]]!.fields[fieldIx].label.toLowerCase()}…`}
                                className="flex-1 px-4 py-2.5 rounded-lg border border-slate-300 text-sm text-slate-800 focus:ring-2 focus:ring-primary/40 focus:border-primary"
                            />

                            <button type="submit" disabled={loading} className="px-7 py-2.5 rounded-lg bg-primary text-white font-semibold transition disabled:opacity-60">
                                {loading ? '…' : 'Поиск'}
                            </button>
                        </form>

                        {error && <p className="text-sm text-red-600 font-medium">Ошибка: {error}</p>}

                        <DataTable
                            rows={rows}
                            loading={loading}
                            pageSize={roleCfg.pageSize}
                            columns={roleCfg.entities[entityKeys[entityIx]]!.columns}
                            onRowClick={(r) => fetchDetail(r.id)}
                            currentEntity={entityKeys[entityIx] as EntityKey}
                            onAction={handleTableAction}
                        />
                    </>
                ) : (
                    <ProfileView
                        loading={detailLoading}
                        error={detailError}
                        data={detailData}
                        onBack={() => setViewMode('list')}
                        onRefresh={refetchDetail}
                        onEdit={() => setEditOpen(true)}
                        onDelete={() => setConfirmOpen(true)}
                        onAssignWorker={ROLE === 'admin' && (entityKeys[entityIx] as EntityKey) === 'clients'
                            ? () => setAssignOpen('worker')
                            : undefined}
                        onAssignBroker={ROLE === 'admin' && (entityKeys[entityIx] as EntityKey) === 'clients'
                            ? () => setAssignOpen('broker')
                            : undefined}
                    />
                )}
            </main>

            {/* Modals */}
            <AssignDialog />

            <EditDialog
                open={editOpen}
                data={detailData}
                onClose={() => setEditOpen(false)}
                onSave={handleSaveEdit}
                title="Редактирование записи"
            />

            <ConfirmDialog
                open={confirmOpen}
                onClose={() => setConfirmOpen(false)}
                onConfirm={handleDelete}
                title="Удалить пользователя?"
                subtitle="Это мягкое удаление: запись будет деактивирована и исключена из списков."
                confirmText="Удалить"
                cancelText="Отмена"
            />
        </div>
    );
};

export default AnalyzePage;
