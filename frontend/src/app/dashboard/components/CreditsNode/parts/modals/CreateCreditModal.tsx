"use client";

import React, { useEffect, useState } from "react";
import { createPortal } from "react-dom";
import { AnimatePresence, motion } from "framer-motion";
import { ClientOut } from "@/app/dashboard/components/CreditsNode/configs/types";
import { adminCreateCredit } from "@/app/dashboard/components/CreditsNode/configs/api";

export default function CreateCreditModal({
                                              open,
                                              client,
                                              token,
                                              base,
                                              onClose,
                                              onCreated,
                                          }: {
    open: boolean;
    client: ClientOut | null;
    token: string;
    base?: string;
    onClose: () => void;
    onCreated: () => void;
}) {
    const [amount, setAmount] = useState<string>("");
    const [error, setError] = useState<string | null>(null);
    const [busy, setBusy] = useState(false);

    useEffect(() => {
        if (!open) {
            setAmount(""); setError(null); setBusy(false);
        }
    }, [open]);

    const submit = async () => {
        if (!client) return;
        const n = Number(amount);
        if (!Number.isFinite(n) || n <= 0) {
            setError("Введите корректную сумму.");
            return;
        }
        try {
            setBusy(true); setError(null);
            await adminCreateCredit({ token, base, client_id: client.id, amount: n });
            onCreated();
            onClose();
        } catch (e: any) {
            setError(e?.message || "Ошибка");
        } finally {
            setBusy(false);
        }
    };

    if (typeof document === "undefined") return null;
    return createPortal(
        <AnimatePresence>
            {open && (
                <motion.div
                    className="fixed inset-0 z-[65] flex items-center justify-center bg-black/40 backdrop-blur-sm"
                    initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                    onClick={onClose} role="dialog" aria-modal
                >
                    <motion.div
                        className="w-[min(560px,92vw)] rounded-3xl border border-slate-200 bg-white p-5 shadow-2xl"
                        initial={{ scale: 0.94, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} exit={{ scale: 0.94, opacity: 0 }}
                        onClick={(e) => e.stopPropagation()}
                    >
                        <div className="mb-4 flex items-center justify-between">
                            <h3 className="text-xl font-extrabold text-[#2B3674]">Создать кредит</h3>
                            <div className="text-xs text-slate-500">Клиент: <span className="font-mono">{client?.id}</span></div>
                        </div>

                        <div className="space-y-3">
                            <div>
                                <div className="mb-1 text-xs font-medium text-[#8F9BBA]">Сумма заявки</div>
                                <input
                                    type="number"
                                    className="w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm focus:border-[#7144ff] focus:outline-none"
                                    placeholder="150000"
                                    inputMode="numeric"
                                    value={amount}
                                    onChange={(e) => setAmount(e.currentTarget.value)}
                                    onKeyDown={(e) => e.key === "Enter" && submit()}
                                />
                            </div>
                            {error && (
                                <div className="rounded-md border border-rose-300 bg-rose-50 px-3 py-2 text-sm text-rose-700" role="alert">
                                    {error}
                                </div>
                            )}
                        </div>

                        <div className="mt-4 flex justify-end gap-2">
                            <button className="rounded-xl border border-slate-300 bg-white px-4 py-2 text-sm hover:bg-slate-50 disabled:opacity-50" onClick={onClose} disabled={busy}>
                                Отмена
                            </button>
                            <button className="rounded-xl bg-[#7144ff] px-4 py-2 text-sm font-semibold text-white hover:brightness-110 disabled:opacity-50" onClick={submit} disabled={busy || amount.trim() === ""}>
                                Создать
                            </button>
                        </div>
                    </motion.div>
                </motion.div>
            )}
        </AnimatePresence>,
        document.body
    );
}
