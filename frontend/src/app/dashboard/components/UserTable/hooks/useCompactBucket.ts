import { useCallback, useEffect, useState } from 'react';
import UserStorage from '@/services/UserStorage';
import { parseBucketResponse } from '../utils';
import { Row, RowMapper, defaultMapper } from '../types';

export function useCompactBucket(
    bucketUrl : string | undefined,
    requiresId: boolean | undefined,
    skip      : number,
    pageSize  : number,
    rowMapper : RowMapper = defaultMapper        // ← fallback
) {
    const [rows   , setRows  ] = useState<Row[]>([]);
    const [total  , setTotal ] = useState(0);
    const [loading, setLoad  ] = useState(false);
    const [error  , setError ] = useState<string | null>(null);

    const fetchData = useCallback(async () => {
        if (!bucketUrl) return;

        setLoad(true);
        setError(null);

        try {
            const me       = requiresId ? UserStorage.get() : null;
            let   url      = bucketUrl;
            // @ts-ignore – id є не у всіх типів юзерів
            if (requiresId && me?.id) url = url.replace(/\/?$/, `/${me.id}`);
            url += `?skip=${skip}&limit=${pageSize}`;

            const res = await fetch(url);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);

            const json          = await res.json();
            const { list, total } = parseBucketResponse(json);

            setRows(list.map(rowMapper));
            setTotal(total);
        } catch (e: any) {
            setError(e.message ?? 'Fetch error');
            setRows([]);
            setTotal(0);
        } finally {
            setLoad(false);
        }
    }, [bucketUrl, requiresId, skip, pageSize, rowMapper]);

    useEffect(() => { fetchData(); }, [fetchData]);

    return { rows, total, loading, error, refetch: fetchData };
}
