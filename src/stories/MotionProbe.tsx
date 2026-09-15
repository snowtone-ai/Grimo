import { motion, useReducedMotion } from 'motion/react';

export function MotionProbe() {
  const reducedMotion = useReducedMotion();

  return (
    <motion.div
      aria-label="Motion for React preview"
      initial={reducedMotion ? false : { opacity: 0, y: 4 }}
      animate={{ opacity: 1, y: 0 }}
      transition={reducedMotion ? { duration: 0 } : { duration: 0.16, ease: 'easeOut' }}
      style={{
        borderRadius: 16,
        padding: '16px 20px',
        background: 'linear-gradient(135deg, #f7fbfd, #e5f1f8)',
        color: '#40566c',
        boxShadow: '-2px -2px 7px rgba(255,255,255,.66), 2px 4px 8px rgba(76,108,134,.11)',
        fontFamily: 'system-ui, sans-serif',
        fontWeight: 600,
      }}
    >
      Motion for React is ready
    </motion.div>
  );
}
