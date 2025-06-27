import { SVGProps } from "react";

const LoopIcon = (props: SVGProps<SVGSVGElement>) => {
    return (
        <svg width="12" height="12" viewBox="0 0 12 12" fill="none" {...props}>
            <circle cx="5.08154" cy="5" r="4.3" stroke="currentColor" strokeWidth="1.4" />
            <line x1="10.0916" y1="11" x2="8.08154" y2="8.98995" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
        </svg>
    );
};

export default LoopIcon;
