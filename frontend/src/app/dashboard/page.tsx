'use client';

import React, { useEffect, useMemo, useState } from 'react';
import { useRouter } from 'next/navigation';

import UserStorage from '@/services/UserStorage';
import type StoredUserType from '@/types/StoredUser';
import dashboardConfig, {
    type StaticMetric,
    type DashboardConfig,
    type EnhancedStaticMetric
} from '@/app/dashboard/config/dashboardConfig';
import LoadingScreen from '@/components/ui/LoadingScreen';

/* ─────────────────────────────────────────────────────────── */

const DashboardPage = () => {
    const router = useRouter();

    /* ——— локальний стейт ——— */
    const [user, setUser] = useState<StoredUserType | null>(null);
    const [role, setRole] = useState<keyof DashboardConfig | null>(null);
    const [metrics, setMetrics] = useState<Record<string, string>>({});

    /* ——— читаємо user з localStorage ——— */
    useEffect(() => {
        const stored = UserStorage.get();
        if (!stored) {
            router.push('/auth/login');
            return;
        }

        setUser(stored);

        const normalizedRole = stored.role?.toLowerCase() as keyof DashboardConfig | undefined;
        setRole(normalizedRole ?? null);
    }, [router]);


    /* ——— конфіг відповідно до ролі ——— */
    const cfg = useMemo(() => (role ? dashboardConfig[role] : null), [role]);

    /* ——— фетчимо тільки static-метрики ——— */
    useEffect(() => {
        if (!cfg?.static) return;

        const loadMetrics = async () => {
            const entries = Object.entries(cfg.static) as [string, EnhancedStaticMetric][];

            const results = await Promise.all(
                entries.map(async ([key, metric]) => {
                    try {
                        if (!metric.fetchUrl) return [key, 'XUY'];
                        let url = metric.fetchUrl
                        if (metric.requiresId) {
                            const stored = UserStorage.get();
                            const userId = stored?.id;
                            if (!userId) return [key, '-'];

                            url = metric.fetchUrl.endsWith('/')
                                ? `${metric.fetchUrl}${userId}`
                                : `${metric.fetchUrl}/${userId}`;
                        }

                        const res = await fetch(url);
                        const data = await res.json();

                        return [key, data?.value ?? '-'];
                    } catch (err) {
                        console.error(`[${key}] fetch failed`, err);
                        return [key, '-'];
                    }
                })
            );

            // Convert array of tuples back to object
            const mapped = Object.fromEntries(results);
            setMetrics(mapped);
        };

        loadMetrics();
    }, [cfg]);

    /* ——— поки немає cfg показуємо лоадер ——— */
    if (!cfg) return <LoadingScreen />;

    /* ——— масиви React-нодів ——— */
    const statCards = cfg.static
        ? (Object.entries(cfg.static) as [string, StaticMetric][]).map(([k, metric]) => (
            <React.Fragment key={k}>
                {metric.render(metrics[k] ?? '-')}
            </React.Fragment>
        ))
        : [];

    const graphicCats = cfg.graphic
        ? (Object.entries(cfg.graphic) as [string, StaticMetric][]).map(([k, metric]) => (
            <React.Fragment key={k}>{metric.render(null)}</React.Fragment>
        ))
        : [];

    const tableCats = cfg.tables
        ? (Object.entries(cfg.tables) as [string, StaticMetric][]).map(([k, metric]) => (
            <React.Fragment key={k}>{metric.render(null)}</React.Fragment>
        ))
        : [];

    /* ——— розмітка (стилі не чіпав) ——— */
    return (
        <div className="md:ml-60 min-h-screen font-[var(--font-dm-sans)]">
            <header className="px-6 py-4 text-primary">
                <div className="text-sm opacity-80">Pages / Dashboard</div>
                <h1 className="text-2xl font-bold mt-1 opacity-95">Панель&nbsp;управления</h1>
            </header>

            <main className="p-2 sm:p-4 lg:p-6 flex flex-col gap-6">
                {!!statCards.length && (
                    <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
                        {statCards}
                    </div>
                )}

                {!!graphicCats.length && (
                    <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
                        {graphicCats}
                    </div>
                )}

                {!!tableCats.length && (
                    <div className="grid grid-cols-1 xl:grid-cols-4 gap-6">
                        <div className="col-span-1 xl:col-span-2 flex flex-col gap-6">
                            {tableCats.slice(0, 1)}
                        </div>
                        <div className="col-span-1 xl:col-span-1 flex flex-col gap-6">
                            {tableCats.slice(1, 2)}
                        </div>
                        <div className="col-span-1 xl:col-span-1 flex flex-col gap-6">
                            {tableCats.slice(2)}
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
};

export default DashboardPage;
