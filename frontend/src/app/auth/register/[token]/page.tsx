// app/auth/register/[token]/page.tsx
import { notFound } from 'next/navigation';
import RegisterPage from '@/components/RegisterPage';

type Params = { token: string };

export default async function Page({ params }: { params: Promise<Params> }) {
    // ✦ 1. чекаємо Promise, тепер помилки не буде
    const { token } = await params;

    // ✦ 2. перевіряємо токен на бекенді
    const res = await fetch(
        `http://localhost:8000/api/auth/register/invite/meta/${token}`,
        { cache: 'no-store' }
    );

    if (!res.ok) return notFound();

    const { role } = await res.json();
    const lower = (role as string).toLowerCase();
    if (lower !== 'worker' && lower !== 'broker') return notFound();

    // ✦ 3. рендеримо форму
    return <RegisterPage role={lower} token={token} />;
}
