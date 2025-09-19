'use client';

/**
 * fetchJSON — tiny fetch helper with robust 204/No-JSON handling.
 * --------------------------------------------------------------
 * - Throws a readable Error on non-2xx responses (tries to use `detail`).
 * - Returns `undefined` for 204/205 or when response has no JSON content-type.
 * - Keeps credentials and JSON headers by default.
 */

export async function fetchJSON<T = unknown>(url: string, init?: RequestInit): Promise<T> {
    const res = await fetch(url, {
        credentials: 'include',
        headers: { 'Content-Type': 'application/json', ...(init?.headers || {}) },
        ...init,
    });

    if (!res.ok) {
        let msg = `HTTP ${res.status}`;
        try {
            const j = await res.json();
            msg = j?.detail ?? msg;
        } catch {}
        throw new Error(msg);
    }

    const ct = res.headers.get('content-type') || '';
    if (res.status === 204 || res.status === 205 || !ct.includes('application/json')) {
        return undefined as T;
    }
    return (await res.json()) as T;
}
