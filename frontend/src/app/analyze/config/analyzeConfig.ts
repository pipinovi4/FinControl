/* ------------------------------------------------------------------
 * Конфиг страницы «Аналитика».
 * -----------------------------------------------------------------*/
import { API } from "@/lib/api";

export type SearchField = { label: string; param: string };
export type Column      = { label: string; key: string };

export type EntityKey   = 'clients' | 'brokers' | 'workers';
export type RoleKey     = 'worker' | 'broker' | 'admin';

export type EntityCfg = {
    entityLabel : string;
    endpoint    : string;
    fields      : SearchField[];
    columns     : Column[];
    detailEndpoint?: string;
};

export type RoleCfg = {
    pageSize: number;
    entities: Partial<Record<EntityKey, EntityCfg>>;
};

/* base arrays */

const clientSearch: SearchField[] = [
    { label: 'E-mail',  param: 'email' },
    { label: 'Телефон', param: 'phone_number' },
    { label: 'ФИО',     param: 'full_name' },
];

const clientCols: Column[] = [
    { label: 'ФИО',     key: 'full_name'   },
    { label: 'Телефон', key: 'phone_number'},
    { label: 'E-mail',  key: 'email'       },
    { label: 'Статус',  key: '__status'    }, // ← NEW
];

const brokerCols: Column[] = [
    { label: 'Почта',    key: 'email'       },
    { label: 'Компания', key: 'company_name'},
    { label: 'Регионы',  key: 'region'      },
    { label: 'Создан',   key: 'created_at'  },
    { label: 'Статус',   key: '__status'    }, // ← NEW
];

const workerCols: Column[] = [
    { label: 'Почта',   key: 'email'      },
    { label: 'Никнейм', key: 'username'   },
    { label: 'Создан',  key: 'created_at' },
    { label: 'Статус',  key: '__status'   }, // ← NEW
];

/* endpoints */

const workerBase  = `${API}/api/dashboard/worker/client/filter/bucket/`;
const brokerBase  = `${API}/api/dashboard/broker/client/filter/bucket/`;
const adminClBase = `${API}/api/dashboard/admin/clients/filter/bucket/`;
const adminBrBase = `${API}/api/dashboard/admin/brokers/filter/bucket/`;
const adminWrBase = `${API}/api/dashboard/admin/workers/filter/bucket/`;

/* final cfg */

export const ANALYZE_CFG: Record<RoleKey, RoleCfg> = {
    worker: {
        pageSize: 6,
        entities: {
            clients: { entityLabel: 'Клиенты', endpoint: workerBase, fields: clientSearch, columns: clientCols },
        },
    },
    broker: {
        pageSize: 6,
        entities: {
            clients: { entityLabel: 'Клиенты', endpoint: brokerBase, fields: clientSearch, columns: clientCols },
        },
    },
    admin: {
        pageSize: 8,
        entities: {
            clients: {
                entityLabel: 'Клиенты',
                endpoint   : adminClBase,
                fields     : clientSearch,
                columns    : clientCols,
                detailEndpoint: `${API}/api/dashboard/admin/client/`,
            },
            brokers: {
                entityLabel: 'Брокеры',
                endpoint   : adminBrBase,
                fields     : [
                    { label: 'Почта',    param: 'email' },
                    { label: 'Компания', param: 'company_name' },
                    { label: 'Регионы',  param: 'region' },
                ],
                detailEndpoint: `${API}/api/dashboard/admin/broker/`,
                columns    : brokerCols,
            },
            workers: {
                entityLabel: 'Работники',
                endpoint   : adminWrBase,
                fields     : [
                    { label: 'Почта',   param: 'email' },
                    { label: 'Никнейм', param: 'username' },
                ],
                detailEndpoint: `${API}/api/dashboard/admin/worker/`,
                columns    : workerCols,
            },
        },
    },
};
