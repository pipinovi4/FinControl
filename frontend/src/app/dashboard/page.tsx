/* eslint-disable react/no-unescaped-entities */
"use client";

import React, { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";

import UserStorage from "@/services/UserStorage";
import type StoredUserType from "@/types/StoredUser";
import dashboardConfig, {
    type StaticMetric,
    type DashboardConfig,
} from "@/app/dashboard/config/dashboardConfig";
import LoadingScreen from "@/components/ui/LoadingScreen";

/* ---------------------------------------------------------- */
/**
 * Головна сторінка Dashboard. Дрендерить секції:
 *  • statCards   – маленькі метрики (4-колонки на XL)
 *  • graphicCats – графіки (2-колонки на XL)
 *  • tableCats   – таблиці з кастомним розкладом 1-2-1
 *  • actionCards – новий блок під таблицями (3-колонки на XL)
 *  • creditsNode – окремий prepared-вузол (2/4 ширини в actionCards)
 */
/* ---------------------------------------------------------- */
const DashboardPage: React.FC = () => {
    const router = useRouter();

    /* ---------- auth / role ---------- */
    const [user, setUser] = useState<StoredUserType | null>(null);
    const [role, setRole] = useState<keyof DashboardConfig | null>(null);

    useEffect(() => {
        const stored = UserStorage.get();
        if (!stored) {
            router.push("/auth/login");
            return;
        }

        setUser(stored);
        setRole((stored.role?.toLowerCase() as keyof DashboardConfig) ?? null);
    }, [router]);

    /* ---------- configs ---------- */
    const cfg = useMemo(() => (role ? dashboardConfig[role] : null), [role]);

    if (!cfg) return <LoadingScreen />;

    /* ---------- helpers ---------- */
    const renderGroup = (obj?: Record<string, StaticMetric>) =>
        obj
            ? (Object.entries(obj) as [string, StaticMetric][]).map(([k, m]) => (
                <React.Fragment key={k}>{m.render()}</React.Fragment>
            ))
            : [];

    /* ---------- prepared nodes ---------- */
    const statCards = renderGroup(cfg.static);
    const graphicCats = renderGroup(cfg.graphic);
    const tableCats = renderGroup(cfg.tables);
    const actionCards = renderGroup(cfg.actionCards);
    const creditsNode = renderGroup(cfg.creditsNode);

    // // NEW: optional prepared node "creditsNode" (configured per role in dashboardConfig)
    // type RoleWithCreditsNode = typeof cfg & { creditsNode?: StaticMetric };
    // const creditsNode = (cfg as RoleWithCreditsNode)?.creditsNode?.render
    //     ? (cfg as RoleWithCreditsNode).creditsNode!.render()
    //     : null;

    /* ---------- layout ---------- */
    return (
        <div className="md:ml-60 min-h-screen font-[var(--font-dm-sans)]">
            {/* header */}
            <header className="px-6 py-4 text-primary">
                <div className="text-sm opacity-80">Pages / Dashboard</div>
                <h1 className="mt-1 text-2xl font-bold opacity-95">Панель&nbsp;управления</h1>
            </header>

            {/* content */}
            <main className="flex flex-col gap-6 p-2 sm:p-4 lg:p-6">
                {!!statCards.length && (
                    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
                        {statCards}
                    </div>
                )}

                {!!graphicCats.length && (
                    <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">
                        {graphicCats}
                    </div>
                )}

                {!!tableCats.length && (
                    <div className="grid grid-cols-1 gap-6 xl:grid-cols-4">
                        <div className="col-span-1 flex flex-col gap-6 xl:col-span-3">
                            {tableCats.slice(0, 1)}
                        </div>
                        <div className="col-span-1 flex flex-col gap-6 xl:col-span-1">
                            {tableCats.slice(1, 2)}
                        </div>
                        {/*<div className="col-span-1 flex flex-col gap-6 xl:col-span-1">*/}
                        {/*    {tableCats.slice(2)}*/}
                        {/*</div>*/}
                    </div>
                )}

                {!!actionCards.length && (
                    <div className="grid grid-cols-1 gap-6 xl:grid-cols-4">
                        <div className="col-span-1 flex flex-col gap-6 xl:col-span-1">
                            {actionCards.slice(0, 1)}
                        </div>
                        <div className="col-span-1 flex flex-col gap-6 xl:col-span-1">
                            {actionCards.slice(1, 2)}
                        </div>
                        <div className="col-span-2 flex flex-col gap-6 xl:col-span-2">
                            {/* NEW: credits node first, then the rest of action cards */}
                            {actionCards.slice(2)}
                        </div>
                    </div>
                )}

                {!!creditsNode.length && (
                    <div className="grid grid-cols-1 gap-6 xl:grid-cols-4">
                        <div className="col-span-2 flex flex-col gap-6 xl:col-span-3">
                            {creditsNode.slice(0, 1)}
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
};

export default DashboardPage;
