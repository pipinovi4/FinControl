import { SVGProps } from "react";

const CompletedIcon = (props: SVGProps<SVGSVGElement>) => {
    return (
        <svg viewBox="0 0 57 56" fill="none" {...props}>
            <circle cx="28.2046" cy="28" r="28" fill="url(#paint0_linear_201_1824)" />
            <g clipPath="url(#clip0_201_1824)">
                <path
                    d="M39.8709 20.0434L26.5593 33.3667L21.6126 28.42L23.2576 26.775L26.5593 30.0767L38.2259 18.41L39.8709 20.0434ZM28.2043 37.3334C23.0593 37.3334 18.8709 33.145 18.8709 28C18.8709 22.855 23.0593 18.6667 28.2043 18.6667C30.0359 18.6667 31.7509 19.2034 33.1976 20.125L34.8893 18.4334C32.9876 17.115 30.6893 16.3334 28.2043 16.3334C21.7643 16.3334 16.5376 21.56 16.5376 28C16.5376 34.44 21.7643 39.6667 28.2043 39.6667C30.2226 39.6667 32.1243 39.1534 33.7809 38.2434L32.0309 36.4934C30.8643 37.03 29.5693 37.3334 28.2043 37.3334ZM36.3709 31.5H32.8709V33.8334H36.3709V37.3334H38.7043V33.8334H42.2043V31.5H38.7043V28H36.3709V31.5Z"
                    fill="white"
                />
            </g>
            <defs>
                <linearGradient id="paint0_linear_201_1824" x1="0.20459" y1="28" x2="56.2046" y2="28" gradientUnits="userSpaceOnUse">
                    <stop stopColor="#4481EB" />
                    <stop offset="1" stopColor="#04BEFE" />
                </linearGradient>
                <clipPath id="clip0_201_1824">
                    <rect width="28" height="28" fill="white" transform="translate(14.2046 14)" />
                </clipPath>
            </defs>
        </svg>
    );
};

export default CompletedIcon;
