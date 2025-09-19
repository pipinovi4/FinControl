export default function ClientRow({
                                      row,
                                      onOpen,
                                      onCreateCredit,
                                      onDelete,
                                      onRestore,
                                  }: {
    row: any;
    onOpen?: () => void;
    onCreateCredit: () => void;
    onDelete?: () => void;
    onRestore?: () => void;
}) {
    const isDeleted = !!row.is_deleted;

    return (
        <tr
            className="cursor-pointer border-b border-[#F0F3FA] hover:bg-[#F6F8FD] transition"
            onClick={onOpen}
        >
            <td className="py-2 pl-3">{row.full_name}</td>
            <td className="py-2 pl-3">{row.phone_number}</td>
            <td className="py-2 pl-3">{row.email}</td>
            <td className="py-2 pl-3">{row.fact_address ?? "—"}</td>

            {/* actions – не відкриваємо модалку по кліку на кнопки */}
            <td
                className="py-2 pl-3 pr-3 text-right"
                onClick={(e) => e.stopPropagation()}
            >
                <div className="flex items-center justify-end gap-2">
                    {!isDeleted && (
                        <button
                            onClick={onCreateCredit}
                            className="cursor-pointer rounded-lg bg-[#7144ff] px-3 py-1.5 text-xs font-semibold text-white hover:brightness-110"
                        >
                            Создать кредит
                        </button>
                    )}
                    {onDelete && !isDeleted && (
                        <button
                            className="cursor-pointer rounded-lg border border-rose-200 bg-rose-50 px-2 py-1 text-xs text-rose-700 hover:bg-rose-100"
                            onClick={onDelete}
                            title="Мягкое удаление клиента"
                        >
                            Удалить
                        </button>
                    )}
                    {onRestore && isDeleted && (
                        <button
                            className="cursor-pointer rounded-lg border border-emerald-200 bg-emerald-50 px-2 py-1 text-xs text-emerald-700 hover:bg-emerald-100"
                            onClick={onRestore}
                            title="Восстановить клиента"
                        >
                            Восстановить
                        </button>
                    )}
                </div>
            </td>
        </tr>
    );
}
