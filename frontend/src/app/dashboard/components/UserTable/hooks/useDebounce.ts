'use client';
import { useEffect, useState } from 'react';

/**
 * Повертає «задебаунсене» значення через delay мілісекунд.
 *
 * @param value   будь-яке значення (string, number, object…)
 * @param delay   затримка у ms (default: 400)
 *
 * @example
 *   const debouncedSearch = useDebounce(search, 400);
 */
export const useDebounce = <T>(value: T, delay = 1000): T => {
    const [debounced, setDebounced] = useState<T>(value);

    useEffect(() => {
        const id = setTimeout(() => setDebounced(value), delay);
        return () => clearTimeout(id);
    }, [value, delay]);

    return debounced;
};
