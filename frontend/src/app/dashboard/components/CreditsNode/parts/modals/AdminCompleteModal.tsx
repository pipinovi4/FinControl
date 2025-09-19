"use client";

import React, { useEffect, useMemo, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { Calendar, X } from "lucide-react";

/* ---------------- Types ---------------- */
export type AdminCompletePayload = {
    approved_amount: number;
    monthly_payment: number;
    bank_name: string;
    first_payment_date: string; // ISO local ("YYYY-MM-DDTHH:mm")
    comment?: string;
};

type Props = {
    open: boolean;
    onClose: () => void;
    onSubmit: (data: AdminCompletePayload) => void;
    loading?: boolean;
    initial?: Partial<AdminCompletePayload>;
    title?: string;
};

/* ---------------- Small helpers ---------------- */
// pads number to 2 digits
const dd = (n: number) => String(n).padStart(2, "0");
// format Date -> "YYYY-MM-DDTHH:mm"
function toLocalISO(dt: Date) {
    return `${dt.getFullYear()}-${dd(dt.getMonth() + 1)}-${dd(dt.getDate())}T${dd(
        dt.getHours()
    )}:${dd(dt.getMinutes())}`;
}

/* ---------------- Inline DateTime picker (popover) ---------------- */
// UI is inspired by PeriodPicker: trigger button + light popover
function DateTimePopover({
                             value,
                             onChange,
                             invalid,
                             placeholder = "Выберите дату и время",
                         }: {
    value?: string;
    onChange: (next: string) => void;
    invalid?: boolean;
    placeholder?: string;
}) {
    const [open, setOpen] = useState(false);
    const [draft, setDraft] = useState<string>(value ?? "");

    // keep local draft in sync when external value changes
    useEffect(() => setDraft(value ?? ""), [value]);

    const shown =
        value && value.length
            ? new Date(value).toLocaleString()
            : placeholder;

    const border = invalid
        ? "border-rose-300 hover:border-rose-400"
        : "border-slate-300 hover:border-[#C7CBE3]";

    return (
        <div className="relative">
            <button
                type="button"
                onClick={() => setOpen(true)}
                className={`w-full cursor-pointer flex items-center justify-between rounded-xl bg-white px-3 py-2 text-sm outline-none border ${border}`}
                aria-haspopup="dialog"
                aria-expanded={open}
            >
        <span className={`truncate ${value ? "text-[#2B3674]" : "text-slate-400"}`}>
          {shown}
        </span>
                <Calendar size={16} className="shrink-0 text-[#2B3674]" />
            </button>

            <AnimatePresence>
                {open && (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.98 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.98 }}
                        className="absolute z-50 mt-2 w-[min(320px,92vw)] rounded-xl border border-[#E4E9F2] bg-white p-4 shadow-xl right-0"
                        role="dialog"
                        aria-modal
                    >
                        <div className="mb-3 flex items-center justify-between">
                            <div className="text-sm font-semibold text-[#2B3674]">Дата и время</div>
                            <button
                                type="button"
                                onClick={() => setOpen(false)}
                                className="rounded-md p-1 hover:bg-[#F4F7FE]"
                                aria-label="Закрыть"
                            >
                                <X size={16} />
                            </button>
                        </div>

                        {/* native calendar/time control inside a neat popover */}
                        <input
                            type="datetime-local"
                            className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm outline-none focus:border-[#7144ff]"
                            value={draft}
                            onChange={(e) => setDraft(e.currentTarget.value)}
                            // min now (optional, comment out if not needed)
                            // min={toLocalISO(new Date())}
                        />

                        <div className="mt-4 flex justify-end gap-2">
                            <button
                                type="button"
                                onClick={() => {
                                    setDraft(value ?? "");
                                    setOpen(false);
                                }}
                                className="rounded-lg border border-slate-300 bg-white px-3 py-1.5 text-sm hover:bg-slate-50"
                            >
                                Отмена
                            </button>
                            <button
                                type="button"
                                onClick={() => {
                                    // if empty — set to now
                                    const next = draft?.trim() || toLocalISO(new Date());
                                    onChange(next);
                                    setOpen(false);
                                }}
                                className="rounded-lg bg-[#7144ff] px-3 py-1.5 text-sm font-semibold text-white hover:brightness-110"
                            >
                                Готово
                            </button>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}

/* ---------------- Main modal ---------------- */
export default function AdminCompleteModal({
                                               open,
                                               onClose,
                                               onSubmit,
                                               loading,
                                               initial,
                                               title = "Данные для статуса «Выдано»",
                                           }: Props) {
    // form state
    const [approvedAmount, setApprovedAmount] = useState<string>(
        initial?.approved_amount?.toString() ?? ""
    );
    const [monthlyPayment, setMonthlyPayment] = useState<string>(
        initial?.monthly_payment?.toString() ?? ""
    );
    const [bankName, setBankName] = useState<string>(initial?.bank_name ?? "");
    const [firstPaymentDate, setFirstPaymentDate] = useState<string>(
        initial?.first_payment_date ?? ""
    );
    const [comment, setComment] = useState<string>(initial?.comment ?? "");

    // reset when closing
    useEffect(() => {
        if (!open) {
            setApprovedAmount(initial?.approved_amount?.toString() ?? "");
            setMonthlyPayment(initial?.monthly_payment?.toString() ?? "");
            setBankName(initial?.bank_name ?? "");
            setFirstPaymentDate(initial?.first_payment_date ?? "");
            setComment(initial?.comment ?? "");
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [open]);

    // validation (only border highlight + disabled button)
    const errors = useMemo(() => {
        const e: Record<string, boolean> = {};
        const amt = Number(approvedAmount);
        const mp = Number(monthlyPayment);
        e.approved_amount = !approvedAmount || isNaN(amt) || amt <= 0;
        e.monthly_payment = !monthlyPayment || isNaN(mp) || mp <= 0;
        e.bank_name = !bankName.trim();
        e.first_payment_date = !firstPaymentDate;
        return e;
    }, [approvedAmount, monthlyPayment, bankName, firstPaymentDate]);

    const disabled =
        (loading ?? false) ||
        errors.approved_amount ||
        errors.monthly_payment ||
        errors.bank_name ||
        errors.first_payment_date;

    const submit = () => {
        if (disabled) return;
        onSubmit({
            approved_amount: Number(approvedAmount),
            monthly_payment: Number(monthlyPayment),
            bank_name: bankName.trim(),
            first_payment_date: firstPaymentDate,
            comment: comment.trim() || undefined,
        });
    };

    return (
        <AnimatePresence>
            {open && (
                <motion.div
                    className="fixed inset-0 z-[80] flex items-center justify-center bg-black/40 backdrop-blur-sm"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    onClick={onClose}
                    role="dialog"
                    aria-modal
                >
                    <motion.div
                        className="w-[min(720px,96vw)] rounded-3xl border border-slate-200 bg-white p-6 shadow-2xl"
                        initial={{ scale: 0.94, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        exit={{ scale: 0.94, opacity: 0 }}
                        onClick={(e) => e.stopPropagation()}
                    >
                        {/* Header */}
                        <div className="mb-4 flex items-center justify-between">
                            <h3 className="text-xl font-extrabold text-[#2B3674]">{title}</h3>
                            <button
                                className="rounded-lg border border-slate-300 bg-white/80 px-3 py-1 text-sm hover:bg-slate-50"
                                onClick={onClose}
                            >
                                Закрыть
                            </button>
                        </div>

                        {/* Form */}
                        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                            <Field label="Согласованная сумма" required invalid={errors.approved_amount}>
                                <input
                                    type="number"
                                    min={0}
                                    step="0.01"
                                    className={`w-full rounded-xl bg-white px-3 py-2 text-sm outline-none border ${
                                        errors.approved_amount
                                            ? "border-rose-300 focus:border-rose-400"
                                            : "border-slate-300 focus:border-[#7144ff]"
                                    }`}
                                    value={approvedAmount}
                                    onChange={(e) => setApprovedAmount(e.currentTarget.value)}
                                    placeholder="Напр., 1500000"
                                />
                            </Field>

                            <Field label="Ежемесячный платёж" required invalid={errors.monthly_payment}>
                                <input
                                    type="number"
                                    min={0}
                                    step="0.01"
                                    className={`w-full rounded-xl bg-white px-3 py-2 text-sm outline-none border ${
                                        errors.monthly_payment
                                            ? "border-rose-300 focus:border-rose-400"
                                            : "border-slate-300 focus:border-[#7144ff]"
                                    }`}
                                    value={monthlyPayment}
                                    onChange={(e) => setMonthlyPayment(e.currentTarget.value)}
                                    placeholder="Напр., 25000"
                                />
                            </Field>

                            <Field label="Банк" required invalid={errors.bank_name}>
                                <input
                                    className={`w-full rounded-xl bg-white px-3 py-2 text-sm outline-none border ${
                                        errors.bank_name
                                            ? "border-rose-300 focus:border-rose-400"
                                            : "border-slate-300 focus:border-[#7144ff]"
                                    }`}
                                    value={bankName}
                                    onChange={(e) => setBankName(e.currentTarget.value)}
                                    placeholder="Название банка"
                                />
                            </Field>

                            <Field label="Первая дата оплаты" required invalid={errors.first_payment_date}>
                                <DateTimePopover
                                    value={firstPaymentDate}
                                    onChange={setFirstPaymentDate}
                                    invalid={errors.first_payment_date}
                                    placeholder="Выберите дату и время"
                                />
                            </Field>

                            <div className="sm:col-span-2">
                                <div className="mb-1 text-xs font-medium text-[#8F9BBA]">Комментарий</div>
                                <input
                                    className="w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm outline-none focus:border-[#7144ff]"
                                    value={comment}
                                    onChange={(e) => setComment(e.currentTarget.value)}
                                    placeholder="Необязательно"
                                />
                            </div>
                        </div>

                        {/* Footer */}
                        <div className="mt-5 flex justify-end gap-2">
                            <button
                                className="rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm hover:bg-slate-50"
                                onClick={onClose}
                            >
                                Отмена
                            </button>
                            <button
                                className="rounded-xl bg-[#7144ff] text-white px-3 py-2 text-sm hover:brightness-110 disabled:opacity-60"
                                disabled={disabled}
                                onClick={submit}
                            >
                                Подтвердить
                            </button>
                        </div>
                    </motion.div>
                </motion.div>
            )}
        </AnimatePresence>
    );
}

/* ---------------- UI-only Field wrapper ---------------- */
function Field({
                   label,
                   required,
                   invalid,
                   children,
               }: {
    label: string;
    required?: boolean;
    invalid?: boolean;
    children: React.ReactNode;
}) {
    return (
        <div>
            <div className="mb-1 text-xs font-medium text-[#8F9BBA]">
                {label}
                {required && <span className="ml-1 text-rose-500">*</span>}
            </div>
            {children}
            {/* visually-hidden hint; no red text in UI */}
            {invalid ? <div className="sr-only">Поле заполнено некорректно</div> : null}
        </div>
    );
}
