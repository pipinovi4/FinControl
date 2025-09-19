import { useCallback, useEffect, useRef, useState } from 'react';
import UserStorage from '@/services/UserStorage';
import { parseBucketResponse } from '../utils';
import {
    RowMapper,
    defaultMapper,
    ModalBucketState,
} from '../types';

/** Пагіновані «бочки» для модального вікна */
export function useModalBuckets(
    labels        : string[],
    userBucketURL : string[],
    requiresId    : boolean | undefined,
    pageSize      : number,
    searchTerm    : string,
    open          : boolean,
    activeRole    : number,
    rowMappers?   : RowMapper[],
) {
    /* ---------- local state ---------- */
    const [buckets, _setBuckets] = useState<ModalBucketState[]>(
        labels.map(() => ({
            data: [], skip: 0, total: 0, loading: false, done: false, error: null,
        }))
    );

    /* ref-дзеркало, щоби бачити актуальний state у колбеках */
    const bucketsRef = useRef(buckets);
    const setBuckets = (fn: (p: ModalBucketState[]) => ModalBucketState[]) => {
        _setBuckets(p => {
            const n = fn(p);
            bucketsRef.current = n;
            return n;
        });
    };

    /* ---------- debounce live search ---------- */
    const debounceRef = useRef<NodeJS.Timeout | null>(null);

    /* ---------- головний фетчер ---------- */
    const fetchBucket = useCallback(
        async (roleIdx: number, reset = false) => {
            const base = userBucketURL[roleIdx];
            if (!base) return;

            /* optimistic */
            setBuckets(prev => {
                const next = [...prev];
                const b    = next[roleIdx];
                next[roleIdx] = {
                    ...b,
                    loading: true,
                    error  : null,
                    ...(reset ? { data: [], skip: 0, total: 0, done: false } : {}),
                };
                return next;
            });

            try {
                /* skip/limit */
                // const current = reset ? { skip: 0 } : bucketsRef.current[roleIdx];
                const current = reset
                     ? { skip: 0 }
                         : bucketsRef.current[roleIdx];
                const me      = requiresId ? UserStorage.get() : null;

                let url = base;
                // @ts-ignore
                if (requiresId && me?.id) url = url.replace(/\/?$/, `/${me.id}`);

                const p = new URLSearchParams({
                    skip : String(current.skip),
                    limit: String(pageSize),
                    ...(searchTerm.trim() ? { q: searchTerm.trim() } : {}),
                });
                url += `?${p.toString()}`;

                /* fetch */
                const res = await fetch(url);
                if (!res.ok) throw new Error(`HTTP ${res.status}`);

                const json              = await res.json();
                const { list, total }   = parseBucketResponse(json);
                const mapper            = rowMappers?.[roleIdx] ?? defaultMapper;
                const incoming          = list.map(mapper);

                setBuckets(prev => {
                    const next = [...prev];
                    const old  = next[roleIdx];

                    // const uniq = incoming.filter(r => !old.data.some(o => o.id === r.id));
                    // const data = reset ? uniq : [...old.data, ...uniq];
                    // const done = data.length >= (total || old.total);

                    const uniq = incoming.filter(r => !old.data.some(o => o.id === r.id));
                    const data = reset ? uniq : [...old.data, ...uniq];

                    /* 👇 нова умова — "повна" сторінка вже завантажена */
                    const done = incoming.length < pageSize || data.length >= (total || old.total);

                    next[roleIdx] = {
                        ...old,
                        loading: false,
                        data,
                        skip  : data.length,
                        total : total || old.total,
                        done,
                        error : null,
                    };
                    return next;
                });
            } catch (e: any) {
                setBuckets(prev => {
                    const next = [...prev];
                    const old  = next[roleIdx];
                    next[roleIdx] = { ...old, loading: false, error: e.message || 'Fetch error' };
                    return next;
                });
            }
        },
        [userBucketURL, requiresId, pageSize, searchTerm, rowMappers]
    );

    /* auto-fetch при відкритті / зміні роли */
    useEffect(() => {
        if (!open) return;
        const b = bucketsRef.current[activeRole];
        if (!b.loading && b.data.length === 0) fetchBucket(activeRole, true);
    }, [open, activeRole, fetchBucket]);

    /* debounce для live-search */
    useEffect(() => {
        if (!open) return;
        if (debounceRef.current) clearTimeout(debounceRef.current);
        debounceRef.current = setTimeout(() => fetchBucket(activeRole, true), 400);
        return () => { if (debounceRef.current) clearTimeout(debounceRef.current); };
    }, [searchTerm, activeRole, fetchBucket]);

    return { buckets, fetchBucket };
}
