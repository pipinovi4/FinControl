// src/parts/ui/SplashLoader.tsx
'use client';

import { motion, AnimatePresence } from 'framer-motion';

export default function SplashLoader() {
    return (
        <AnimatePresence>
            <motion.div
                key="splash"
                className="fixed inset-0 z-[9999] flex items-center justify-center bg-gradient-to-br from-[#F8FAFF] to-[#EEF2FF]"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
            >
                {/* ─────────── Логотип ─────────── */}
                <motion.div
                    className="
            relative flex items-center justify-center
            rounded-3xl bg-white shadow-2xl
            h-20 w-20
            sm:h-24 sm:w-24
            lg:h-28 lg:w-28
            xl:h-32 xl:w-32
          "
                    initial={{ scale: 0.7 }}
                    animate={{ scale: 1 }}
                    transition={{ type: 'spring', stiffness: 260, damping: 20 }}
                >
          <span
              className="
              font-black text-[#4B22F4]
              text-3xl
              sm:text-4xl
              lg:text-5xl
            "
          >
            F
          </span>

                    <motion.span
                        className="absolute inset-0 rounded-3xl border-4 border-[#4B22F4]/30"
                        animate={{ scale: [1, 1.15, 1], opacity: [1, 0.3, 1] }}
                        transition={{ duration: 2, ease: 'easeInOut', repeat: Infinity }}
                    />
                </motion.div>

                {/* ─────────── Прогрес-бар ─────────── */}
                <motion.div
                    className="
            absolute bottom-10
            h-1.5
            w-[70%]              /* < 600 px  →  ~30 % коротший */
            max-w-xs
            sm:bottom-12
            sm:w-3/4             /* ≥ 640 px  →  повертаємось до 75 % */
            sm:max-w-sm
            overflow-hidden rounded-full bg-[#E0E7FF]
          "
                    initial={{ width: 0 }}
                    animate={{ width: '100%' }}
                    transition={{ duration: 0.3, delay: 0.4 }}
                >
                    <motion.span
                        className="block h-full w-full origin-left rounded-full bg-gradient-to-r from-[#4B22F4] via-[#6752FF] to-[#9C7CFF]"
                        animate={{ scaleX: [0, 1, 1, 0] }}
                        transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
                    />
                </motion.div>
            </motion.div>
        </AnimatePresence>
    );
}
