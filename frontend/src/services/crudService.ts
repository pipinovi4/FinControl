import { loadMetaRoutes, metaFetch } from '@/lib/metaFetch';
import { z } from 'zod';

const getRole = (): string => {
    const user = localStorage.getItem('user');
    if (!user) throw new Error('User not found in localStorage');
    const parsed = JSON.parse(user);
    if (!parsed.role) throw new Error('User role missing');
    return parsed.role.toLowerCase();
};

// 🧠 UUID нормалізатор
const normalizePath = (rawPath: string): string =>
    rawPath.replace(
        /[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/gi,
        '{id}'
    );

export const roleBasedCrudService = {
    async get(id?: string) {
        const role = getRole();
        const path = `/api/entities/${role}${id ? `/${id}` : ''}`;
        return metaFetch(path, {}, { credentials: 'include' });
    },

    async create(data: any) {
        const role = getRole();
        return metaFetch(`/api/entities/create/${role}`, data, { credentials: 'include' });
    },

    async update(id: string, data: any) {
        const role = getRole()
        return metaFetch(`/api/entities/update/${role}/${id}`, data, { credentials: 'include' });
    },

    async delete(id: string) {
        const role = getRole();
        const path = `/api/entities/delete/${role}/${id}`;
        return metaFetch(path, { id }, { credentials: 'include' });
    },
};
