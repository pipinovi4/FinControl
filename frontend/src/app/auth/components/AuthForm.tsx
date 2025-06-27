"use client";

import React from "react";

interface FieldConfig {
    name: string;
    label: string;
    type?: "text" | "password" | "email";
    required?: boolean;
    placeholder?: string;
}

interface AuthFormProps {
    fields: FieldConfig[]; // Це приходить з бекенду (meta)
    onSubmitAction: (data: Record<string, string>) => void;
    buttonText?: string;
}

export default function AuthForm({ fields, onSubmitAction, buttonText = "Увійти" }: AuthFormProps) {
    const [formState, setFormState] = React.useState<Record<string, string>>({});

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormState((prev) => ({
            ...prev,
            [e.target.name]: e.target.value,
        }));
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSubmitAction(formState);
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            {fields.map((field) => (
                <div key={field.name} className="flex flex-col gap-1">
                    <label htmlFor={field.name} className="text-sm font-medium text-foreground">
                        {field.label}
                    </label>
                    <input
                        type={field.type ?? "text"}
                        name={field.name}
                        id={field.name}
                        required={field.required}
                        placeholder={field.placeholder ?? ""}
                        onChange={handleChange}
                        className="border border-border rounded-md px-3 py-2 text-sm focus:outline-none focus:ring focus:ring-primary/40 transition"
                    />
                </div>
            ))}

            <button
                type="submit"
                className="w-full bg-primary text-white py-2 rounded-md font-semibold hover:opacity-90 transition"
            >
                {buttonText}
            </button>
        </form>
    );
}
