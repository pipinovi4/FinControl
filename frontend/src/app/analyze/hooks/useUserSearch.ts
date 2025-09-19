'use client';

import { useState, useCallback } from 'react';
import type { SearchField } from '../config/analyzeConfig';
import UserStorage from '@/services/UserStorage';

export type UserRow = {
    id: string;
    full_name?: string;
    company_name?: string;
    email?: string;
    phone_number?: string;
    region?: string;
    username?: string;
    created_at?: string;
    taken_at_worker?: string;
    taken_at_broker?: string;
    is_deleted?: boolean; // ← NEW
    is_active?: boolean;  // (если есть на бэке)
};

export const useUserSearch = (baseEndpoint: string, field: SearchField) => {
    const [loading, setLoading] = useState(false);
    const [rows, setRows] = useState<UserRow[]>([]);
    const [error, setError] = useState<string | null>(null);

    // @ts-ignore
    const userId = (UserStorage.get()?.id as string) || null;

    const runSearch = useCallback(
        async (value: string, extraParams?: Record<string, string | boolean | null>) => {
            if (!value.trim()) return [];

            setLoading(true);
            setError(null);

            try {
                let base = baseEndpoint;
                if (userId) base += userId;

                const url = new URL(base);
                url.searchParams.set(field.param, value.trim());
                // add extra params (e.g., is_deleted)
                if (extraParams) {
                    Object.entries(extraParams).forEach(([k, v]) => {
                        if (v === null || v === undefined || v === '') return;
                        url.searchParams.set(k, String(v));
                    });
                }

                const res = await fetch(url.toString(), { credentials: 'include' });
                if (!res.ok) throw new Error(res.statusText);

                const json = await res.json();
                const list: UserRow[] = Array.isArray(json) ? json : json.clients ?? json.results ?? json.items ?? json.users ?? [];

                const norm = list.map((u) => ({
                    ...u,
                    created_at: u.created_at || u.taken_at_worker || u.taken_at_broker || '',
                }));

                setRows(norm);
                return norm;
            } catch (e: any) {
                setError(e.message || 'Network error');
                setRows([]);
                return [];
            } finally {
                setLoading(false);
            }
        },
        [baseEndpoint, field.param, userId]
    );

    return { loading, rows, error, setRows, runSearch };
};
