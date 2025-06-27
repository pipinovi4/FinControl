import {useQuery} from "@tanstack/react-query";

export interface FieldConfig {
    name: string;
    label: string;
    type?: "text" | "password" | "email";
    required?: boolean;
    placeholder?: string;
}

export type SchemaFieldMap = Record<string, string>;

const fetchRoutesInfo = async (): Promise<Response> => {
    return await fetch("http://127.0.0.1:8000/api/system/routes-info")
};

export const useSchemaFields = (schemaName: string) => {
    return useQuery({
        queryKey: ["routes-info", schemaName],
        queryFn: () => fetchRoutesInfoFor(schemaName),
        staleTime: 5 * 60 * 1000,
    });
};

// виділений хук + функція для параметра
const fetchRoutesInfoFor = async (schemaName: string): Promise<SchemaFieldMap> => {
    const res = await fetch("http://127.0.0.1:8000/api/system/routes-info");
    const data = await res.json();
    const target = data.find((route: any) => route.input_schema === schemaName);
    return target?.schema_fields ?? {};
};

export const useRoutesInfo = () => {
    return useQuery({
        queryKey: ["routes-info", "auth-login-admin"],
        queryFn: fetchRoutesInfo,
        staleTime: 5 * 60 * 1000,
    });
};
