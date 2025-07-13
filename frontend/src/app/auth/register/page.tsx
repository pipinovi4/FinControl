'use client';

import React, { useState } from 'react';
import clsx from 'clsx';
import Link from 'next/link';
import { authService } from '@/services/AuthService';
import {UUID} from "node:crypto";
import {MetaFetchError} from "@/lib/metaFetch";
import { useRouter } from 'next/navigation';
import UserStorage from "@/services/UserStorage"; // ⬅️ додай цей імпорт

const RegisterPage = () => {
    const [role, setRole] = useState<'broker' | 'worker'>('broker');
    const [formData, setFormData] = useState<Record<string, string | string[] | UUID>>({});
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const router = useRouter();

    // Додай цей імпорт або просто функцію в код
    const validateFormData = (
        data: Record<string, string | string[] | UUID>,
        role: 'broker' | 'worker'
    ): string | null => {
        const email = data.email?.toString() || '';
        const password = data.password?.toString() || '';
        const username = data.username?.toString() || '';
        const company_name = data.company_name?.toString() || '';
        const region = data.region?.toString() || '';

        if (!email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) return 'Введіть коректну пошту.';
        if (password.length < 6) return 'Пароль має містити щонайменше 6 символів.';

        if (role === 'worker') {
            if (username.length < 3) return 'Ім’я користувача повинне містити щонайменше 3 символи.';
        }

        if (role === 'broker') {
            if (company_name.length < 2) return 'Назва компанії є обов’язковою.';
            if (region.length < 2) return 'Регіон є обов’язковим.';
        }

        return null;
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { id, value } = e.target;
        setFormData((prev) => ({ ...prev, [id]: value }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            const enrichedData = {
                ...formData,
                email: formData.email || `user${Math.floor(Math.random() * 10000)}@example.com`,
                password: formData.password || "qwerty123",
                telegram_id: crypto.randomUUID(),
                telegram_username: `user_${Math.random().toString(36).substring(2, 10)}`,
                region: role === "broker"
                    ? (typeof formData.region === "string" && formData.region.trim()
                        ? [formData.region]
                        : ["Київська область"])
                    : undefined,
                company_name: role === "broker"
                    ? (formData.company_name || "My Test Company")
                    : undefined,
                username: role === "worker"
                    ? (formData.username || `worker_${Math.floor(Math.random() * 1000)}`)
                    : undefined,
            };

            const validationError = validateFormData(formData, role);
            if (validationError) {
                setError(validationError);
                setLoading(false);
                return;
            }

            const res = await authService.register(role, enrichedData as any);
            console.log('✅ Registered:', res);
            router.push('/dashboard');
        } catch (err) {
            setLoading(false);

            if (err instanceof MetaFetchError) {
                setError(err.userMessage);
                console.error('[MetaFetchError]', err.devMessage, err.stack);
            } else {
                console.error('[Unexpected]', err);
                setError('Невідома помилка.');
            }
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-[#F8FAFF] px-4 py-12 font-[var(--font-dm-sans)]">
            <div className="w-full max-w-md bg-white shadow-lg rounded-2xl px-6 sm:px-8 py-8 sm:py-10 flex flex-col gap-6">
                <h1 className="text-2xl font-bold text-[#2B3674] text-center">Создать аккаунт</h1>

                <form className="flex flex-col gap-4" onSubmit={handleSubmit}>
                    <div className="flex flex-col gap-1">
                        <label htmlFor="email" className="text-sm text-[#8F9BBA]">Почта</label>
                        <input
                            type="email"
                            id="email"
                            placeholder="you@example.com"
                            onChange={handleChange}
                            className="rounded-xl border border-gray-200 px-4 py-2 text-sm"
                        />
                    </div>

                    <div className="flex flex-col gap-1">
                        <label htmlFor="password" className="text-sm text-[#8F9BBA]">Пароль</label>
                        <input
                            type="password"
                            id="password"
                            placeholder="********"
                            onChange={handleChange}
                            className="rounded-xl border border-gray-200 px-4 py-2 text-sm"
                        />
                    </div>

                    {role === 'worker' && (
                        <div className="flex flex-col gap-1">
                            <label htmlFor="username" className="text-sm text-[#8F9BBA]">Логин</label>
                            <input
                                type="text"
                                id="username"
                                placeholder="john_doe"
                                onChange={handleChange}
                                className="rounded-xl border border-gray-200 px-4 py-2 text-sm"
                            />
                        </div>
                    )}

                    {role === 'broker' && (
                        <>
                            <div className="flex flex-col gap-1">
                                <label htmlFor="company_name" className="text-sm text-[#8F9BBA]">Название компании</label>
                                <input
                                    type="text"
                                    id="company_name"
                                    placeholder="My Company LLC"
                                    onChange={handleChange}
                                    className="rounded-xl border border-gray-200 px-4 py-2 text-sm"
                                />
                            </div>
                            <div className="flex flex-col gap-1">
                                <label htmlFor="region" className="text-sm text-[#8F9BBA]">Регион</label>
                                <input
                                    type="text"
                                    id="region"
                                    placeholder="Киевская область"
                                    onChange={handleChange}
                                    className="rounded-xl border border-gray-200 px-4 py-2 text-sm"
                                />
                            </div>
                        </>
                    )}

                    <div className="mt-2">
                        <p className="text-sm mb-1 text-[#8F9BBA]">Роль</p>
                        <div className="flex gap-2">
                            {(['broker', 'worker'] as const).map(opt => (
                                <button
                                    key={opt}
                                    type="button"
                                    onClick={() => setRole(opt)}
                                    className={clsx(
                                        'flex-1 text-sm font-medium rounded-xl py-2 transition',
                                        role === opt
                                            ? 'bg-[#2B3674] text-white'
                                            : 'bg-[#F1F4FA] text-[#2B3674] hover:bg-[#E6E9F2]'
                                    )}
                                >
                                    {opt === 'broker' ? 'Брокер' : 'Работник'}
                                </button>
                            ))}
                        </div>
                    </div>

                    {error && (
                        <div className="mt-2 rounded-xl bg-red-100 border border-red-300 text-red-700 px-4 py-2 text-sm text-center">
                            ⚠️ {error}
                        </div>
                    )}

                    <button
                        type="submit"
                        disabled={loading}
                        className="mt-4 py-2 rounded-xl bg-[#2B3674] text-white font-semibold hover:bg-[#1e295c] transition"
                    >
                        {loading ? 'Загрузка...' : 'Зарегистрироваться'}
                    </button>

                    <p className="text-center text-sm text-[#8F9BBA] mt-2">
                        Уже есть аккаунт? <Link href="/auth/login" className="text-[#2B3674] hover:underline font-medium">Войти</Link>
                    </p>

                </form>
            </div>
        </div>
    );
};

export default RegisterPage;
