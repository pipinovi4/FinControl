"use client";

import React, { useEffect, useState } from "react";
import { createPortal } from "react-dom";
import { AnimatePresence, motion } from "framer-motion";

export default function ConfirmModal({
                                         open,
                                         title = "Подтвердите действие",
                                         text,
                                         confirmLabel = "Подтвердить",
                                         cancelLabel = "Отмена",
                                         onConfirm,
                                         onClose,
                                         loading,
                                         icon,
                                         accent,
                                     }: {
    open: boolean;
    title?: string;
    text: string;
    confirmLabel?: string;
    cancelLabel?: string;
    onConfirm: () => void;
    onClose: () => void;
    loading?: boolean;
    icon?: React.ReactNode;
    accent?: "danger" | "primary";
}) {
    if (typeof document === "undefined") return null;

    // локальний стан видимості для плавного exit
    const [visible, setVisible] = useState(open);

    // коли батько відкриває — показуємо; коли закриває ззовні — стартуємо exit
    useEffect(() => {
        if (open) setVisible(true);
        else setVisible(false);
    }, [open]);

    const requestClose = () => setVisible(false);

    return createPortal(
        // Викликаємо onClose ПІСЛЯ завершення exit-анімації
        <AnimatePresence onExitComplete={onClose}>
            {visible && (
                <motion.div
                    key="overlay"
                    className="fixed inset-0 z-[70] bg-black/40 backdrop-blur-sm flex items-center justify-center"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 0.25 }}
                    onClick={requestClose}
                >
                    <motion.div
                        key="dialog"
                        className="w-[min(520px,92vw)] rounded-2xl bg-white p-5 shadow-2xl"
                        initial={{ scale: 0.92, opacity: 0, y: 6 }}
                        animate={{ scale: 1, opacity: 1, y: 0 }}
                        exit={{ scale: 0.92, opacity: 0, y: 6 }}
                        transition={{ duration: 0.25 }}
                        onClick={(e) => e.stopPropagation()}
                    >
                        <h3 className="mb-2 flex items-center gap-2 text-lg font-extrabold text-[#2B3674]">
                            {icon} {title}
                        </h3>
                        <div className="text-sm text-slate-600">{text}</div>
                        <div className="mt-4 flex justify-end gap-2">
                            <button
                                className="rounded-xl border border-slate-300 px-4 py-2 text-sm hover:bg-slate-50 cursor-pointer"
                                onClick={requestClose}
                                disabled={!!loading}
                            >
                                {cancelLabel}
                            </button>
                            <button
                                className={`rounded-xl px-4 py-2 text-sm text-white hover:brightness-110 disabled:opacity-60 cursor-pointer ${
                                    accent === "danger" ? "bg-rose-600" : "bg-[#7144ff]"
                                }`}
                                onClick={onConfirm}
                                disabled={!!loading}
                            >
                                {confirmLabel}
                            </button>
                        </div>
                    </motion.div>
                </motion.div>
            )}
        </AnimatePresence>,
        document.body
    );
}
