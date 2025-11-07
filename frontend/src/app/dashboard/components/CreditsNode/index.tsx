// src/app/dashboard/components/CreditsNode/CreditsNode.tsx
"use client";

import React, { useCallback, useEffect, useMemo, useRef, useState } from "react";
import clsx from "clsx";
import { Loader2, RefreshCw, Search, Trash2, CheckCircle, Users } from "lucide-react";
import UserStorage from "@/services/UserStorage";
import {
    fetchAdminCredits,
    fetchAdminClients,
    adminDeleteCredit,
    adminRestoreCredit,
    adminDeleteClient,
    adminRestoreClient,
} from "./configs/api";
import CreditRow from "./parts/CreditRow";
import ClientRow from "./parts/ClientRow";
import ConfirmModal from "./parts/modals/CofirmModal";
import EntityModal from "./parts/modals/EntityModal";
import CreateCreditModal from "./parts/modals/CreateCreditModal";
import type {
    Role,
    CreditOut,
    ClientOut,
    CreditStatus,
} from "@/app/dashboard/components/CreditsNode/configs/types";

const API = process.env.NEXT_PUBLIC_API_URL ?? "";
type Tab = "credits" | "clients";
type DeletedFilter = "active" | "only" | "all";
const LIMIT = 30;

const STATUS_OPTIONS = [
    { value: "all", label: "Все статусы" },
    { value: "new", label: "Новая" },
    { value: "treatment", label: "На доработку" },
    { value: "approved", label: "Согласовано" },
    { value: "completed", label: "Выдано" },
] as const;

type OpenEntity =
    | { kind: "credit"; data: CreditOut }
    | { kind: "client"; data: ClientOut }
    | null;

export default function CreditsNode() {
    // session/role/auth
    const session: any = UserStorage.get();
    const adminId = session?.id ?? session?.data?.id;
    const token = session?.access_token ?? session?.data?.access_token;
    const auth = token ? `Bearer ${token}` : "";
    const role: Role = (session?.role ?? session?.data?.role ?? "admin").toLowerCase();

    // UI state
    const [tab, setTab] = useState<Tab>("credits");
    const [input, setInput] = useState("");
    const [search, setSearch] = useState("");
    const [statusFilter, setStatusFilter] = useState<CreditStatus | "all">("all");
    const [deleted, setDeleted] = useState<DeletedFilter>("all");

    // data state
    const [rows, setRows] = useState<any[]>([]);
    const [total, setTotal] = useState(0);
    const [skip, setSkip] = useState(0);
    const [loading, setLoading] = useState(false);
    const [hasMore, setHasMore] = useState(true);

    // guards
    const inflightRef = useRef(false);
    const reqIdRef = useRef(0);

    // scroll + lazy loading refs
    const listScrollRef = useRef<HTMLDivElement | null>(null);
    const loadMoreRef = useRef<HTMLDivElement | null>(null);

    // modals
    const [openEntity, setOpenEntity] = useState<OpenEntity>(null);
    const [openCreateForClient, setOpenCreateForClient] = useState<ClientOut | null>(null);
    const [confirm, setConfirm] =
        useState<{ kind: "delete" | "restore"; entity: "credit" | "client"; row: any } | null>(null);

    // errors
    const [error, setError] = useState<string | null>(null);

    // key for reload on filters change
    const queryKey = useMemo(
        () => `${tab}|${search}|${statusFilter}|${deleted}`,
        [tab, search, statusFilter, deleted]
    );

    // loader
    const load = useCallback(
        async (fromStart = false) => {
            if (inflightRef.current) return;
            if (!fromStart && (!hasMore || loading)) return;

            inflightRef.current = true;
            setLoading(true);
            setError(null);
            const myReq = ++reqIdRef.current;
            const offset = fromStart ? 0 : skip;

            try {
                if (tab === "credits") {
                    const { credits, total } = await fetchAdminCredits({
                        token: auth,
                        base: API,
                        skip: offset,
                        limit: LIMIT,
                        statuses: statusFilter === "all" ? undefined : [statusFilter],
                        search: search || undefined,
                        deleted,
                    });
                    if (myReq !== reqIdRef.current) return;

                    const nextSkip = offset + credits.length;
                    const progressed = nextSkip > offset;

                    setRows((prev) => (offset === 0 ? credits : [...prev, ...credits]));
                    setTotal(total);
                    setSkip(nextSkip);
                    setHasMore(progressed && nextSkip < total);
                } else {
                    const { clients, total } = await fetchAdminClients({
                        token: auth,
                        base: API,
                        skip: offset,
                        limit: LIMIT,
                        search: search || undefined,
                        id: adminId,
                        deleted,
                    });
                    if (myReq !== reqIdRef.current) return;

                    const nextSkip = offset + clients.length;
                    const progressed = nextSkip > offset;

                    setRows((prev) => (offset === 0 ? clients : [...prev, ...clients]));
                    setTotal(total);
                    setSkip(nextSkip);
                    setHasMore(progressed && nextSkip < total);
                }
            } catch (e: any) {
                console.error("[CreditsNode] load error:", e);
                if (myReq === reqIdRef.current) {
                    setHasMore(false);
                    setError(e?.message || "Ошибка загрузки");
                }
            } finally {
                inflightRef.current = false;
                setLoading(false);
            }
        },
        [tab, auth, search, statusFilter, deleted, skip, hasMore, loading, adminId]
    );

    // first page + on filters change
    useEffect(() => {
        setRows([]);
        setTotal(0);
        setSkip(0);
        setHasMore(true);
        reqIdRef.current++; // invalidate old responses
        inflightRef.current = false;
        void load(true);
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [queryKey]);

    // lazy loading via IO — root = scroll container
    useEffect(() => {
        const root = listScrollRef.current;
        const target = loadMoreRef.current;
        if (!root || !target) return;

        const disabled = loading || !hasMore || !!error;
        if (disabled) return;

        const io = new IntersectionObserver(
            (entries) => {
                const vis = entries.some((e) => e.isIntersecting);
                if (vis) {
                    // догружаємо порцію
                    load(false);
                }
            },
            {
                root,
                rootMargin: "200px 0px 400px 0px",
                threshold: 0.01,
            }
        );

        io.observe(target);
        return () => io.disconnect();
    }, [load, loading, hasMore, error, rows.length]);

    const triggerSearch = () => setSearch(input.trim());

    // confirm actions
    const doConfirmAction = async () => {
        if (!confirm) return;
        const { entity, kind, row } = confirm;
        try {
            if (entity === "credit") {
                if (kind === "delete") await adminDeleteCredit({ token: auth, base: API, id: row.id });
                else await adminRestoreCredit({ token: auth, base: API, id: row.id });
            } else {
                if (kind === "delete") await adminDeleteClient({ token: auth, base: API, id: row.id });
                else await adminRestoreClient({ token: auth, base: API, id: row.id });
            }
            // full refresh
            setRows([]);
            setTotal(0);
            setSkip(0);
            setHasMore(true);
            reqIdRef.current++;
            inflightRef.current = false;
            await load(true);
        } catch (e) {
            console.error(e);
        } finally {
            setConfirm(null);
        }
    };

    const refresh = () => {
        setRows([]);
        setTotal(0);
        setSkip(0);
        setHasMore(true);
        reqIdRef.current++;
        inflightRef.current = false;
        void load(true);
    };

    const isFirstPageLoading = loading && skip === 0;
    const isFetchingMore = loading && skip > 0;

    return (
        <div className="relative flex h-[420px] sm:h-[440px] lg:h-[460px] flex-col rounded-[calc(theme(borderRadius.3xl)-1px)] bg-white/90 p-6 shadow-xl overflow-hidden backdrop-blur border border-transparent hover:border-[#E5E9F6]">
            <div className="mb-3 flex items-center justify-between">
                <div>
                    <div className="text-sm text-[#8F9BBA] font-bold">Список заявок</div>
                    <h3 className="text-2xl font-extrabold text-[#2B3674]">
                        {role === "admin" ? "Админ" : "Брокер"} • {tab === "credits" ? "кредиты" : "клиенты"}
                    </h3>
                </div>
                <button
                    onClick={refresh}
                    title="Обновить"
                    className="cursor-pointer p-2 rounded-lg text-[#7144ff] hover:bg-[#F4F7FE] transition"
                >
                    <RefreshCw size={18} className={loading ? "animate-spin" : ""} />
                </button>
            </div>

            {/* Tabs + фільтри */}
            <div className="mb-3 flex flex-row rounded-2xl p-1">
                <div className="flex flex-row items-center">
                    <button
                        onClick={() => setTab("credits")}
                        className={clsx(
                            "cursor-pointer flex items-center gap-2 rounded-xl px-4 py-2 text-sm",
                            tab === "credits" ? "bg-white shadow text-[#2B3674]" : "text-slate-600"
                        )}
                        title="Заявки"
                    >
                        <CheckCircle size={16} /> Заявки
                    </button>
                    <button
                        onClick={() => setTab("clients")}
                        className={clsx(
                            "cursor-pointer flex items-center gap-2 rounded-xl px-4 py-2 text-sm",
                            tab === "clients" ? "bg-white shadow text-[#2B3674]" : "text-slate-600"
                        )}
                        title="Клиенты"
                    >
                        <Users size={16} /> Клиенты
                    </button>
                </div>

                <div className="flex flex-row items-center">
                    {/* статус — лише для credits */}
                    {tab === "credits" && (
                        <div className="ml-3 flex flex-wrap items-center gap-2">
                            <select
                                value={statusFilter}
                                onChange={(e) => setStatusFilter(e.currentTarget.value as any)}
                                className="min-w-[180px] rounded-xl border border-slate-300 bg-white px-3 py-1.5 text-sm text-slate-700"
                                title="Статус заявки"
                            >
                                {STATUS_OPTIONS.map((o) => (
                                    <option key={o.value} value={o.value}>
                                        {o.label}
                                    </option>
                                ))}
                            </select>
                        </div>
                    )}

                    {/* фільтр deleted — і для credits, і для clients */}
                    {role === "admin" && (
                        <div className="ml-3">
                            <select
                                value={deleted}
                                onChange={(e) => setDeleted(e.currentTarget.value as DeletedFilter)}
                                className="min-w-[180px] rounded-xl border border-slate-300 bg-white px-3 py-1.5 text-sm text-slate-700"
                                title="Фильтр удаления"
                            >
                                <option value="all">Все</option>
                                <option value="active">Только активные</option>
                                <option value="only">Только удалённые</option>
                            </select>
                        </div>
                    )}
                </div>
            </div>

            {/* Search */}
            <div className="mb-3 grid grid-cols-1 gap-2 md:grid-cols-2">
                <div className="flex items-stretch gap-2">
                    <div className="relative flex-1">
                        <input
                            value={input}
                            onChange={(e) => setInput(e.currentTarget.value)}
                            onKeyDown={(e) => e.key === "Enter" && triggerSearch()}
                            placeholder={tab === "credits" ? "Поиск: ID/email/телефон/ФИО…" : "Поиск: email/телефон/ФИО…"}
                            className="w-full rounded-xl border border-slate-300 bg-slate-50 px-10 py-2 text-sm outline-none focus:border-[#7144ff]"
                        />
                        <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
                    </div>
                    <button
                        onClick={triggerSearch}
                        className="cursor-pointer shrink-0 rounded-xl bg-[#7144ff] px-4 py-2 text-sm font-semibold text-white hover:brightness-110"
                        title="Поиск"
                    >
                        Поиск
                    </button>
                </div>
            </div>

            {/* Error banner */}
            {error && (
                <div className="mb-3 rounded-md border border-rose-300 bg-rose-50 px-3 py-2 text-sm text-rose-700 flex items-center justify-between">
                    <span>{error}</span>
                    <button
                        onClick={() => {
                            setError(null);
                            refresh();
                        }}
                        className="rounded-lg border border-rose-300 bg-white/50 px-2 py-1 text-xs hover:bg-white"
                    >
                        Повторити
                    </button>
                </div>
            )}

            {/* List with own scroll */}
            <div className="flex-1 min-h-0 overflow-hidden rounded-2xl border border-slate-200 bg-white flex flex-col">                {/* table header */}
                <div className="sticky top-0 z-10 bg-white text-[#8F9BBA] border-b">
                    <table className="w-full text-sm">
                        <thead>
                        {tab === "credits" ? (
                            <tr>
                                <th className="py-3 pl-3 text-sm font-bold tracking-tight text-left">Дата</th>
                                <th className="py-3 pl-3 text-sm font-bold tracking-tight text-left">Клиент</th>
                                <th className="py-3 pl-3 text-sm font-bold tracking-tight text-left">Сумма</th>
                                <th className="py-3 pl-3 text-sm font-bold tracking-tight text-left">Согласовано</th>
                                <th className="py-3 pl-3 text-sm font-bold tracking-tight text-left">Статус</th>
                                <th className="py-3 pr-3 text-sm font-bold tracking-tight text-right">Действия</th>
                            </tr>
                        ) : (
                            <tr>
                                <th className="py-3 pl-3 text-sm font-bold tracking-tight text-left">ФИО</th>
                                <th className="py-3 pl-3 text-sm font-bold tracking-tight text-left">Телефон</th>
                                <th className="py-3 pl-3 text-sm font-bold tracking-tight text-left">Email</th>
                                <th className="py-3 pl-3 text-sm font-bold tracking-tight text-left">Адрес</th>
                                <th className="py-3 pr-3 text-sm font-bold tracking-tight text-right">Действия</th>
                            </tr>
                        )}
                        </thead>
                    </table>
                </div>

                {/* scrollable body */}
                <div ref={listScrollRef} className="custom-scrollbars min-h-0 flex-1 overflow-y-auto">
                    <table className="w-full text-sm">
                        <tbody className="text-[#2B3674] font-medium tracking-tight">
                        {rows.map((r) =>
                            tab === "credits" ? (
                                <CreditRow
                                    key={r.id}
                                    row={r}
                                    onOpen={() => setOpenEntity({ kind: "credit", data: r })}
                                    onDelete={() => setConfirm({ kind: "delete", entity: "credit", row: r })}
                                    onRestore={() => setConfirm({ kind: "restore", entity: "credit", row: r })}
                                />
                            ) : (
                                <ClientRow
                                    key={r.id}
                                    row={r}
                                    onOpen={() => setOpenEntity({ kind: "client", data: r })}
                                    onCreateCredit={() => setOpenCreateForClient(r)}
                                    onDelete={role === "admin" ? () => setConfirm({ kind: "delete", entity: "client", row: r }) : undefined}
                                    onRestore={role === "admin" ? () => setConfirm({ kind: "restore", entity: "client", row: r }) : undefined}
                                />
                            )
                        )}

                        {isFirstPageLoading && (
                            <tr>
                                <td colSpan={6} className="py-6 text-center text-slate-500">
                                    <Loader2 className="mr-2 inline h-4 w-4 animate-spin" /> Загрузка…
                                </td>
                            </tr>
                        )}

                        {!isFirstPageLoading && rows.length === 0 && (
                            <tr>
                                <td colSpan={6} className="py-6 text-center text-slate-500">
                                    Нет данных
                                </td>
                            </tr>
                        )}
                        </tbody>
                    </table>

                    {/* sentinel for IO inside scroll area */}
                    <div ref={loadMoreRef} className="h-10 w-full" />
                </div>

                {/* fetching more footer */}
                {isFetchingMore && !!rows.length && (
                    <div className="flex items-center justify-center gap-2 py-2 text-xs text-slate-500">
                        <Loader2 className="animate-spin" size={14} /> Подгружаем…
                    </div>
                )}
            </div>

            {/* Entity modal */}
            {openEntity && (
                <EntityModal
                    open={true}
                    kind={openEntity.kind}
                    entity={openEntity.data}
                    role={role}
                    token={auth}
                    base={API}
                    onClose={() => setOpenEntity(null)}
                    onChanged={() => {
                        setOpenEntity(null);
                        refresh();
                    }}
                />
            )}

            {/* Create-credit modal */}
            {openCreateForClient && (
                <CreateCreditModal
                    open
                    client={openCreateForClient}
                    token={auth}
                    base={API}
                    onClose={() => setOpenCreateForClient(null)}
                    onCreated={() => {
                        setOpenCreateForClient(null);
                        setTab("credits");
                        refresh();
                    }}
                />
            )}

            {/* Confirm */}
            {confirm && (
                <ConfirmModal
                    open={!!confirm}
                    title={
                        confirm?.kind === "delete"
                            ? confirm?.entity === "credit"
                                ? "Удалить кредит?"
                                : "Удалить клиента?"
                            : "Восстановить клиента?"
                    }
                    text={
                        confirm?.kind === "delete"
                            ? "Это мягкое удаление. Запись можно отфильтровать и восстановить (для клиентов)."
                            : "Запись будет помечена как активная."
                    }
                    confirmLabel={confirm?.kind === "delete" ? "Удалить" : "Восстановить"}
                    accent={confirm?.kind === "delete" ? "danger" : "primary"}
                    icon={<Trash2 size={16} />}
                    onClose={() => setConfirm(null)}
                    onConfirm={doConfirmAction}
                />
            )}

            {/* custom scrollbars */}
            <style jsx>{`
        .custom-scrollbars::-webkit-scrollbar {
          width: 10px;
        }
        .custom-scrollbars::-webkit-scrollbar-thumb {
          background: rgba(148, 163, 184, 0.6);
          border-radius: 9999px;
        }
        .custom-scrollbars::-webkit-scrollbar-track {
          background: transparent;
        }
      `}</style>
        </div>
    );
}
