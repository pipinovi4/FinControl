'use client';

import { useEffect, useState, RefObject } from 'react';

/**
 * Повертає true, коли target-елемент (sentinel) перетинає viewport
 * указаного scroll-container (rootRef). Якщо rootRef не передати —
 * спостерігаємо за вікном браузера.
 *
 * @param targetRef  ref на sentinel div
 * @param rootRef    ref на scroll-контейнер
 * @param options    IntersectionObserverInit без поля root
 */
export const useIntersectionObserver = (
    targetRef: RefObject<Element | null>,
    rootRef?:  RefObject<Element | null>,
    options:   Partial<Omit<IntersectionObserverInit, 'root'>> = {},
): boolean => {
    const [intersecting, setIntersecting] = useState(false);

    useEffect(() => {
        const target = targetRef.current;
        if (!target) return;

        const observer = new IntersectionObserver(
            ([entry]) => setIntersecting(entry.isIntersecting),
            {
                root        : rootRef?.current ?? null,
                rootMargin  : options.rootMargin ?? '0px',
                threshold   : options.threshold  ?? 0,
            },
        );

        observer.observe(target);
        return () => observer.disconnect();
    }, [
        targetRef,
        rootRef?.current,          // важливо: ref.current у залежностях
        options.rootMargin,
        options.threshold,
    ]);

    return intersecting;
};
