import React from 'react';
import { RefreshCw, MoreHorizontal, ChevronDown, ChevronUp } from 'lucide-react';

type Props = {
    title: string;
    labels: string[];
    roleIndex: number;
    onChangeRole: (i:number)=>void;
    onReload: () => void;
    loading: boolean;
};

const CardHeader: React.FC<Props> = ({
                                         title, labels, roleIndex,
                                         onChangeRole, onReload, loading
                                     }) => {
    const activeLabel = labels[roleIndex] ?? 'Список';
    return (
        <div className="flex justify-between items-start mb-4 relative z-10">
            <div className="flex flex-col gap-1">
                <h2 className="text-lg font-extrabold text-[#2B3674] tracking-tight">
                    {title}: {activeLabel}
                </h2>

                {labels.length > 1 && (
                    <div className="relative w-40">
                        {/* native select */}
                        <select
                            value={roleIndex}                              // активний індекс
                            onChange={e => onChangeRole(Number(e.target.value))}
                            className="
        mt-1 w-full pr-9 pl-3 py-2
        rounded-lg bg-[#F4F7FE] hover:bg-[#EEF3FF]
        text-[13px] font-medium text-[#2B3674]
        border border-transparent focus:border-[#7144ff]
        outline-none appearance-none transition
      "
                        >
                            {labels.map((label, idx) => (
                                <option key={label} value={idx}>
                                    {label}
                                </option>
                            ))}
                        </select>

                        {/* декоративна стрілочка */}
                        <ChevronDown
                            size={14}
                            className="
        pointer-events-none
        absolute right-3 top-1/2 -translate-y-1/2
        text-[#2B3674]
      "
                        />
                    </div>
                )}
            </div>

            <div className="flex items-center gap-2">
                <button
                    onClick={onReload}
                    title="Обновить"
                    className="cursor-pointer p-2 rounded-lg text-[#7144ff] hover:bg-[#F4F7FE] transition"
                >
                    <RefreshCw size={18} className={loading ? 'animate-spin' : ''} />
                </button>
            </div>
        </div>
    );
};

export default CardHeader;
