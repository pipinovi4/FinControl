import StoredUserType from "@/types/StoredUser"

class UserStorage {
    get(): StoredUserType | null {
        const raw = localStorage.getItem('user');
        return raw ? JSON.parse(raw) : null;
    }

    set(user: StoredUserType): void {
        localStorage.setItem('user', JSON.stringify(user));
    }

    clear(): void {
        localStorage.removeItem('user');
    }
}

export default new UserStorage();