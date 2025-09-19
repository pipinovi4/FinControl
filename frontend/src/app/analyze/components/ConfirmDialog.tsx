'use client';

import React from 'react';

type Props = {
    open: boolean;
    title?: string;
    subtitle?: string;
    confirmText?: string;
    cancelText?: string;
    loading?: boolean;
    onConfirm: () => void;
    onClose: () => void;
};

export default function ConfirmDialog({
                                          open,
                                          title = 'Вы уверены?',
                                          subtitle,
                                          confirmText = 'Подтвердить',
                                          cancelText = 'Отмена',
                                          loading = false,
                                          onConfirm,
                                          onClose,
                                      }: Props) {
    if (!open) return null;

    return (
        <div
            className="fixed inset-0 z-[90] flex items-center justify-center bg-black/40 backdrop-blur-sm"
            onClick={onClose}
            role="dialog"
            aria-modal
        >
            <div
                className="w-[min(520px,92vw)] rounded-2xl border border-slate-200 bg-white p-5 shadow-2xl"
                onClick={(e) => e.stopPropagation()}
            >
                <div className="flex items-start justify-between gap-3">
                    <h3 className="text-base font-bold text-[#2B3674]">{title}</h3>
                    <button
                        onClick={onClose}
                        className="rounded-full p-1 text-slate-500 hover:bg-slate-100"
                        aria-label="Закрыть"
                    >
                        ✕
                    </button>
                </div>

                {subtitle && <p className="mt-2 mb-4 text-sm text-slate-600">{subtitle}</p>}

                <div className="flex justify-end gap-2">
                    <button
                        onClick={onClose}
                        disabled={loading}
                        className="rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm hover:bg-slate-50 disabled:opacity-50"
                    >
                        {cancelText}
                    </button>
                    <button
                        onClick={onConfirm}
                        disabled={loading}
                        className="rounded-lg bg-rose-600 px-4 py-2 text-sm font-semibold text-white hover:brightness-110 disabled:opacity-50"
                    >
                        {loading ? '…' : confirmText}
                    </button>
                </div>
            </div>
        </div>
    );
}
