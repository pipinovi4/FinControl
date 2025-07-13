import { OutputOf } from '@/lib/metaFetch';

type Role = 'admin' | 'worker' | 'broker';

type LoginResponseByRole = {
    admin: OutputOf<'/api/auth/login/admin/web'>;
    worker: OutputOf<'/api/auth/login/worker/web'>;
    broker: OutputOf<'/api/auth/login/broker/web'>;
};

type StoredUserType = {
    role: Role;
    data: LoginResponseByRole[Role];
};

export default StoredUserType;
