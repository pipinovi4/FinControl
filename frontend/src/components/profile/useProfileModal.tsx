// src/components/profile/useProfileModal.ts
'use client';

import { createContext, useContext, useState, ReactNode } from 'react';

type ProfileCtx = { open: () => void; close: () => void; isOpen: boolean };

const Ctx = createContext<ProfileCtx | null>(null);
export const useProfileModal = () => useContext(Ctx)!;

export function ProfileProvider({ children }: { children: ReactNode }) {
    const [isOpen, set] = useState(false);
    const value = { isOpen, open: () => set(true), close: () => set(false) };
    return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}
