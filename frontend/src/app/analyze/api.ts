export const API = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

export async function fetchJSON<T>(url: string, init?: RequestInit): Promise<T> {
    const res = await fetch(url, {
        credentials: 'include',
        headers: { 'Content-Type': 'application/json', ...(init?.headers || {}) },
        ...init,
    });
    if (!res.ok) {
        let msg = `HTTP ${res.status}`;
        try {
            const j = await res.json();
            msg = j?.detail ?? msg;
        } catch {}
        throw new Error(msg);
    }
    return res.json() as Promise<T>;
}

/* detail */
export const detailClient = (id: string) => `${API}/api/dashboard/admin/client/${id}`;
export const detailBroker = (id: string) => `${API}/api/dashboard/admin/broker/${id}`;
export const detailWorker = (id: string) => `${API}/api/dashboard/admin/worker/${id}`;

/* broker self-attach/detach */
export async function brokerSignClient(clientId: string, brokerId: string) {
    const url = new URL(`${API}/api/dashboard/admin/client/${clientId}/assign-broker`);
    url.searchParams.set('broker_id', brokerId);
    return fetchJSON<{ status: string; broker_id: string }>(url.toString(), { method: 'PATCH' });
}
export async function brokerUnsignClient(clientId: string) {
    const url = new URL(`${API}/api/dashboard/admin/client/${clientId}/assign-broker`);
    return fetchJSON<{ status: string }>(url.toString(), { method: 'PATCH' });
}

/* reassign by EMAIL */
export async function adminAssignWorkerByEmail(clientId: string, workerEmail: string | null) {
    const url = new URL(`${API}/api/dashboard/admin/client/${clientId}/assign-worker-by-email`);
    if (workerEmail) url.searchParams.set('worker_email', workerEmail);
    return fetchJSON<{ status: string }>(url.toString(), { method: 'PATCH' });
}
export async function adminAssignBrokerByEmail(clientId: string, brokerEmail: string | null) {
    const url = new URL(`${API}/api/dashboard/admin/client/${clientId}/assign-broker-by-email`);
    if (brokerEmail) url.searchParams.set('broker_email', brokerEmail);
    return fetchJSON<{ status: string }>(url.toString(), { method: 'PATCH' });
}

/* edit entities */
export async function adminEditClient(clientId: string, fields: Record<string, any>) {
    return fetchJSON<{ status: string }>(`${API}/api/dashboard/admin/client/${clientId}`, { method: 'PATCH', body: JSON.stringify(fields) });
}
export async function adminEditBroker(brokerId: string, fields: Record<string, any>) {
    return fetchJSON<{ status: string }>(`${API}/api/dashboard/admin/broker/${brokerId}`, { method: 'PATCH', body: JSON.stringify(fields) });
}
export async function adminEditWorker(workerId: string, fields: Record<string, any>) {
    return fetchJSON<{ status: string }>(`${API}/api/dashboard/admin/worker/${workerId}`, { method: 'PATCH', body: JSON.stringify(fields) });
}

/* soft delete / restore user */
export async function adminSoftDeleteUser(userId: string) {
    return fetchJSON<{ status: string }>(`${API}/api/dashboard/admin/user/${userId}/deactivate`, { method: 'PATCH' });
}
export async function adminRestoreUser(userId: string) {
    return fetchJSON<{ status: string }>(`${API}/api/dashboard/admin/user/${userId}/restore`, { method: 'PATCH' });
}

/* role helpers */
export type RoleKey = 'worker' | 'broker' | 'admin';
export type EntityKey = 'clients' | 'brokers' | 'workers';

export const getRole = (): RoleKey => {
    try {
        const raw = JSON.parse(localStorage.getItem('user') ?? '{}').role?.toLowerCase();
        return raw === 'admin' || raw === 'broker' || raw === 'worker' ? (raw as RoleKey) : 'broker';
    } catch {
        return 'broker';
    }
};
export const getUserId = (): string | null => {
    try { return JSON.parse(localStorage.getItem('user') ?? 'null')?.id ?? null; }
    catch { return null; }
};
