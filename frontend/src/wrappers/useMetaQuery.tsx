import {InputOf, metaFetch, OutputOf} from "@/lib/metaFetch";
import {useQuery, UseQueryOptions} from "@tanstack/react-query";


export function useMetaQuery<P extends string>(
    path: P,
    body?: InputOf<P>,
    options?: UseQueryOptions<OutputOf<P>>
) {
    return useQuery({
        queryKey: [path, body],
        queryFn: () => metaFetch(path, body),
        ...options,
    });
}
