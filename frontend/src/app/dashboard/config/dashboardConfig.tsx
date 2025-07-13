import React from 'react';
import {
    DollarIcon,
    AnalyzeIcon,
    DealIcon,
    CompletedIcon,
} from '@/components/icons';

import StatCard         from '@/app/dashboard/components/StatCard';
import IncomeChart      from '@/app/dashboard/components/IncomeChart';
import DailyTrafficCard from '@/app/dashboard/components/DailyTraffic';
import UserTable        from '@/app/dashboard/components/UserTable';
import PieStatusCard    from '@/app/dashboard/components/PieStatusCard';
import CalendarCard     from '@/app/dashboard/components/CalendarCard';

/* ---------- types ---------- */
export type ComponentFactory = (v: any) => React.ReactNode;

export type StaticMetric = {
    fetchUrl: string;
    render: ComponentFactory;
};

export type EnhancedStaticMetric = {
    fetchUrl: string;
    requiresId: boolean;
    render: ComponentFactory;
};

type RoleConfig = {
    static?: Record<string, EnhancedStaticMetric>;
    graphic?: Record<string, StaticMetric>;
    tables?: Record<string, StaticMetric>;
};

export type DashboardConfig = Record<'worker' | 'broker' | 'admin', RoleConfig>;

/* ---------- config ---------- */
const dashboardConfig: DashboardConfig = {
    worker: {
        static: {
            totalClients: {
                fetchUrl: 'http://localhost:8000/api/dashboard/worker/client/sum/',
                requiresId: true,
                render: (v) => <StatCard icon={<DealIcon className="w-11 h-11" />} label="Всего клиентов" value={v} />,
            },
            totalEarned: {
                fetchUrl: 'http://localhost:8000/api/dashboard/worker/client/earnings/total/',
                requiresId: true,
                render: (v) => <StatCard icon={<DollarIcon className="w-11 h-11" />} label="Всего заработано" value={v} />,
            },
            earnedMonthly: {
                fetchUrl: 'http://localhost:8000/api/dashboard/worker/client/earnings/month/',
                requiresId: true,
                render: (v) => <StatCard icon={<AnalyzeIcon className="w-5 h-5 text-primary" />} label="Заработано за месяц" value={v} />,
            },
            totalDeals: {
                fetchUrl: 'http://localhost:8000/api/dashboard/worker/client/deals-sum/',
                requiresId: true,
                render: (v) => <StatCard icon={<CompletedIcon className="w-11 h-11 text-white" />} label="Всего сделок" value={v} />,
            },
        },
        graphic: {
            incomeChart: {
                fetchUrl: '',
                render: (v) => <IncomeChart  />,
            },
            dailyTraffic: {
                fetchUrl: '',
                render: (v) => <DailyTrafficCard />,
            },
        },
        tables: {
            userTable: {
                fetchUrl: '',
                render: (v) => <UserTable  />,
            },
            statusPie: {
                fetchUrl: '',
                render: (v) => <PieStatusCard  />,
            },
            calendar: {
                fetchUrl: '',
                render: (v) => <CalendarCard  />,
            },
        },
    },

    broker: {
        static: {
            totalCommission: {
                fetchUrl: 'http://localhost:8000/api/dashboard/broker/client/credits/sum/',
                requiresId: true,
                render: (v) => <StatCard icon={<DollarIcon className="w-11 h-11" />} label="Всего комиссий" value={v} />,
            },
            commissionMonth: {
                fetchUrl: 'http://localhost:8000/api/dashboard/broker/client/credits/month/',
                requiresId: true,
                render: (v) => <StatCard icon={<AnalyzeIcon className="w-5 h-5 text-primary" />} label="Комиссия за месяц" value={v} />,
            },
            activeCredits: {
                fetchUrl: 'http://localhost:8000/api/dashboard/broker/client/credits/active/',
                requiresId: true,
                render: (v) => <StatCard icon={<DealIcon className="w-11 h-11" />} label="Активные кредиты" value={v} />,
            },
            completedCredits: {
                fetchUrl: 'http://localhost:8000/api/dashboard/broker/client/credits/completed/',
                requiresId: true,
                render: (v) => <StatCard icon={<CompletedIcon className="w-11 h-11 text-white" />} label="Завершено кредитов" value={v} />,
            },
        },
        graphic: {
            incomeChart: {
                fetchUrl: '',
                render: (v) => <IncomeChart  />,
            },
            dailyTraffic: {
                fetchUrl: '',
                render: (v) => <DailyTrafficCard  />,
            },
        },
        tables: {
            userTable: {
                fetchUrl: '',
                render: (v) => <UserTable  />,
            },
            statusPie: {
                fetchUrl: '',
                render: (v) => <PieStatusCard  />,
            },
        },
    },

    admin: {
        static: {
            totalSum: {
                fetchUrl: 'http://localhost:8000/api/dashboard/admin/earnings/total/',
                requiresId: false,
                render: (v) => <StatCard icon={<DollarIcon className="w-11 h-11" />} label="Всего заработано" value={v} />,
            },
            monthlySum: {
                fetchUrl: 'http://localhost:8000/api/dashboard/admin/earnings/month/',
                requiresId: false,
                render: (v) => <StatCard icon={<AnalyzeIcon className="w-5 h-5 text-primary" />} label="Заработано за месяц" value={v} />,
            },
            totalAccounts: {
                fetchUrl: 'http://localhost:8000/api/dashboard/admin/clients/total',
                requiresId: false,
                render: (v) => <StatCard icon={<DealIcon className="w-11 h-11" />} label="Всего аккаунтов" value={v} />,
            },
            totalCredits: {
                fetchUrl: 'http://localhost:8000/api/dashboard/admin/credits/total/',
                requiresId: false,
                render: (v) => <StatCard icon={<CompletedIcon className="w-11 h-11 text-white" />} label="Всего комиссий" value={v} />,
            },
            monthlyCredits: {
                fetchUrl: 'http://localhost:8000/api/dashboard/admin/credits/month/',
                requiresId: false,
                render: (v) => <StatCard icon={<CompletedIcon className="w-11 h-11 text-white" />} label="Комиссий за месяц" value={v} />,
            },
            totalDeals: {
                fetchUrl: 'http://localhost:8000/api/dashboard/admin/deals/count/',
                requiresId: false,
                render: (v) => <StatCard icon={<CompletedIcon className="w-11 h-11 text-white" />} label="Всего сделок" value={v} />,
            },
        },
        graphic: {
            incomeChart: {
                fetchUrl: '',
                render: (v) => <IncomeChart  />,
            },
            dailyTraffic: {
                fetchUrl: '',
                render: (v) => <DailyTrafficCard  />,
            },
        },
        tables: {
            userTable: {
                fetchUrl: '',
                render: (v) => <UserTable  />,
            },
            statusPie: {
                fetchUrl: '',
                render: (v) => <PieStatusCard  />,
            },
            calendar: {
                fetchUrl: '',
                render: (v) => <CalendarCard  />,
            },
        },
    },
};

export default dashboardConfig;


// import React from 'react';
// import {
//     DollarIcon,
//     AnalyzeIcon,
//     DealIcon,
//     CompletedIcon,
// } from '@/components/icons';
//
// import StatCard         from '@/app/dashboard/components/StatCard';
// import IncomeChart      from '@/app/dashboard/components/IncomeChart';
// import DailyTrafficCard from '@/app/dashboard/components/DailyTraffic';
// import UserTable        from '@/app/dashboard/components/UserTable';
// import PieStatusCard    from '@/app/dashboard/components/PieStatusCard';
// import CalendarCard     from '@/app/dashboard/components/CalendarCard';
//
// /* ---------- types ---------- */
// export type ComponentFactory = (v: any) => React.ReactNode;
//
// export type StaticMetric = {
//     fetchUrl: string;
//     render: ComponentFactory;
// };
//
// type RoleConfig = {
//     static?: Record<string, StaticMetric>;
//     graphic?: Record<string, StaticMetric>;
//     tables?: Record<string, StaticMetric>;
// };
//
// export type DashboardConfig = Record<'worker' | 'broker' | 'admin', RoleConfig>;
//
// /* ---------- config ---------- */
// const dashboardConfig: DashboardConfig = {
//     worker: {
//         static: {
//             totalClients: {
//                 fetchUrl: 'http://localhost:8000/api/dashboard/worker/client/sum/',
//                 render: (v) => (
//                     <StatCard
//                         icon={<DealIcon className="w-11 h-11" />}
//                         values={[{ key: 'clients', label: 'Всего клиентов', value: v }]}
//                     />
//                 ),
//             },
//             totalEarned: {
//                 fetchUrl: 'http://localhost:8000/api/dashboard/worker/client/earnings/total/',
//                 render: (v) => (
//                     <StatCard
//                         icon={<DollarIcon className="w-11 h-11" />}
//                         values={[{ key: 'earned_total', label: 'Всего заработано', value: v }]}
//                     />
//                 ),
//             },
//             earnedMonthly: {
//                 fetchUrl: 'http://localhost:8000/api/dashboard/worker/client/earnings/month/',
//                 render: (v) => (
//                     <StatCard
//                         icon={<AnalyzeIcon className="w-5 h-5 text-primary" />}
//                         values={[{ key: 'earned_month', label: 'Заработано за месяц', value: v }]}
//                     />
//                 ),
//             },
//             totalDeals: {
//                 fetchUrl: 'http://localhost:8000/api/dashboard/worker/client/deals-sum/',
//                 render: (v) => (
//                     <StatCard
//                         icon={<CompletedIcon className="w-11 h-11 text-white" />}
//                         values={[{ key: 'deals', label: 'Всего сделок', value: v }]}
//                     />
//                 ),
//             },
//         },
//         graphic: {
//             incomeChart: {
//                 fetchUrl: '',
//                 render: (v) => <IncomeChart />,
//             },
//             dailyTraffic: {
//                 fetchUrl: '',
//                 render: (v) => <DailyTrafficCard />,
//             },
//         },
//         tables: {
//             userTable: {
//                 fetchUrl: '',
//                 render: (v) => <UserTable />,
//             },
//             statusPie: {
//                 fetchUrl: '',
//                 render: (v) => <PieStatusCard />,
//             },
//             calendar: {
//                 fetchUrl: '',
//                 render: (v) => <CalendarCard />,
//             },
//         },
//     },
//
//     broker: {
//         static: {
//             totalCommission: {
//                 fetchUrl: 'http://localhost:8000/api/dashboard/broker/client/credits/sum/',
//                 render: (v) => (
//                     <StatCard
//                         icon={<DollarIcon className="w-11 h-11" />}
//                         values={[{ key: 'commission', label: 'Всего комиссий', value: v }]}
//                     />
//                 ),
//             },
//             commissionMonth: {
//                 fetchUrl: 'http://localhost:8000/api/dashboard/broker/client/credits/month/',
//                 render: (v) => (
//                     <StatCard
//                         icon={<AnalyzeIcon className="w-5 h-5 text-primary" />}
//                         values={[{ key: 'commission_month', label: 'Комиссия за месяц', value: v }]}
//                     />
//                 ),
//             },
//             activeCredits: {
//                 fetchUrl: 'http://localhost:8000/api/dashboard/broker/client/credits/active/',
//                 render: (v) => (
//                     <StatCard
//                         icon={<DealIcon className="w-11 h-11" />}
//                         values={[{ key: 'active', label: 'Активные кредиты', value: v }]}
//                     />
//                 ),
//             },
//             completedCredits: {
//                 fetchUrl: 'http://localhost:8000/api/dashboard/broker/client/credits/completed/',
//                 render: (v) => (
//                     <StatCard
//                         icon={<CompletedIcon className="w-11 h-11 text-white" />}
//                         values={[{ key: 'completed', label: 'Завершено кредитов', value: v }]}
//                     />
//                 ),
//             },
//         },
//         graphic: {
//             incomeChart: {
//                 fetchUrl: '',
//                 render: (v) => <IncomeChart />,
//             },
//             dailyTraffic: {
//                 fetchUrl: '',
//                 render: (v) => <DailyTrafficCard />,
//             },
//         },
//         tables: {
//             userTable: {
//                 fetchUrl: '',
//                 render: (v) => <UserTable />,
//             },
//             statusPie: {
//                 fetchUrl: '',
//                 render: (v) => <PieStatusCard />,
//             },
//         },
//     },
//
//     admin: {
//         static: {
//             totalSum: {
//                 fetchUrl: 'http://localhost:8000/api/dashboard/admin/earnings/total/',
//                 render: (v) => (
//                     <StatCard
//                         icon={<DollarIcon className="w-11 h-11" />}
//                         values={[{ key: 'sum', label: 'Всего заработано', value: v }]}
//                     />
//                 ),
//             },
//             monthlySum: {
//                 fetchUrl: 'http://localhost:8000/api/dashboard/admin/earnings/month/',
//                 render: (v) => (
//                     <StatCard
//                         icon={<AnalyzeIcon className="w-5 h-5 text-primary" />}
//                         values={[{ key: 'monthly', label: 'Заработано за месяц', value: v }]}
//                     />
//                 ),
//             },
//             totalAccounts: {
//                 fetchUrl: 'http://localhost:8000/api/dashboard/admin/clients/total/',
//                 render: (v) => (
//                     <StatCard
//                         icon={<DealIcon className="w-11 h-11" />}
//                         values={[
//                             { key: 'users', label: 'Всего пользователей', value: v },
//                             { key: 'brokers', label: 'Всего брокеров', value: v },
//                             { key: 'workers', label: 'Всего работников', value: v },
//                             { key: 'clients', label: 'Всего клиентов', value: v },
//                         ]}
//                         defaultKey="users"
//                     />
//                 ),
//             },
//             totalCredits: {
//                 fetchUrl: 'http://localhost:8000/api/dashboard/admin/credits/total/',
//                 render: (v) => (
//                     <StatCard
//                         icon={<CompletedIcon className="w-11 h-11 text-white" />}
//                         // values={[{ key: 'credits', label: 'Всего кредитов', value: v }]}
//                         value={v}
//                     />
//                 ),
//             },
//             totalDeals: {
//                 fetchUrl: 'http://localhost:8000/api/dashboard/admin/deals/count/',
//                 render: (v) => (
//                     <StatCard
//                         icon={<CompletedIcon className="w-11 h-11 text-white" />}
//                         // values={[{ key: 'deals', label: 'Всего сделок', value: v }]}
//                         value={v}
//                     />
//                 ),
//             },
//         },
//         graphic: {
//             incomeChart: {
//                 fetchUrl: '',
//                 render: (v) => <IncomeChart />,
//             },
//             dailyTraffic: {
//                 fetchUrl: '',
//                 render: (v) => <DailyTrafficCard />,
//             },
//         },
//         tables: {
//             userTable: {
//                 fetchUrl: '',
//                 render: (v) => <UserTable />,
//             },
//             statusPie: {
//                 fetchUrl: '',
//                 render: (v) => <PieStatusCard />,
//             },
//             calendar: {
//                 fetchUrl: '',
//                 render: (v) => <CalendarCard />,
//             },
//         },
//     },
// };
//
// export default dashboardConfig;
