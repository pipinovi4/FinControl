// fields.ts — спільні типи опису полів для модалки
export type FieldType = "read" | "text" | "number" | "date";

export type FieldDef<T> = {
    key: keyof T & string;
    label: string;
    type: FieldType;
    editable?: boolean;
    format?: (val: any, entity: T) => React.ReactNode;
    placeholder?: string;
};
