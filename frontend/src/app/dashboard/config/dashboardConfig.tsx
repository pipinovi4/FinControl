import React from 'react';
import {
    DollarIcon,
    AnalyzeIcon,
    DealIcon,
    CompletedIcon,
} from '@/components/icons';
import { API } from "@/lib/api";

import StatCard         from '@/app/dashboard/components/StatCard';
import IncomeChart      from '@/app/dashboard/components/IncomeChart';
import DailyTrafficCard from '@/app/dashboard/components/DailyTraffic';
import UserTable        from '@/app/dashboard/components/UserTable/UserTable';
import PieStatusCard    from '@/app/dashboard/components/PieStatusCard';
import {
    mapAdminClient,
    mapBroker,
    mapBrokerClient,
    mapWorker,
    mapWorkerClient
} from "@/app/dashboard/components/UserTable/types";
import InviteGenerator from "@/app/dashboard/components/InviteGenerator";
import CreateUser from "@/app/dashboard/components/CreateUser/CreateUser";
import AdminPromotions from "@/app/dashboard/components/Promotion/Promotion";

import CreditsCenter from "@/app/dashboard/components/CreditsNode";

/* ---------- types ---------- */
/* ---------- types ---------- */
export type ComponentFactory = () => React.ReactNode;

export type StaticMetric = {
    requiresId: boolean;
    render: ComponentFactory;
};

// 🔧 ДОДАЙ creditsNode у тип ролі
type RoleConfig = {
    static?: Record<string, StaticMetric>;
    graphic?: Record<string, StaticMetric>;
    tables?:  Record<string, StaticMetric>;
    actionCards?:  Record<string, StaticMetric>;
    creditsNode?: Record<string, StaticMetric>;            // ← нове
};

export type DashboardConfig = Record<'worker' | 'broker' | 'admin', RoleConfig>;

/* ---------- configs ---------- */
const dashboardConfig: DashboardConfig = {
    /* ─── WORKER ───────────────────────────────────────────── */
    worker: {
        static: {
            // totalClients: {
            //     requiresId: true,
            //     render: () => (
            //         <StatCard
            //             icon={<DealIcon className="w-11 h-11" />}
            //             labels={['Всего клиентов', 'Новых клиентов']}
            //             fetchUrls={['${API}/api/dashboard/worker/client/sum/', '${API}/api/dashboard/worker/client/new-today/count/']}
            //             requiresId
            //         />
            //     ),
            // },
            // totalEarned: {
            //     requiresId: true,
            //     render: () => (
            //         <StatCard
            //             icon={<DollarIcon className="w-11 h-11" />}
            //             labels={['Всего заработано']}
            //             fetchUrls={['${API}/api/dashboard/worker/client/earnings/total/']}
            //             requiresId
            //         />
            //     ),
            // },
            // earnedMonthly: {
            //     requiresId: true,
            //     render: () => (
            //         <StatCard
            //             icon={<AnalyzeIcon className="w-5 h-5 text-primary" />}
            //             labels={['Заработано за месяц']}
            //             fetchUrls={['${API}/api/dashboard/worker/client/earnings/month/']}
            //             requiresId
            //         />
            //     ),
            // },
            // totalDeals: {
            //     requiresId: true,
            //     render: () => (
            //         <StatCard
            //             icon={<CompletedIcon className="w-11 h-11 text-white" />}
            //             labels={['Всего сделок']}
            //             fetchUrls={['${API}/api/dashboard/worker/client/deals-sum/']}
            //             requiresId
            //         />
            //     ),
            // },
        },

        graphic: {
            // incomeChart: {
            //     requiresId: true,
            //     render: () => (
            //         <IncomeChart
            //             labels={['Заработано']}
            //             monthUrls={[`${API}/api/dashboard/worker/client/earnings/sum/monthly/`]}
            //             yearUrls={[`${API}/api/dashboard/worker/client/earnings/sum/yearly/`]}
            //             requiresId
            //         />
            //     )
            // },
            // dailyTraffic: {
            //     requiresId: true,
            //     render: () => (
            //         <DailyTrafficCard
            //             labels={['Новые клиенты']}
            //             fetchUrls={['${API}/api/dashboard/worker/client/new-today/']}
            //             yesterdayUrls={['${API}/api/dashboard/worker/client/new-today/']}
            //             requiresId
            //         />
            //     )
            // },
        },

        tables: {
            userTable:  {
                requiresId: true,
                render: () => (
                    <UserTable
                        labels={['Клиенты']}
                        userBucketURL={['${API}/api/dashboard/worker/client/bucket/']}
                        getFullUserURL={['${API}/api/dashboard/worker/client/']}
                        tableHeads={[
                            ['ФИО', 'Телефон', 'Адрес', 'Взят в роботу'],
                        ]}
                        // buttonActionLabel={['Отписать клиента']}
                        // buttonActionURL={['${API}/api/dashboard/worker/client/unsign/']}
                        // requiresButton={true}
                        rowMappers={[mapWorkerClient]}
                        colKeys={[
                            ['name', 'phone', 'fact_address', 'date'],
                        ]}
                        requiresId
                        pageSize={20}
                    />
                )
            },
            // statusPie:  {
            //     requiresId: true,
            //     render: () => (
            //         <PieStatusCard
            //             labels={['Статус клиентов']}
            //             labelsActive={['В процессе']}
            //             labelsCompleted={['Закрытые']}
            //             activeUrls={['${API}/api/dashboard/worker/client/active/count/']}
            //             completedUrls={['${API}/api/dashboard/worker/client/completed/count/']}
            //             requiresId
            //         />
            //     )
            // },
        },
    },

    /* ─── BROKER ───────────────────────────────────────────── */
    broker: {
        static: {
            totalCommission: {
                requiresId: true,
                render: () => (
                    <StatCard
                        icon={<DollarIcon className="w-11 h-11" />}
                        labels={['Комиссий', 'Комиссий за месяц']}
                        fetchUrls={['${API}/api/dashboard/broker/client/credits/sum/total/', '${API}/api/dashboard/broker/client/credits/sum/month/']}
                        requiresId
                    />
                ),
            },
            commissionsCount: {
                requiresId: true,
                render: () => (
                    <StatCard
                        icon={<AnalyzeIcon className="w-5 h-5 text-primary" />}
                        labels={['Всего комиссий', 'Комиссий за месяц']}
                        fetchUrls={['${API}/api/dashboard/broker/client/credits/count/total/', '${API}/api/dashboard/broker/client/credits/count/month/']}
                        requiresId
                    />
                ),
            },
            creditsStatus: {
                requiresId: true,
                render: () => (
                    <StatCard
                        icon={<DealIcon className="w-11 h-11" />}
                        labels={['Активные кредиты', 'Завершено кредитов']}
                        fetchUrls={['${API}/api/dashboard/broker/client/credits/count/active/', '${API}/api/dashboard/broker/client/credits/count/completed/']}
                        requiresId
                    />
                ),
            },
            completedCredits: {
                requiresId: true,
                render: () => (
                    <StatCard
                        icon={<CompletedIcon className="w-11 h-11 text-white" />}
                        labels={['Комиссии активных кредитов', 'Комиссии не активных кредитов']}
                        fetchUrls={[
                            '${API}/api/dashboard/broker/client/credits/sum/active/',
                            '${API}/api/dashboard/broker/client/credits/sum/completed/',
                        ]}
                        requiresId
                    />
                ),
            },
        },

        graphic: {
            incomeChart: {
                requiresId: true,
                render: () => (
                    <IncomeChart
                        labels={['Заработано']}
                        monthUrls={[`${API}/api/dashboard/broker/client/credits/sum/monthly/`]}
                        yearUrls={[`${API}/api/dashboard/broker/client/credits/sum/yearly/`]}
                        requiresId
                    />
                )
            },
            dailyTraffic: {
                requiresId: true,
                render: () => (
                    <DailyTrafficCard
                        labels={['Новые клиенты']}
                        fetchUrls={['${API}/api/dashboard/broker/client/new-today/']}
                        yesterdayUrls={['${API}/api/dashboard/broker/client/new-yesterday/sum/']}
                        requiresId
                    />
                )
            },
        },

        tables: {
            creditsNode: {
                requiresId: false,
                render: () => <CreditsCenter />
            },
            statusPie:  {
                requiresId: true,
                render: () => (
                    <PieStatusCard
                        labels={['Статус клиентов']}
                        labelsActive={['В процессе']}
                        labelsCompleted={['Закрытые']}
                        activeUrls={['${API}/api/dashboard/broker/client/credits/count/active/']}
                        completedUrls={['${API}/api/dashboard/broker/client/credits/count/completed/']}
                        requiresId
                    />
                )
            },
        },
        creditsNode: {
            userTable:  {
                requiresId: true,
                render: () => (
                    <UserTable
                        labels={['Клиенты']}
                        userBucketURL={['${API}/api/dashboard/broker/client/signed/bucket/']}
                        getFullUserURL={['${API}/api/dashboard/broker/client/']}
                        tableHeads={[
                            ['ФИО', 'Телефон', 'Адрес', 'Взят в роботу'],
                        ]}
                        colKeys={[
                            ['name', 'phone', 'fact_address', 'date'],
                        ]}
                        rowMappers={[mapBrokerClient]}
                        requiresId
                        pageSize={20}
                    />
                )
            },
        },
    },

    /* ─── ADMIN ────────────────────────────────────────────── */
    admin: {
        static: {
            totalSums: {
                requiresId: false,
                render: () => (
                    <StatCard
                        icon={<DollarIcon className="w-11 h-11" />}
                        labels={['Всего выдано']}
                        fetchUrls={['${API}/api/dashboard/admin/credits/total/']}
                    />
                ),
            },
            monthlySums: {
                requiresId: false,
                render: () => (
                    <StatCard
                        // Или вместо выдано можна написать "Комиссий за месяц"
                        icon={<AnalyzeIcon className="w-5 h-5 text-primary" />}
                        labels={['Выдано за месяц']}
                        fetchUrls={['${API}/api/dashboard/admin/credits/month/']}
                    />
                ),
            },
            totalAccounts: {
                requiresId: false,
                render: () => (
                    <StatCard
                        icon={<DealIcon className="w-11 h-11 text-white" />}
                        labels={[
                            'Всего пользователей',
                            'Всего клиентов',
                            'Всего брокеров',
                            'Всего работников',
                        ]}
                        fetchUrls={[
                            '${API}/api/dashboard/admin/users/total',    // <- змініть на свої, якщо різні
                            '${API}/api/dashboard/admin/clients/total',
                            '${API}/api/dashboard/admin/brokers/total',
                            '${API}/api/dashboard/admin/workers/total',
                        ]}
                    />
                ),
            },
            totalDeals: {
                requiresId: false,
                render: () => (
                    <StatCard
                        icon={<CompletedIcon className="w-11 h-11 text-white" />}
                        labels={['Всего комиссий']}
                        fetchUrls={['${API}/api/dashboard/admin/credits/count/']}
                    />
                ),
            },
        },

        graphic: {
            incomeChart: {
                requiresId: false,
                render: () => (
                    <IncomeChart
                        labels={['Комиссий всего']}
                        monthUrls={[`${API}/api/dashboard/admin/credits/sum/monthly/`]}
                        yearUrls={[`${API}/api/dashboard/admin/credits/sum/yearly/`]}
                        requiresId={false}
                    />
                )
            },
            dailyTraffic: {
                requiresId: true,
                render: () => (
                    <DailyTrafficCard
                        labels={['Новых работников', 'Новых брокеров', 'Новые клиенты (Работники)', "Новые клиенты (Брокеры)"]}
                        fetchUrls={['${API}/api/dashboard/admin/workers/new-today/', '${API}/api/dashboard/admin/brokers/new-today/', '${API}/api/dashboard/admin/workers/clients/new-today/', '${API}/api/dashboard/admin/brokers/clients/new-today/']}
                        yesterdayUrls={['${API}/api/dashboard/admin/workers/new-yesterday/', '${API}/api/dashboard/admin/brokers/new-yesterday/','${API}/api/dashboard/admin/workers/clients/new-yesterday/', '${API}/api/dashboard/admin/brokers/clients/new-today/']}
                        requiresId
                    />
                )
            },
        },

        tables: {
            creditsNode: {
                requiresId: false,
                render: () => <CreditsCenter />
            },
            generateLink: {
                requiresId: true,
                render: () => (
                    <InviteGenerator/>
                )
            },
        },
        actionCards: {
            statusPie:  {
                requiresId: true,
                render: () => (
                    <PieStatusCard
                        labels={['Статус кредитов']}
                        labelsActive={['В процессе']}
                        labelsCompleted={['Закрытые']}
                        activeUrls={['${API}/api/dashboard/admin/credits/count/active/']}
                        completedUrls={['${API}/api/dashboard/admin/credits/count/completed/']}
                        requiresId
                    />
                )
            },
            createUser: {
                requiresId: false,
                render: () => (
                    <CreateUser
                        defaultRole="CLIENT"

                        /* список полів — 4 масиви у порядку WORKER, BROKER, CLIENT, ADMIN */
                        fieldsList={[
                            // ────────── WORKER ──────────
                            [
                                { name: "email",  label: "Email",  type: "email" },
                                { name: "password", label: "Пароль", type: "text" },
                                { name: "username", label: "Логин", type: "text" },
                                { name: "community", label: "Сообщество", type: "select", options: ["Helix", "Union"] },
                            ],
                            // ────────── BROKER ──────────
                            [
                                { name: "email",  label: "Email",  type: "email" },
                                { name: "password", label: "Пароль", type: "text" },
                                { name: "region",  label: "Регион (список)", type: "array" },
                                { name: "company_name", label: "Компания", type: "text" },
                            ],
                            // ────────── CLIENT ──────────
                            [
                                /* — обов’язкові — */
                                { name: "worker_username", label: "Логин работника",      type: "text" },
                                { name: "full_name",       label: "ФИО",                    type: "text" },
                                { name: "phone_number",    label: "Телефон",                type: "text" },
                                { name: "email",           label: "Почта",                  type: "email" },
                                { name: "password",        label: "Пароль",                 type: "password" },

                                /* — сума, якщо вже відома — */
                                { name: "amount",          label: "Сумма кредита",          type: "int",    optional: true },

                                /* — паспорт / податкові дані — */
                                { name: "snils",           label: "СНИЛС",                  type: "text",   optional: true },
                                { name: "inn",             label: "ИНН",                    type: "text",   optional: true },

                                /* — адреси — */
                                { name: "reg_address",     label: "Адреса прописки",        type: "text",   optional: true },
                                { name: "fact_address",    label: "Факт. адреса",           type: "text",   optional: true },

                                /* — особисті дані — */
                                { name: "reg_date",        label: "Дата регистрации",       type: "text",   optional: true },
                                { name: "family_status",   label: "Семейное положение",     type: "text",   optional: true },

                                /* — робота клієнта — */
                                { name: "workplace",           label: "Место работы",           type: "text", optional: true },
                                { name: "org_legal_address",   label: "Юр. адрес организации",  type: "text", optional: true },
                                { name: "org_fact_address",    label: "Факт. адрес организации",type: "text", optional: true },
                                { name: "position",            label: "Должность",              type: "text", optional: true },
                                { name: "income",              label: "Доход (₽)",            type: "int",  optional: true },
                                { name: "income_proof",        label: "Подтверждение дохода",    type: "text", optional: true },
                                { name: "employment_date",     label: "Дата трудоустройства",    type: "text", optional: true },
                                { name: "org_activity",        label: "Сфера деятельности орг.", type: "text", optional: true },

                                /* — активи та дод. прибуток — */
                                { name: "assets",        label: "Активы",        type: "text", optional: true },
                                { name: "extra_income",  label: "Доп. доход",    type: "text", optional: true },

                                /* — контакти та файли — */
                                { name: "contact_person", label: "Контактное лицо", type: "text",  optional: true },
                                { name: "report_files",   label: "Файлы отчёта",    type: "array", optional: true }
                            ],
                            // ────────── ADMIN ───────────
                            [
                                { name: "email",  label: "Email",  type: "email" },
                                { name: "password", label: "Пароль", type: "text" },
                                { name: "display_name", label: "Display Name", type: "text" },
                            ],
                        ]}

                        /* ендпоїнти у тому ж порядку */
                        registrationUrls={[
                            `${API}/api/entities/create/worker`,
                            `${API}/api/entities/create/broker`,
                            `${API}/api/entities/create/client`,
                            `${API}/api/entities/create/admin`  ,
                        ]}
                    />
                ),
            },
            promotion: {
                requiresId: true,
                render: () => (
                    <AdminPromotions/>
                ),
            },
        },
        creditsNode: {
            userTable:  {
                requiresId: true,
                render: () => (
                    <UserTable
                        labels={['Работники', 'Брокеры', 'Клиенты']}
                        userBucketURL={['${API}/api/dashboard/admin/workers/', '${API}/api/dashboard/admin/brokers/', '${API}/api/dashboard/admin/clients/']}
                        getFullUserURL={['${API}/api/dashboard/admin/worker/', '${API}/api/dashboard/admin/broker/', '${API}/api/dashboard/admin/client/']}
                        tableHeads={[
                            ['Почта', 'Никнейм', 'Создан'],           // Workers
                            ['Почта', 'Компания', 'Регионы', 'Создан'],           // Brokers
                            ['ФИО', 'Телефон', 'Адрес', 'Создан'],    // Clients
                        ]}
                        colKeys={[
                            ['email', 'username', 'date'],          // Brokers
                            ['email', 'company', 'region', 'date'],          // Brokers
                            ['name', 'phone', 'fact_address', 'date'],       // Clients  ✅
                        ]}
                        pageSize={10}
                        rowMappers={[mapWorker, mapBroker, mapAdminClient]}
                        requiresId
                    />
                )
            },
        },
    },
};

export default dashboardConfig;
