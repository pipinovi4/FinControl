import { formatMoney } from "@/app/dashboard/components/UserTable/types";
import clsx from "clsx";

const statusLabel: Record<string, string> = {
    new: "Новая",
    treatment: "На доработку",
    approved: "Согласовано",
    completed: "Выдано",
};

export default function CreditRow({
                                      row,
                                      onOpen,
                                      onDelete,
                                      onRestore,
                                  }: {
    row: any;
    onOpen: () => void;
    onDelete: () => void;
    onRestore: () => void;
}) {
    const isDeleted = !!row.is_deleted;

    return (
        <tr
            className="cursor-pointer border-b border-[#F0F3FA] hover:bg-[#F6F8FD] transition px-3 py-4"
            onClick={onOpen}
        >
            <td className="py-2 pl-3 whitespace-nowrap">
                {new Date(row.issued_at).toLocaleDateString("ru-RU")}
            </td>
            <td className="py-2 pl-3 font-mono text-xs">
                {String(row.client_id).slice(0, 8)}…
            </td>
            <td className="py-2 pl-3">{formatMoney(row.amount)}</td>
            <td className="py-2 pl-3">{formatMoney(row.approved_amount)}</td>
            <td className="py-2 pl-3">
        <span
            className={clsx(
                "rounded-full border px-2 py-0.5 text-xs",
                row.status === "new" && "border-blue-200 bg-blue-50 text-blue-700",
                row.status === "needs_fix" &&
                "border-amber-200 bg-amber-50 text-amber-700",
                row.status === "approved" &&
                "border-emerald-200 bg-emerald-50 text-emerald-700",
                row.status === "completed" &&
                "border-slate-300 bg-slate-100 text-slate-700"
            )}
        >
          {statusLabel[row.status] ?? row.status}
        </span>
            </td>

            {/* actions – клік по кнопках не відкриває модалку */}
            <td
                className="py-2 pl-3 pr-3 text-right"
                onClick={(e) => e.stopPropagation()}
            >
                {isDeleted ? (
                    <button
                        className="cursor-pointer rounded-lg border border-emerald-200 bg-emerald-50 px-2 py-1 text-xs text-emerald-700 hover:bg-emerald-100"
                        onClick={onRestore}
                        title="Восстановить кредит"
                    >
                        Восстановить
                    </button>
                ) : (
                    <button
                        className="cursor-pointer rounded-lg border border-rose-200 bg-rose-50 px-2 py-1 text-xs text-rose-700 hover:bg-rose-100"
                        onClick={onDelete}
                        title="Мягкое удаление"
                    >
                        Удалить
                    </button>
                )}
            </td>
        </tr>
    );
}
