// @ts-ignore
import { FieldDef } from "./fields";
// @ts-ignore
import { ClientOut, toRuDateTime } from "./types";

// @ts-ignore
export const clientFields: FieldDef<ClientOut>[] = [
    { key: "full_name",    label: "ФИО",            type: "text",   editable: true },
    { key: "email",        label: "Email",          type: "text",   editable: true },
    { key: "phone_number", label: "Телефон",        type: "text",   editable: true },
    { key: "fact_address", label: "Адрес (факт.)",  type: "text",   editable: true },
    { key: "created_at",   label: "Создан",         type: "read",   format: (v) => toRuDateTime(v) },
    { key: "is_deleted",   label: "Статус записи",  type: "read",   format: (v) => (v ? "Удалён" : "Активен") },
];
