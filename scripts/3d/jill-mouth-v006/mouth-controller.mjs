/** Match the saved Blender mouth drivers when controlling static glTF morphs. */
export function resolveJillMouthWeights(controls = {}) {
    const unit = (name) => {
        const value = controls[name] ?? 0;
        if (typeof value !== 'number' || !Number.isFinite(value)) throw new TypeError(`Invalid Jill mouth control: ${name}`);
        return Math.min(1, Math.max(0, value));
    };
    const close = unit('mouth_close');
    return {
        FACE_MouthClose: close,
        FACE_MouthOpen: unit('mouth_open') * (1 - close),
        'FACE_Smile.L': unit('smile.L') * (1 - close),
        'FACE_Smile.R': unit('smile.R') * (1 - close)
    };
}

/** Bind once per loaded Jill render root. Other morphs and all bones are untouched.
 * The caller must own these four weights: pause a conflicting animation track, or
 * apply the resolved controls after its animation update. No scene globals used.
 */
export function createJillMouthController(entity) {
    const instances = [...new Set(entity.findComponents('render').flatMap(c => c.meshInstances).map(m => m.morphInstance).filter(Boolean))];
    const names = Object.keys(resolveJillMouthWeights());
    if (!instances.length) throw new Error('Jill has no morph instances');
    for (const instance of instances) {
        const available = new Set(instance.morph.targets.map(t => t.name));
        if (names.some(name => !available.has(name))) throw new Error('Jill mouth morph contract is incomplete');
    }
    return {
        set(controls = {}) {
            const weights = resolveJillMouthWeights(controls);
            for (const instance of instances) for (const [name, weight] of Object.entries(weights)) instance.setWeight(name, weight);
            return weights;
        },
        read() {
            return instances.map(instance => Object.fromEntries(names.map(name => [name, instance.getWeight(name)])));
        },
        instanceCount: instances.length
    };
}
