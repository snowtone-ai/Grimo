# Verified repository experience

- React Strict Mode can cancel an asynchronous Pixi mount after initialization begins. Publish the QA/runtime handle only for the surviving mount and explicitly destroy the cancelled application; this was reproduced as a stale destroyed handle and verified across 254 route remount cycles.
- Synthetic `pointerdown` used for browser QA may not own an active native pointer, so `setPointerCapture` can throw even when optional chaining is used. Treat capture as best-effort and keep `pointercancel` cleanup independently testable.
- On the Pixel 7a-like DPR 2.625 profile, the configured renderer cap produced a 2× backing buffer (368×364 CSS → 736×728 pixels) without visible source-scaling blur in the Gate 1 capture.
