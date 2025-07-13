import { MoreHorizontal } from 'lucide-react';

const users = [
    {
        name: 'Алексей Кузнецов',
        phone: '+7 (916) 123–45–67',
        status: 'В процессе',
        date: '24.Янв.2021',
    },
    {
        name: 'Мария Смирнова',
        phone: '+7 (495) 987–65–43',
        status: 'Закрыта',
        date: '12.Янв.2021',
    },
    {
        name: 'Игорь Сидоров',
        phone: '+7 (926) 404–11–22',
        status: 'Закрыта',
        date: '5.Янв.2021',
    },
    {
        name: 'Екатерина Белова',
        phone: '+7 (812) 300–20–10',
        status: 'В процессе',
        date: '7.Мар.2021',
    },
    {
        name: 'Дмитрий Орлов',
        phone: '+7 (903) 777–88–99',
        status: 'Новый юзер',
        date: '17.Фев.2021',
    },
];

const UsersTable = () => {
    return (
        <div className="w-full h-full bg-white rounded-2xl shadow px-6 py-6">
            <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-extrabold text-[#2B3674] tracking-tight">Таблица юзеров</h2>
                <button className="text-[#A3AED0] hover:text-[#4318FF]">
                    <MoreHorizontal className="w-5 h-5" />
                </button>
            </div>

            <div className="overflow-x-auto">
                <table className="w-full text-base">
                    <thead className="text-[#8F9BBA] text-left border-b font-extrabold tracking-tight">
                    <tr>
                        <th className="py-3">ФИО</th>
                        <th className="py-3">Номер телефона</th>
                        <th className="py-3">Статус</th>
                        <th className="py-3">Дата</th>
                    </tr>
                    </thead>
                    <tbody className="text-[#2B3674] font-bold tracking-tight">
                    {users.map((user, index) => (
                        <tr
                            key={index}
                            className="border-b border-[#F0F3FA] hover:bg-[#F6F8FD] transition"
                        >
                            <td className="py-3 flex items-center gap-2">
                                <input
                                    type="checkbox"
                                    className="accent-[#4318FF] w-4 h-4"
                                />
                                {user.name}
                            </td>
                            <td className="py-3">{user.phone}</td>
                            <td className="py-3">{user.status}</td>
                            <td className="py-3">{user.date}</td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default UsersTable;
