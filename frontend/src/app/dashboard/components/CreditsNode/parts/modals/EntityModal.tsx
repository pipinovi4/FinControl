"use client";

import React, { useEffect, useMemo, useState } from "react";
import { createPortal } from "react-dom";
import { AnimatePresence, motion } from "framer-motion";

import ConfirmModal from "./CofirmModal";
import BrokerCommentModal from "./BrokerCommentModal";
import AdminCompleteModal, { AdminCompletePayload } from "./AdminCompleteModal";

import type { Role, CreditOut, ClientOut, CreditStatus } from "../../configs/types";
import { statusLabel, allowChangeByRole } from "../../configs/types";

import {
    adminChangeStatus,
    adminUpdateCredit,
    adminUpdateClient,
    fetchClientOne,
    adminAddComment,
} from "../../configs/api";

import { FieldDef } from "../../configs/fields";
import { creditFields } from "../../configs/creditFields";
import { clientFields } from "../../configs/clientFields";

const statusClasses: Record<CreditStatus, string> = {
    new: "bg-blue-50 text-blue-600 border-blue-200",
    approved: "bg-emerald-50 text-emerald-600 border-emerald-200",
    rejected: "bg-rose-50 text-rose-600 border-rose-200",
    treatment: "bg-amber-50 text-amber-600 border-amber-200",
    completed: "bg-purple-50 text-purple-600 border-purple-200",
};

type Props =
    | {
    open: true;
    kind: "credit";
    entity: CreditOut;
    role: Role;
    token: string;
    base?: string;
    onClose: () => void;
    onChanged: () => void;
}
    | {
    open: true;
    kind: "client";
    entity: ClientOut;
    role: Role;
    token: string;
    base?: string;
    onClose: () => void;
    onChanged: () => void;
};

export default function EntityModal(props: Props) {
    // SSR guard
    if (typeof document === "undefined") return null;

    const { open, kind, role, token, base, onClose, onChanged } = props;
    const isAdmin = role === "admin";

    // ───────────────────────────────────────────────
    // Header title
    // ───────────────────────────────────────────────
    const title = kind === "credit" ? `Заявка • ${statusLabel[(props as any).entity.status]}` : "Клиент";

    // ───────────────────────────────────────────────
    // Credit extras: client full name fetched by client_id
    // ───────────────────────────────────────────────
    const [clientName, setClientName] = useState<string>(kind === "credit" ? String((props as any).entity.client_id) : "");
    useEffect(() => {
        if (kind !== "credit") return;
        let done = false;
        fetchClientOne({ token, base, id: (props as any).entity.client_id })
            .then((c: any) => !done && setClientName(c.full_name || String((props as any).entity.client_id)))
            .catch(() => setClientName(String((props as any).entity.client_id)));
        return () => {
            done = true;
        };
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [kind, (props as any).entity?.id]);

    // ───────────────────────────────────────────────
    // Fields config + local draft state
    // ───────────────────────────────────────────────
    const fields: FieldDef<any>[] = useMemo(
        () => (kind === "credit" ? creditFields(clientName) : clientFields),
        [kind, clientName]
    );

    const [draft, setDraft] = useState<Record<string, any>>({});
    const editableKeys = useMemo(() => fields.filter((f) => f.editable).map((f) => f.key), [fields]);

    useEffect(() => {
        // reset draft on entity change
        const next: Record<string, any> = {};
        for (const f of fields) if (f.editable) next[f.key] = (props.entity as any)?.[f.key] ?? "";
        setDraft(next);
        setErr(null);
        setEdit(false);
        setAskSave(false);
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [kind, (props as any).entity?.id, fields]);

    const patch = useMemo(() => {
        // collect changed editable fields only
        const out: Record<string, any> = {};
        for (const k of editableKeys) {
            const prev = (props.entity as any)?.[k];
            const cur = draft[k];
            if (cur !== prev) out[k] = cur === "" ? null : cur;
        }
        return out;
    }, [editableKeys, draft, props.entity]);

    // ───────────────────────────────────────────────
    // Common UI state
    // ───────────────────────────────────────────────
    const [busy, setBusy] = useState(false);
    const [err, setErr] = useState<string | null>(null);
    const [edit, setEdit] = useState(false);
    const [askSave, setAskSave] = useState(false);

    // broker's comment modal (treatment/needs_fix)
    const [askComment, setAskComment] = useState(false);

    // admin's complete modal (set financials before "completed")
    const [askComplete, setAskComplete] = useState(false);

    // ───────────────────────────────────────────────
    // Status actions
    // ───────────────────────────────────────────────
    const canTo = useMemo<CreditStatus[]>(
        // allowed transitions by role and current status
        () => (kind === "credit" ? (allowChangeByRole as any)[role][(props as any).entity.status] ?? [] : []),
        [kind, role, (props as any).entity?.status]
    );

    async function save() {
        try {
            setBusy(true);
            setErr(null);
            if (kind === "credit") {
                await adminUpdateCredit({ token, base, id: (props as any).entity.id, patch });
            } else {
                await adminUpdateClient({ token, base, id: (props as any).entity.id, patch });
            }
            onChanged();
            setEdit(false);
            onClose();
        } catch (e: any) {
            setErr(e?.message || "Ошибка сохранения");
        } finally {
            setBusy(false);
            setAskSave(false);
        }
    }

    async function changeStatus(to: CreditStatus) {
        if (kind !== "credit") return;
        try {
            if (!canTo.includes(to)) throw new Error("Недопустимый переход статуса");
            setErr(null);

            // broker flow: require comment for "На доработку"
            if (to === "treatment") {
                setAskComment(true);
                return;
            }

            // admin flow: require financials before "Выдано"
            if (to === "completed" && isAdmin) {
                setAskComplete(true);
                return;
            }

            setBusy(true);
            await adminChangeStatus({ token, base, id: (props as any).entity.id, status: to });
            onChanged();
            onClose();
        } catch (e: any) {
            setErr(e?.message || "Ошибка смены статуса");
        } finally {
            setBusy(false);
        }
    }

    // broker: send comment then set status "treatment"
    async function submitTreatment(commentText: string) {
        try {
            setBusy(true);
            setErr(null);
            const id = (props as any).entity.id;
            await adminChangeStatus({ token, base, id, status: "treatment" });
            await adminAddComment({ token, base, id, text: commentText });
            onChanged();
            onClose();
        } catch (e: any) {
            setErr(e?.message || "Не удалось перевести на доработку");
        } finally {
            setBusy(false);
            setAskComment(false);
        }
    }

    // admin: set financials first, then "completed"
    async function submitComplete(data: AdminCompletePayload) {
        try {
            setBusy(true);
            setErr(null);
            const id = (props as any).entity.id;

            // 1) update financial fields
            await adminUpdateCredit({
                token,
                base,
                id,
                patch: {
                    approved_amount: data.approved_amount,
                    monthly_payment: data.monthly_payment,
                    bank_name: data.bank_name,
                    first_payment_date: data.first_payment_date,
                    comment: data.comment ?? null,
                },
            });

            // 2) set status completed
            await adminChangeStatus({ token, base, id, status: "completed" });

            onChanged();
            onClose();
        } catch (e: any) {
            setErr(e?.message || "Не удалось перевести в статус «Выдано»");
        } finally {
            setBusy(false);
            setAskComplete(false);
        }
    }

    // ───────────────────────────────────────────────
    // Render helpers
    // ───────────────────────────────────────────────
    function renderField(f: FieldDef<any>) {
        const entity: any = props.entity as any;
        const val = f.editable ? draft[f.key] : entity?.[f.key];

        // read-only view
        if (!f.editable || !isAdmin) {
            const displayed = f.format ? f.format(entity?.[f.key], entity) : val ?? "—";
            return (
                <FieldWrap key={f.key} label={f.label}>
                    <div className="rounded-xl border border-slate-300 bg-slate-50 px-3 py-2 text-sm">{displayed ?? "—"}</div>
                </FieldWrap>
            );
        }
        // edit off
        if (!edit) {
            const displayed = f.format ? f.format(entity?.[f.key], entity) : entity?.[f.key] ?? "—";
            return (
                <FieldWrap key={f.key} label={f.label}>
                    <div className="rounded-xl border border-slate-300 bg-slate-50 px-3 py-2 text-sm">{displayed ?? "—"}</div>
                </FieldWrap>
            );
        }
        // inputs
        return (
            <FieldWrap key={f.key} label={f.label}>
                {f.type === "number" ? (
                    <input
                        type="number"
                        className="w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm"
                        placeholder={f.placeholder}
                        value={val ?? ""}
                        onChange={(e) =>
                            setDraft((d) => ({ ...d, [f.key]: e.currentTarget.value === "" ? null : Number(e.currentTarget.value) }))
                        }
                    />
                ) : f.type === "date" ? (
                    <input
                        type="datetime-local"
                        className="w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm"
                        placeholder={f.placeholder}
                        value={val ?? ""}
                        onChange={(e) => setDraft((d) => ({ ...d, [f.key]: e.currentTarget.value }))}
                    />
                ) : (
                    <input
                        className="w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm"
                        placeholder={f.placeholder}
                        value={val ?? ""}
                        onChange={(e) => setDraft((d) => ({ ...d, [f.key]: e.currentTarget.value }))}
                    />
                )}
            </FieldWrap>
        );
    }

    // ───────────────────────────────────────────────
    // Render
    // ───────────────────────────────────────────────
    return createPortal(
        <>
            <AnimatePresence>
                {open && (
                    <motion.div
                        className="fixed inset-0 z-[70] flex items-center justify-center bg-black/40 backdrop-blur-sm"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        onClick={onClose}
                        role="dialog"
                        aria-modal
                    >
                        <motion.div
                            className="w-[min(920px,96vw)] rounded-3xl border border-slate-200 bg-white p-6 shadow-2xl"
                            initial={{ scale: 0.94, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            exit={{ scale: 0.94, opacity: 0 }}
                            onClick={(e) => e.stopPropagation()}
                        >
                            {/* Header */}
                            <div className="mb-4 flex items-center justify-between">
                                <h3 className="text-xl font-extrabold text-[#2B3674]">{title}</h3>
                                {kind === "credit" && (
                                    // @ts-ignore
                                    <span
                                        className={`rounded-full px-3 py-1 text-sm font-medium border ${statusClasses[(props as any).entity.status]}`}
                                    >
                                        {statusLabel[(props as any).entity.status]}
                                    </span>
                                )}
                            </div>

                            {/* Body */}
                            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                                {kind === "credit" && <Read label="ФИО" value={clientName} />}
                                {fields.map(renderField)}

                                {kind === "credit" && (
                                    <div className="sm:col-span-2">
                                        <div className="mb-1 text-xs font-medium text-[#8F9BBA]">Статус</div>
                                        {(canTo.length ?? 0) === 0 ? (
                                            <div className="text-sm text-slate-500">Нет доступных действий</div>
                                        ) : (
                                            <div className="flex flex-wrap gap-2">
                                                {canTo.map((s) => (
                                                    <button
                                                        key={s}
                                                        className="rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm hover:bg-slate-50 disabled:opacity-60"
                                                        onClick={() => changeStatus(s)}
                                                        disabled={busy}
                                                    >
                                                        {statusLabel[s]}
                                                    </button>
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                )}
                            </div>

                            {err && (
                                <div className="mt-3 rounded-md border border-rose-300 bg-rose-50 px-3 py-2 text-sm text-rose-700" role="alert">
                                    {err}
                                </div>
                            )}

                            {/* Footer */}
                            <div className="mt-5 flex items-center justify-between">
                                <div className="text-xs text-slate-500">
                                    ID: <span className="font-mono">{(props as any).entity.id}</span>
                                </div>
                                <div className="flex gap-2">
                                    {isAdmin && !edit && (
                                        <button
                                            className="rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm hover:bg-slate-50"
                                            onClick={() => setEdit(true)}
                                        >
                                            Редактировать
                                        </button>
                                    )}
                                    {isAdmin && edit && (
                                        <button
                                            className="rounded-xl bg-[#7144ff] text-white px-3 py-2 text-sm hover:brightness-110 disabled:opacity-60"
                                            onClick={() => setAskSave(true)}
                                            disabled={busy || Object.keys(patch).length === 0}
                                        >
                                            Сохранить
                                        </button>
                                    )}
                                    <button className="rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm hover:bg-slate-50" onClick={onClose}>
                                        Закрыть
                                    </button>
                                </div>
                            </div>
                        </motion.div>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Confirm save modal */}
            <ConfirmModal
                open={askSave}
                title="Подтверждение"
                text="Вы уверены, что хотите обновить данные?"
                confirmLabel="Обновить"
                onClose={() => setAskSave(false)}
                onConfirm={save}
                loading={busy}
            />

            {/* Broker: comment modal for 'На доработку' */}
            <BrokerCommentModal open={askComment} onClose={() => setAskComment(false)} onSubmit={submitTreatment} loading={busy} />

            {/* Admin: complete modal for 'Выдано' */}
            <AdminCompleteModal
                open={askComplete}
                onClose={() => setAskComplete(false)}
                loading={busy}
                initial={{
                    approved_amount: (props as any).entity?.approved_amount ?? undefined,
                    monthly_payment: (props as any).entity?.monthly_payment ?? undefined,
                    bank_name: (props as any).entity?.bank_name ?? "",
                    first_payment_date: (props as any).entity?.first_payment_date ?? "",
                    comment: (props as any).entity?.comment ?? "",
                }}
                onSubmit={submitComplete}
            />
        </>,
        document.body
    );
}

function Read({ label, value }: { label: string; value: React.ReactNode }) {
    return (
        <div>
            <div className="mb-1 text-xs font-medium text-[#8F9BBA]">{label}</div>
            <div className="rounded-xl border border-slate-300 bg-slate-50 px-3 py-2 text-sm">{value ?? "—"}</div>
        </div>
    );
}

function FieldWrap({ label, children }: { label: string; children: React.ReactNode }) {
    return (
        <div>
            <div className="mb-1 text-xs font-medium text-[#8F9BBA]">{label}</div>
            {children}
        </div>
    );
}
