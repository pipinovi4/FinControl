import { metaFetch, InputOf, OutputOf } from '@/lib/metaFetch';
import UserStorage from "@/services/UserStorage";
import { API, api } from "@/lib/api";


/* ─────────── roles & helpers ─────────── */

type Role = 'admin' | 'worker' | 'broker' | 'client';
const makePath  = (action: 'login' | 'register', role: Role) =>
    `/api/auth/${action}/${role}/web`;
const makeInvite = (role: 'worker' | 'broker', token: string) =>
    `/api/auth/register/invite/${role}/${token}`;

/* ─────────── DTO-type helpers ─────────── */

type LoginInput   = InputOf<`/api/auth/login/web`>;
type LoginOutput   = OutputOf<`/api/auth/login/web`>;
type RegisterInput<R extends Role> = InputOf<`/api/auth/register/${R}/web`>;
type RegisterOutput<R extends Role>= OutputOf<`/api/auth/register/${R}/web`>;
type RefreshOutput                 = OutputOf<'/api/auth/refresh'>;

async function fetchJson<T>(
    path: string,
    opts: RequestInit = {},
): Promise<T> {
    const res = await fetch(api(path), {
        headers: { 'Content-Type': 'application/json', ...(opts.headers || {}) },
        credentials: 'include',
        ...opts,
    });

    if (!res.ok) {
        const errTxt = await res.text().catch(() => '');
        throw new Error(`${res.status}: ${errTxt || res.statusText}`);
    }
    return await res.json() as Promise<T>;
}
/* ─────────── AuthService ─────────── */

export const authService = {
    /** `/api/auth/login/<role>/web` */
    async login(
        data: LoginInput,
    ): Promise<LoginOutput> {
        const res = await metaFetch("/api/auth/login/web", data, {credentials: 'include'});
        UserStorage.set(res);
        return res;
    },

    /** `/api/auth/register/<role>/web` */
    async register<R extends Role>(
        role: R,
        data: RegisterInput<R>,
    ): Promise<RegisterOutput<R>> {
        const res = await metaFetch(makePath('register', role), data, { credentials: 'include' })
        UserStorage.set(res);
        return res;
    },

    /** `/api/auth/refresh` */
    refresh(): Promise<RefreshOutput> {
        return metaFetch('refresh', {}, { credentials: 'include' });
    },

    /** `/api/auth/logout` */
    async logout(): Promise<void> {
        const res = await fetch(`${API}/api/session/logout`, {
            method: 'POST',
            credentials: 'include',
        });

        if (res.status === 200) {
            localStorage.removeItem('user');
            localStorage.removeItem('analyzeCache');
            localStorage.removeItem('analyzeState');
        } else {
            console.error('Logout failed', await res.json());
        }
    },

    /** /api/auth/register/invite/<role>/<token> */
    async registerWithToken<R extends 'worker' | 'broker'>(
        role: R,
        token: string,
        data: RegisterInput<R>,
    ): Promise<RegisterOutput<R>> {
        const res = await fetchJson<RegisterOutput<R>>(makeInvite(role, token), {
            method: 'POST',
            body: JSON.stringify(data),
        });
        UserStorage.set(res);
        return res;
    },
};
