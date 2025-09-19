"use client";

import React, { useEffect, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";

type Props = {
    open: boolean;
    onClose: () => void;
    onSubmit: (text: string) => void; // returns comment text
    loading?: boolean;
    title?: string;
    placeholder?: string;
    initialText?: string;
};

export default function BrokerCommentModal({
                                               open,
                                               onClose,
                                               onSubmit,
                                               loading,
                                               title = "Причина доработки",
                                               placeholder = "Опишите, что нужно исправить…",
                                               initialText = "",
                                           }: Props) {
    // local state for comment text
    const [text, setText] = useState(initialText);

    // reset state when modal closes
    useEffect(() => {
        if (!open) setText(initialText ?? "");
    }, [open, initialText]);

    const disabled = (loading ?? false) || text.trim().length === 0;

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
                        className="w-[min(560px,92vw)] rounded-2xl border border-slate-200 bg-white p-5 shadow-2xl"
                        initial={{ scale: 0.94, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        exit={{ scale: 0.94, opacity: 0 }}
                        onClick={(e) => e.stopPropagation()}
                    >
                        <div className="mb-3 text-lg font-extrabold text-[#2B3674]">{title}</div>
                        <div className="mb-1 text-xs font-medium text-[#8F9BBA]">
                            Укажите, что именно нужно исправить. Комментарий обязателен.
                        </div>
                        <textarea
                            className="w-full min-h-28 rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm outline-none focus:border-[#7144ff]"
                            placeholder={placeholder}
                            value={text}
                            onChange={(e) => setText(e.currentTarget.value)}
                        />
                        <div className="mt-4 flex justify-end gap-2">
                            <button
                                className="rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm hover:bg-slate-50"
                                onClick={onClose}
                            >
                                Отмена
                            </button>
                            <button
                                className="rounded-xl bg-[#7144ff] text-white px-3 py-2 text-sm hover:brightness-110 disabled:opacity-60"
                                disabled={disabled}
                                onClick={() => onSubmit(text.trim())}
                            >
                                Отправить
                            </button>
                        </div>
                    </motion.div>
                </motion.div>
            )}
        </AnimatePresence>
    );
}
