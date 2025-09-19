'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { authService } from '@/services/AuthService';
import { MetaFetchError } from '@/lib/metaFetch';

const LoginPage = () => {
    const router = useRouter();
    const [formData, setFormData] = useState({ email: '', password: '' });

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { id, value } = e.target;
        setFormData(prev => ({ ...prev, [id]: value }));
    };

    const validate = (email: string, pass: string): string | null => {
        if (!email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) return 'Введіть коректну пошту.';
        if (pass.length < 6) return 'Пароль щонайменше 6 символів.';
        return null;
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);

        const v = validate(formData.email, formData.password);
        if (v) {
            setError(v);
            return;
        }

        setLoading(true);
        try {
            const res = await authService.login(formData);
            console.log('✅ Logged in:', res);
            router.push('/dashboard');
        } catch (err) {
            if (err instanceof MetaFetchError) {
                setError(err.userMessage);
                console.error(err.devMessage);
            } else {
                console.error('Unexpected error', err);
                setError('Щось пішло не так. Спробуйте пізніше.');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-[#F8FAFF] px-4 py-12 font-[var(--font-dm-sans)]">
            <div className="w-full max-w-md 2xl:max-w-xl bg-white shadow-lg rounded-2xl px-6 sm:px-8 py-8 sm:py-10 flex flex-col gap-6">
                <h1 className="text-2xl font-bold text-[#2B3674] text-center">Войти в аккаунт</h1>

                <form className="flex flex-col gap-4" onSubmit={handleSubmit}>
                    <div className="flex flex-col gap-1">
                        <label htmlFor="email" className="text-sm text-[#8F9BBA]">Почта</label>
                        <input
                            type="email"
                            id="email"
                            placeholder="you@example.com"
                            onChange={handleChange}
                            className="rounded-xl border border-gray-200 px-4 py-2 text-sm text-[#2B3674] bg-white placeholder-[#C0C5D6] focus:outline-none focus:ring-2 focus:ring-[#2B3674]"
                        />
                    </div>

                    <div className="flex flex-col gap-1">
                        <label htmlFor="password" className="text-sm text-[#8F9BBA]">Пароль</label>
                        <input
                            type="password"
                            id="password"
                            placeholder="********"
                            onChange={handleChange}
                            className="rounded-xl border border-gray-200 px-4 py-2 text-sm text-[#2B3674] bg-white placeholder-[#C0C5D6] focus:outline-none focus:ring-2 focus:ring-[#2B3674]"
                        />
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
                        {loading ? 'Загрузка…' : 'Войти'}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default LoginPage;
