'use client';

import { useState, useRef, useEffect } from 'react';
import clsx from 'clsx';
import { ChevronLeft, ChevronRight } from 'lucide-react';

/* ─── helpers ─── */
const ruMonths = [
    'Январь','Февраль','Март','Апрель','Май','Июнь',
    'Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь',
];
const weekdays = ['Пн','Вт','Ср','Чт','Пт','Сб','Вс'];

const getMonthMatrix = (y:number, m:number) => {
    const first = new Date(y, m, 1);
    const start = (first.getDay() + 6) % 7;
    const daysInM = new Date(y, m + 1, 0).getDate();
    const daysPrev = new Date(y, m, 0).getDate();
    const cells:number[] = [];
    for (let i = start; i > 0; i--) cells.push(-(daysPrev - i + 1));
    for (let i = 1; i <= daysInM; i++) cells.push(i);
    while (cells.length % 7) cells.push(-(cells.length % 7));
    return cells;
};

export default function CalendarCard() {
    const today = new Date();
    const [view, setView]   = useState({ y: today.getFullYear(), m: today.getMonth() });
    const [range, setRange] = useState<[Date|null,Date|null]>([null, null]);
    const [openYear, setOpenYear] = useState(false);
    const yearBoxRef = useRef<HTMLDivElement>(null);

    /* ── закриваємо дроп, якщо клік поза ним ── */
    useEffect(() => {
        const handler = (e: MouseEvent) => {
            if (openYear && yearBoxRef.current && !yearBoxRef.current.contains(e.target as Node)) {
                setOpenYear(false);
            }
        };
        window.addEventListener('mousedown', handler);
        return () => window.removeEventListener('mousedown', handler);
    }, [openYear]);

    const selectDate = (d:number) => {
        if (d<=0) return;
        const clicked = new Date(view.y, view.m, d);
        if (!range[0] || range[1]) setRange([clicked, null]);
        else setRange(range[0] < clicked ? [range[0], clicked] : [clicked, range[0]]);
    };

    const same = (a:Date,b:Date) => a.getFullYear()===b.getFullYear()&&a.getMonth()===b.getMonth()&&a.getDate()===b.getDate();
    const isStart = (d:number)=>range[0]&&same(new Date(view.y,view.m,d),range[0]);
    const isEnd   = (d:number)=>range[1]&&same(new Date(view.y,view.m,d),range[1]);
    const inRange = (d:number)=>{
        if(d<=0||!range[0]||!range[1]) return false;
        const t=new Date(view.y,view.m,d).getTime();
        return t>range[0].getTime()&&t<range[1].getTime();
    };

    const cells = getMonthMatrix(view.y, view.m);

    const years = Array.from({length:21},(_,i)=>view.y-10+i);

    return (
        <div className="w-full h-full rounded-[24px] p-6 bg-white shadow-md flex flex-col font-[var(--font-dm-sans)] text-[#1C2141]">
            {/* header */}
            <div className="flex items-center gap-2 font-bold mb-4 relative z-10">
                <button onClick={()=>setView(v=>({m:v.m? v.m-1:11,y:v.m? v.y:v.y-1}))}>
                    <ChevronLeft className="w-5 h-5 text-[#4B22F4]" />
                </button>

                <span className="bg-[#F3F3FF] text-[#4B22F4] rounded-[20px] px-3 py-1">{ruMonths[view.m]}</span>

                <ChevronRight className="w-4 h-4 text-[#8F9BBA]" />

                {/* selector року */}
                <div ref={yearBoxRef} className="relative">
                    <button onClick={()=>setOpenYear(o=>!o)} className="text-[#8F9BBA] font-medium">{view.y}</button>

                    {openYear && (
                        <div
                            className="absolute left-1/2 -translate-x-1/2 mt-2 bg-white border border-[#E0E0E0] rounded-xl shadow-lg
                         max-h-44 w-24 overflow-y-auto scrollbar-thin scrollbar-thumb-[#D4D7E5] scrollbar-track-transparent z-50">
                            {years.map(y=>(
                                <div
                                    key={y}
                                    onClick={()=>{setView(v=>({...v,y}));setOpenYear(false);}}
                                    className={clsx(
                                        "px-4 py-2 text-sm cursor-pointer select-none",
                                        y===view.y ? "bg-[#F3F3FF] text-[#4B22F4] font-semibold" : "hover:bg-[#F3F3FF]"
                                    )}
                                >{y}</div>
                            ))}
                        </div>
                    )}
                </div>
            </div>

            {/* weekdays */}
            <div className="grid grid-cols-7 text-center text-sm font-medium mb-2">
                {weekdays.map(d=><span key={d}>{d}</span>)}
            </div>

            {/* days */}
            <div className="grid grid-cols-7 gap-y-2 flex-1 text-center">
                {cells.map((d,i)=>{
                    const off=d<=0;
                    const inside=inRange(d); const st=isStart(d); const ed=isEnd(d);
                    return (
                        <div key={i} className="relative flex justify-center">
                            {(inside||st||ed)&&(
                                <div className={clsx("absolute h-9 w-full z-0",
                                    inside && "bg-[#F3F3FF]",
                                    st&&!ed && "bg-[#F3F3FF] rounded-l-full",
                                    ed&&!st && "bg-[#F3F3FF] rounded-r-full"
                                )}/>
                            )}
                            <button
                                disabled={off}
                                onClick={()=>selectDate(d)}
                                className={clsx("w-9 h-9 z-10 rounded-full flex items-center justify-center text-sm transition",
                                    off && "text-[#D1D4E0]",
                                    (st||ed) && "bg-[#4B22F4] text-white shadow-md",
                                    inside && !st && !ed && "text-[#4B22F4]",
                                    !inside && !st && !ed && !off && "hover:bg-[#F0F1F9]"
                                )}
                            >
                                {d>0&&d}
                            </button>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
