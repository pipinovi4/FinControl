import { useCallback, useEffect, useState } from 'react';

export interface UserDetailState {
    data: Record<string, any> | null;
    loading: boolean;
    error: string | null;
}

export function useUserDetails(
    baseUrl: string | undefined,
    id: string | null,
    enabled: boolean
) {
    const [state, setState] = useState<UserDetailState>({
        data: null,
        loading: false,
        error: null
    });

    const fetchDetails = useCallback(async () => {
        if (!enabled || !baseUrl || !id) return;
        let url = baseUrl;
        // очікуємо baseUrl типу ".../client/" і тоді додаємо id
        if (!url.endsWith('/')) url += '/';
        url += id;

        setState(s => ({ ...s, loading: true, error: null }));
        try {
            const res = await fetch(url);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            const json = await res.json();

            // тут можна зробити будь-яке нормалізування
            setState({ data: json, loading: false, error: null });
        } catch (e: any) {
            setState({ data: null, loading: false, error: e.message || 'Fetch error' });
        }
    }, [baseUrl, id, enabled]);

    useEffect(() => {
        fetchDetails();
    }, [fetchDetails]);

    return {
        ...state,
        refetch: fetchDetails
    };
}
