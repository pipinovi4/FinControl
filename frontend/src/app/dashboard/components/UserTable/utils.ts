/* utils.ts
 * --------------------------------------------------------------
 *  🔹 formatDate     –  ISO → DD.MM.YYYY
 *  🔹 mapClient      –  raw → Row   (роль "client")
 *  🔹 mapWorker      –  raw → Row   (роль "worker")
 *  🔹 mapBroker      –  raw → Row   (роль "broker")
 *  🔹 defaultMapper  –  fallback-конвертер
 *  🔹 mapRawToRows   –  thin-wrapper навколо defaultMapper
 *  🔹 parseBucketResponse –  { list, total } з будь-якого бек-формату
 * -------------------------------------------------------------- */

import { Row } from './types';

/* ─────────────── helpers ─────────────── */

/** ISO-рядок → "DD.MM.YYYY" або "—" */
export const formatDate = (iso?: string): string => {
    if (!iso) return '—';
    const d = new Date(iso);
    if (Number.isNaN(d.getTime())) return 'XUY-MM-DD';
    return `${d.getDate().toString().padStart(2, '0')}.` +
        `${(d.getMonth() + 1).toString().padStart(2, '0')}.` +
        d.getFullYear();
};

/* ─────────────── Row-мапери для ролей ─────────────── */

/** fallback, якщо не передали спеціальний mapper */
export const defaultMapper = (r: any): Row => ({
    ...r,
    id: r.id ??
        (typeof crypto?.randomUUID === 'function'
            ? crypto.randomUUID()
            : Math.random().toString(36).slice(2)),
});

/** Залишив для зворотної сумісності: raw[] → Row[] */
export const mapRawToRows = (raw: any[]): Row[] => raw.map(defaultMapper);

/* ─────────────── backend → { list, total } ─────────────── */

/**
 *  Підтримує формати:
 *   – plain array (сервер віддав одразу масив)
 *   – { clients: [...], total }
 *   – { items: [...], total }
 *   – { workers: [...] }
 *   – { brokers: [...] }
 *   – { value: [...] }
 *   – { results: [...] }  // на всяк випадок
 */
export const parseBucketResponse = (
    j: any,
): { list: any[]; total: number } => {
    /* 1) сервер прислав одразу масив */
    if (Array.isArray(j)) {
        return { list: j, total: j.length };
    }

    /* 2) знайти перший ключ, де лежить масив */
    const keys = [
        'clients',
        'items',
        'value',
        'workers',
        'brokers',
        'results',
    ] as const;

    const found = keys.find((k) => Array.isArray(j?.[k]));
    const list: any[] = found ? j[found] : [];

    /* 3) total */
    const total = typeof j?.total === 'number' ? j.total : list.length;

    return { list, total };
};
