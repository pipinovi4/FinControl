"use client";

import React from "react";
import AuthCard from "@/app/auth/components/AuthCard";
import AuthForm from "@/app/auth/components/AuthForm"; // шляхи підкоригуй під себе
import { useRoutesInfo } from "@/hooks/useRoutesInfo";

export default function LoginPage() {
    const { data: fields, isLoading, isError } = useRoutesInfo();

    const handleLogin = (formData: Record<string, string>) => {
        console.log("🧾 Login form data:", formData);
    };
    console.log(fields, isLoading, isError)
    return (
        <div className="min-h-screen flex items-center justify-center px-4">
            <AuthCard>
                {isLoading && <p>Завантаження...</p>}
                {isError && <p className="text-red-500">Помилка при завантаженні полів</p>}
                {fields && (
                    <AuthForm
                        fields={fields}
                        onSubmitAction={handleLogin}
                        buttonText="Уaвійти"
                    />
                )}
            </AuthCard>
        </div>
    );
}
