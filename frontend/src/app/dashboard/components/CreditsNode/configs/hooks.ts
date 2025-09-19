import { useEffect, useRef, useState } from "react";

export function useDebounce<T>(value: T, ms = 400) {
    const [v, setV] = useState(value);
    useEffect(() => {
        const t = setTimeout(() => setV(value), ms);
        return () => clearTimeout(t);
    }, [value, ms]);
    return v;
}

export function useInfiniteScroll(cb: () => void, disabled?: boolean) {
    const ref = useRef<HTMLDivElement | null>(null);
    useEffect(() => {
        if (disabled) return;
        const el = ref.current;
        if (!el) return;
        const io = new IntersectionObserver(
            (entries) => entries.forEach((e) => e.isIntersecting && cb()),
            { rootMargin: "600px" }
        );
        io.observe(el);
        return () => io.disconnect();
    }, [cb, disabled]);
    return ref;
}
