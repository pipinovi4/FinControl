/* FullscreenModal.tsx */
'use client';

import { createPortal } from 'react-dom';
import { AnimatePresence, motion } from 'framer-motion';

type Props = {
    modalOpen: boolean;
    toggleModal: () => void;
    children: React.ReactNode;
};

export default function FullscreenModal({
                                            modalOpen, toggleModal, children,
                                        }: Props) {
    /* portal завжди у DOM; AnimatePresence керує монтуванням/демонтуванням */
    return createPortal(
        <AnimatePresence>
            {modalOpen && (
                <motion.div
                    key="overlay"
                    /* overlay fade */
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: .25 }}
                    className="fixed inset-0 z-50 flex items-center justify-center
                     bg-black/40 backdrop-blur-sm"
                    onClick={toggleModal}
                >
                    <motion.div
                        key="dialog"
                        /* невеликий zoom + fade для самого вмісту */
                        initial={{ scale: .92, opacity: 0 }}
                        animate={{ scale: 1,   opacity: 1 }}
                        exit={{ scale: .92, opacity: 0 }}
                        transition={{ duration: .25 }}
                        onClick={e => e.stopPropagation()}
                    >
                        {children}
                    </motion.div>
                </motion.div>
            )}
        </AnimatePresence>,
        document.body,
    );
}
