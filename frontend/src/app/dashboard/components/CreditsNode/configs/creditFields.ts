import { FieldDef } from "./fields";
import { CreditOut, formatMoney, toRuDateTime, statusLabel } from "./types";

export const creditFields = (clientName: string): FieldDef<CreditOut>[] => [
    { key: "amount",             label: "Сумма заявки",        type: "read",   format: (v) => formatMoney(v) },
    { key: "client_id",          label: "Клиент",               type: "read",   format: () => clientName },
    { key: "issued_at",          label: "Выдача",               type: "read",   format: (v) => toRuDateTime(v) },
    { key: "approved_amount",    label: "Согласованная сумма",  type: "number", editable: true },
    { key: "monthly_payment",    label: "Ежемесячный платёж",   type: "number", editable: true },
    { key: "bank_name",          label: "Банк",                 type: "text",   editable: true },
    { key: "first_payment_date", label: "Первая дата оплаты",   type: "text",   editable: true },
    { key: "comment",            label: "Комментарий",          type: "text",   editable: true },
    { key: "status",             label: "Текущий статус",       type: "read",   format: (v) => statusLabel[v as keyof typeof statusLabel] ?? String(v) },
    { key: "is_deleted",         label: "Статус записи",        type: "read",   format: (v) => (v ? "Удалён" : "Активен") },
];
