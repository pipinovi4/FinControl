import {SVGProps} from "react";

const MoonIcon = (props: SVGProps<SVGSVGElement>) => {
    return (
        <svg width="15" height="18" viewBox="0 0 15 18" fill="currentColor" {...props}>
            <path d="M8.24662 18C10.774 18 13.0823 16.737 14.6115 14.6675C14.8377 14.3613 14.5911 13.9141 14.2414 13.9872C10.266 14.8188 6.6153 11.4709 6.6153 7.06303C6.6153 4.52398 7.85277 2.18914 9.86399 0.931992C10.174 0.738211 10.096 0.221941 9.74377 0.150469C9.24992 0.0504468 8.7488 8.21369e-05 8.24662 0C3.72369 0 0.0527344 4.02578 0.0527344 9C0.0527344 13.9679 3.71793 18 8.24662 18Z" fill="currentColor"/>
        </svg>
    );
};

export default MoonIcon;