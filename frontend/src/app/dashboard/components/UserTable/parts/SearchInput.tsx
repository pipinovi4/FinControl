'use client';

import React from 'react';
import { Search } from 'lucide-react';

type Props = {
    value: string;
    onChange: (v: string) => void;
    placeholder?: string;
    className?: string;
};

const SearchInput: React.FC<Props> = ({
                                          value,
                                          onChange,
                                          placeholder = 'Поиск...',
                                          className = '',
                                      }) => {
    return (
        <div className={`relative w-full ${className}`}>
            <Search
                size={16}
                className="absolute left-3 top-1/2 -translate-y-1/2 text-[#8F9BBA]"
            />
            <input
                type="text"
                value={value}
                onChange={e => onChange(e.target.value)}
                placeholder={placeholder}
                className="w-full pl-9 pr-3 py-2 rounded-lg bg-[#F4F7FE] focus:bg-white border border-transparent focus:border-[#7144ff] outline-none text-sm transition"
            />
        </div>
    );
};

export default SearchInput;
