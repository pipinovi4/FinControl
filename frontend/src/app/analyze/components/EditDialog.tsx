'use client';

import React, { useMemo, useState, useEffect } from 'react';

const BLOCKED = new Set(['id', 'created_at', 'updated_at', 'role']);

/**
 * Нормалізація значення із текстового інпуту у потрібний тип.
 * Підтримує:
 * - порожній рядок → null (очищення поля)
 * - JSON-об'єкти/масиви
 * - булеві (true/false) якщо оригінал був boolean
 * - числа якщо оригінал був number, або якщо оригінал null/undefined і вигляд числовий
 * - масиви: якщо оригінал масив → CSV "a, b, c" -> string[] (або JSON вже буде розпарсовано вище)
 * - інакше → рядок
 */
function coerceValue(raw: unknown, original: unknown) {
    const s = typeof raw === 'string' ? raw : String(raw ?? '');
    const v = s.trim();

    // 1) порожнє → null
    if (v === '') return null;

    // 2) виглядає як JSON
    const looksLikeJson =
        (v.startsWith('{') && v.endsWith('}')) ||
        (v.startsWith('[') && v.endsWith(']'));
    if (looksLikeJson) {
        try {
            return JSON.parse(v);
        } catch {
            // якщо JSON невалидний — залишимо як рядок (або нижчі гілки оброблять)
        }
    }

    // 3) якщо оригінал булевий — парсимо булеве
    if (typeof original === 'boolean') {
        if (v.toLowerCase() === 'true') return true;
        if (v.toLowerCase() === 'false') return false;
    }

    // 4) якщо оригінал число — парсимо число
    if (typeof original === 'number') {
        const n = Number(v);
        if (Number.isFinite(n)) return n;
    }

    // 5) якщо оригінал масив — інтерпретуємо CSV як масив
    if (Array.isArray(original)) {
        // JSON-масив уже повернули у п.2
        return v.split(',').map((x) => x.trim()).filter(Boolean);
    }

    // 6) якщо тип не відомий (null/undefined), спробуємо число/булеве за виглядом
    if (original == null) {
        if (/^-?\d+(\.\d+)?$/.test(v)) {
            const n = Number(v);
            if (Number.isFinite(n)) return n;
        }
        if (v.toLowerCase() === 'true') return true;
        if (v.toLowerCase() === 'false') return false;
        // масив у цьому випадку приймаємо лише у JSON-форматі (п.2)
    }

    // 7) за замовчуванням — рядок
    return s;
}

type Props = {
    open: boolean;
    title?: string;
    data: Record<string, any> | null;
    onClose: () => void;
    onSave: (patch: Record<string, any>) => Promise<void> | void;
};

export default function EditDialog({
                                       open,
                                       title = 'Редактирование записи',
                                       data,
                                       onClose,
                                       onSave,
                                   }: Props) {
    const editableKeys = useMemo(() => {
        if (!data) return [];
        return Object.keys(data).filter((k) => !BLOCKED.has(k));
    }, [data]);

    // зберігаємо усе як РЯДКИ для textarea
    const [state, setState] = useState<Record<string, string>>({});
    const [saving, setSaving] = useState(false);
    const [err, setErr] = useState<string | null>(null);

    useEffect(() => {
        if (!open || !data) return;
        const next: Record<string, string> = {};
        editableKeys.forEach((k) => {
            const v = (data as any)[k];
            if (Array.isArray(v)) next[k] = v.join(', ');
            else if (v && typeof v === 'object') next[k] = JSON.stringify(v, null, 2);
            else next[k] = v == null ? '' : String(v);
        });
        setState(next);
        setErr(null);
    }, [open, data, editableKeys]);

    if (!open) return null;

    const handleSave = async () => {
        setSaving(true);
        setErr(null);
        try {
            const patch: Record<string, any> = {};
            editableKeys.forEach((k) => {
                const raw = state[k]; // string | undefined
                const original = (data as any)[k];

                const val = coerceValue(raw, original);

                // глибоке порівняння щоб не надсилати незмінені поля
                if (JSON.stringify(val) !== JSON.stringify(original)) {
                    patch[k] = val;
                }
            });

            if (Object.keys(patch).length > 0) {
                await onSave(patch);
            }
            onClose();
        } catch (e: any) {
            setErr(e?.message || 'Ошибка');
        } finally {
            setSaving(false);
        }
    };

    return (
        <div
            className="fixed inset-0 z-[95] flex items-center justify-center bg-black/40 backdrop-blur-sm"
            onClick={onClose}
            role="dialog"
            aria-modal
        >
            <div
                className="w-[min(720px,94vw)] max-h-[88vh] overflow-auto rounded-2xl border border-slate-200 bg-white p-5 shadow-2xl"
                onClick={(e) => e.stopPropagation()}
            >
                <div className="mb-3 flex items-center justify-between gap-3">
                    <h3 className="text-lg font-bold text-[#2B3674]">{title}</h3>
                    <button
                        onClick={onClose}
                        className="rounded-full p-1 text-slate-500 hover:bg-slate-100"
                    >
                        ✕
                    </button>
                </div>

                {!data ? (
                    <div className="text-sm text-slate-500">Нет данных</div>
                ) : (
                    <div className="grid gap-3 sm:grid-cols-2">
                        {editableKeys.map((k) => (
                            <label key={k} className="flex flex-col gap-1">
                <span className="text-[11px] uppercase tracking-wide text-slate-500 font-semibold">
                  {k.replace(/_/g, ' ')}
                </span>
                                <textarea
                                    rows={Math.min(
                                        8,
                                        Math.max(2, String(state[k] ?? '').split('\n').length)
                                    )}
                                    className="rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-800 focus:border-primary focus:ring-2 focus:ring-primary/40"
                                    value={state[k] ?? ''}
                                    onChange={(e) =>
                                        setState((s) => ({ ...s, [k]: e.target.value }))
                                    }
                                    placeholder={
                                        Array.isArray((data as any)[k])
                                            ? 'CSV: a, b, c — або JSON-масив'
                                            : typeof (data as any)[k] === 'object' && (data as any)[k] !== null
                                                ? 'JSON-объект'
                                                : 'Введіть значення'
                                    }
                                />
                            </label>
                        ))}
                    </div>
                )}

                {err && <p className="mt-3 text-sm text-rose-600">{err}</p>}

                <div className="mt-4 flex justify-end gap-2">
                    <button
                        onClick={onClose}
                        className="rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm hover:bg-slate-50"
                    >
                        Отмена
                    </button>
                    <button
                        onClick={handleSave}
                        disabled={saving}
                        className="rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-white disabled:opacity-60"
                    >
                        {saving ? 'Сохраняем…' : 'Сохранить'}
                    </button>
                </div>
            </div>
        </div>
    );
}
