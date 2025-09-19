/* ───────────────────────────── Базові типи ───────────────────────────── */

export type Row = { id: string } & Record<string, any>;

export type RowMapper = (raw: any) => Row;

/* ───────────────────────────── Modal bucket ──────────────────────────── */

export type ModalBucketState = {
    data   : Row[];
    skip   : number;
    total  : number;
    loading: boolean;
    done   : boolean;
    error  : string | null;
};

/* ───────────────────────────── Props таблиці ─────────────────────────── */

export type UserTableProps = {
    labels         : string[];
    userBucketURL  : string[];
    getFullUserURL : string[];
    requiresId     : boolean;

    tableHeads : string[][];     // заголовки th (за ролями)
    rowMappers : RowMapper[];    // конвертери raw → Row (за ролями)
    colKeys?: string[][];

    pageSize?           : number;
    fixed?              : boolean;
    expandedModalTitle? : string;
};

/* ──────────────────────────── Функції-мапери ─────────────────────────── */

import { formatDate } from './utils';

/* клієнт */
export const mapWorkerClient: RowMapper = (r) => ({
    id    : r.id,
    name  : r.full_name    ?? '—',
    phone : r.phone_number ?? '—',
    fact_address: r.fact_address,
    date  : formatDate(r.taken_at_worker) ?? '-',
});

export const mapBrokerClient: RowMapper = (r) => ({
    id    : r.id,
    name  : r.full_name    ?? '—',
    phone : r.phone_number ?? '—',
    fact_address: r.fact_address,
    date  : formatDate(r.taken_at_broker) ?? '-',
});

export const mapAdminClient: RowMapper = (r) => ({
    id    : r.id,
    name  : r.full_name    ?? '—',
    phone : r.phone_number ?? '—',
    fact_address: r.fact_address,
    date  : formatDate(r.created_at) ?? '-',
});

/* працівник */
export const mapWorker: RowMapper = (r) => ({
    id   : r.id,
    email: r.email    ?? '—',
    user : r.username ?? '—',
    date : formatDate(r.created_at) ?? '-',
});

/* брокер */
export const mapBroker: RowMapper = (r) => ({
    id     : r.id,
    email  : r.email            ?? '—',
    company: r.company_name     ?? '—',
    region : r.region?.join(', ') ?? '—',
    date   : formatDate(r.created_at) ?? '-',
});

/* дефолт, якщо мапер не передали */
export const defaultMapper: RowMapper = (r) => ({
    id: r.id ?? (typeof crypto?.randomUUID === 'function'
        ? crypto.randomUUID()
        : Math.random().toString(36).slice(2)),
    ...r,
});

/* ───────────────────────────── Хелпери ───────────────────────────── */

export const formatMoney = (n?: number | null, currency = "RUB") =>
    typeof n === "number"
        ? n.toLocaleString("ru-RU", {
            style: "currency",
            currency,
            maximumFractionDigits: 0,
        })
        : "—";

/* кредит */
export const mapCreditRow: RowMapper = (r) => ({
    id      : r.id,
    date    : formatDate(r.issued_at) ?? "-",
    client  : r.client?.full_name
        ?? r.client_full_name
        ?? (r.client_id ? `${String(r.client_id).slice(0, 8)}…` : "—"),
    amount   : formatMoney(r.amount),
    approved : formatMoney(r.approved_amount),
    status   : r.status ?? "new",
});

/* ────────────────────────────── Константи ────────────────────────────── */

export const ROW_HEIGHT = 48;
