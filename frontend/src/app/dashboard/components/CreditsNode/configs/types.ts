"use client";

/* Shared types and tiny helpers */

export type Role = "admin" | "broker";

// statuses (оновлені)
export type CreditStatus = "new" | "treatment" | "approved" | "completed";

export type CreditOut = {
    id: string;
    client_id: string;
    broker_id?: string | null;
    worker_id?: string | null;
    issued_at: string; // ISO
    amount: number;
    approved_amount?: number | null;
    monthly_payment?: number | null;
    bank_name?: string | null;
    first_payment_date?: string | null; // ISO
    status: CreditStatus;
    comment?: string | null;
    comments?: { text: string; created_at?: string }[];
    is_deleted?: boolean;
};

export type CreditsPage = { credits: CreditOut[]; total: number };

export type ClientOut = {
    id: string;
    full_name: string;
    email: string;
    phone_number: string;
    broker_id?: string | null;
    fact_address?: string | null;
    created_at?: string | null;
    is_deleted?: boolean;
};

export type ClientsPage = { clients: ClientOut[]; total: number };

export const statusLabel: Record<CreditStatus, string> = {
    new: "Новая",
    treatment: "На доработку",
    approved: "Согласовано",
    completed: "Выдано",
};

// allowed transitions (UI guard — бек все одно перевіряє)
export const allowChangeByRole: Record<
    Role,
    Partial<Record<CreditStatus, CreditStatus[]>>
> = {
    broker: {
        new: ["approved", "treatment"],
        approved: ["treatment"],
        treatment: ["approved"],
        completed: [],
    },
    admin: {
        new: [],
        treatment: [],
        approved: ["completed"],
        completed: [],
    },
};

// money formatter
export function formatMoney(n?: number | null) {
    return typeof n === "number"
        ? n.toLocaleString("ru-RU", {
            style: "currency",
            currency: "RUB",
            maximumFractionDigits: 0,
        })
        : "—";
}

// date helpers
export const toRuDate = (iso?: string | null) =>
    iso ? new Date(iso).toLocaleDateString("ru-RU") : "—";
export const toRuDateTime = (iso?: string | null) =>
    iso ? new Date(iso).toLocaleString("ru-RU") : "—";
