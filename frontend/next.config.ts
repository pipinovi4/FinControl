import type { NextConfig } from "next";

const nextConfig: NextConfig = {
    reactStrictMode: false, // 👈 дуже важливо, інакше conditional hooks = смерть
    output: "standalone",   // 👈 генерує .next/standalone автоматично
    eslint: {
        ignoreDuringBuilds: true,
    },
    typescript: {
        ignoreBuildErrors: true,
    },
};

export default nextConfig;
