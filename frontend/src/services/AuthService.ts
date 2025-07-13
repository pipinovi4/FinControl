import { metaFetch, InputOf, OutputOf } from '@/lib/metaFetch';
import UserStorage from "@/services/UserStorage";

/* ─────────── roles & helpers ─────────── */

type Role = 'admin' | 'worker' | 'broker' | 'client';
const makePath = (action: 'login' | 'register', role: Role) =>
    `/api/auth/${action}/${role}/web`;

/* ─────────── DTO-type helpers ─────────── */

type LoginInput   = InputOf<`/api/auth/login/web`>;
type LoginOutput   = OutputOf<`/api/auth/login/web`>;
type RegisterInput<R extends Role> = InputOf<`/api/auth/register/${R}/web`>;
type RegisterOutput<R extends Role>= OutputOf<`/api/auth/register/${R}/web`>;
type RefreshOutput                 = OutputOf<'/api/auth/refresh'>;

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
        const res = await fetch('http://localhost:8000/api/session/logout', {
            method: 'POST',
            credentials: 'include',
        });

        if (res.status === 200) {
            localStorage.removeItem('user');
        } else {
            console.error('Logout failed', await res.json());
        }
    }
};
