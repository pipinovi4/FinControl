import React from 'react';

type Props = {
    skip: number;
    pageSize: number;
    total: number;
    onOpenModal: () => void;
};

const CardFooter: React.FC<Props> = ({ skip, pageSize, total, onOpenModal }) => {
    return (
        <div className="mt-4 flex justify-between items-center text-[12px] text-[#8F9BBA]">
            <div>
                Страница:{' '}
                <span className="font-semibold text-[#2B3674]">
          {Math.floor(skip / pageSize) + 1}
        </span>
                {total > 0 && (
                    <>
                        {' '}| Всего:{' '}
                        <span className="font-semibold text-[#2B3674]">{total}</span>
                    </>
                )}
            </div>
            <button
                onClick={onOpenModal}
                className="cursor-pointer px-4 py-1.5 rounded-lg bg-[#7144ff] text-white text-xs font-medium hover:opacity-90 transition"
            >
                Расширенный поиск
            </button>
        </div>
    );
};

export default CardFooter;
