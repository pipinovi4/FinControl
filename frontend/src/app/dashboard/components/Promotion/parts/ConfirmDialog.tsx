"use client";

import React, { useEffect, useState } from "react";
import { createPortal } from "react-dom";

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

    // локальний стейт, щоб лишати DOM під час анімації
    const [show, setShow] = useState(open);

    useEffect(() => {
        if (open) setShow(true);
        else {
            const t = setTimeout(() => setShow(false), 300); // час анімації
            return () => clearTimeout(t);
        }
    }, [open]);

    if (!show) return null;

    return createPortal(
        <div
            className={`
        fixed inset-0 z-[70] flex items-center justify-center
        bg-black/40 backdrop-blur-sm
        transition-opacity duration-300 ease-out
        ${open ? "opacity-100 visible" : "opacity-0 invisible"}
      `}
            onClick={onClose}
        >
            <div
                className={`
          w-[min(520px,92vw)] rounded-2xl bg-white p-5 shadow-2xl
          transform transition-all duration-300 ease-out
          ${open ? "scale-100 opacity-100" : "scale-95 opacity-0"}
        `}
                onClick={(e) => e.stopPropagation()}
            >
                <h3 className="mb-2 flex items-center gap-2 text-lg font-extrabold text-[#2B3674]">
                    {icon} {title}
                </h3>
                <div className="text-sm text-slate-600">{text}</div>
                <div className="mt-4 flex justify-end gap-2">
                    <button
                        className="rounded-xl border border-slate-300 px-4 py-2 text-sm hover:bg-slate-50 cursor-pointer"
                        onClick={onClose}
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
            </div>
        </div>,
        document.body
    );
}
