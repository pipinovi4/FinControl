import React from "react";

const StatCard = ({ icon, label, value }: { icon: React.ReactElement<React.SVGProps<SVGSVGElement>>, label: string, value: string }) => (
    <div className="bg-white rounded-2xl shadow flex items-center gap-4 px-6 py-5">
        <div className="w-12 h-12 rounded-full flex items-center justify-center bg-[#F4F7FE]">
            {icon}
        </div>
        <div>
            <p className="text-sm text-[#8F9BBA] font-medium">{label}</p>
            <p className="text-xl font-bold text-[#2B3674]">{value}</p>
        </div>
    </div>
);

export default StatCard;