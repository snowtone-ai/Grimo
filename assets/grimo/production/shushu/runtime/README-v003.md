# Shushu v004 / v003 candidate runtime

PlayCanvas 2.22.2. Separate candidate; Human appearance PENDING. See [review](../../../../../docs/production/shushu/evidence/production-rig-v004-motion-ready/final-v003/REVIEW.md). No original replacement or Motion production is authorized by this package.

```js
import {loadShushuCandidate} from './shushu-v004-loader-v003.mjs';
const shushu = await loadShushuCandidate({pc, app, url: candidateGlbUrl});
// Caller owns body/face animation and supplies its matching current Seat.
shushu.pawControls.set({Seat: 0, 'Hold.L': .6, 'SelfContact.R': 1, 'Wrist.R': .2});
// Later: return Paw ownership to the caller's baked animation.
shushu.pawControls.set(null);
// When removing this instance (safe to call twice):
shushu.dispose();
```

The final GLB SHA256 is `11dc599c13d14db8c6ddd68068059738cf4ec6ac81c7ff706530eff65578c892`. Its clip is a **diagnostic proof**, not a production motion library. The loader performs one fetch and owns an independent container parse, entity, cloned mesh/material buffers and listeners. Releasing one instance must not unload a peer. The supplied `pc` namespace and `app` come from the host application.

Paws retain their approved Basis, UV and texture, but use a single Spine2 carrier and 438 ordinary shape targets each. Hold > SelfContact > Offer arbitration is independent on either side; Wrist is independent, including at zero reach. Body/face pose and Seat are caller-owned. Legacy direct arm FK clips do not drive these rebuilt Paws. Blending baked endpoint clips alone omits the intermediate volume correction; supply current purposes to the controller for blended input and interruptions.

The controller reapplies weights on Application `update`, after Engine `animationUpdate`. `set(values)` also applies immediately. `{defer:true}` only queues input for that update; use it from an earlier input/system phase. Hold anchors follow the evaluated surface plus the existing canonical-forward .031H fixture offset. The deformation module supports full-eight Torso skinning and current-surface Paw NORMAL streams. No Blender callbacks, QA globals, DOM, camera or proof frame numbers are used by either module.

The default uses CPU Paw normal updates and the owned GPU shader path. `normalsEnabled:false` is a diagnostic opt-out; equivalent appearance is not guaranteed. Fixed validated motion witnesses, lifecycle correspondence and a 300-second Xiaomi run are recorded in the review. Untested arbitrary control combinations, legacy FK, item geometry and mobile-network download time remain outside the demonstrated scope. rAF measurements are not GPU timings.
