import { createJillMouthController } from '/mouth-controller.mjs';

/** Optional local QA UI. Reads weights only after an actual rendered frame. */
export function installMouthReview({ app, entity, onManual }) {
    const controller = createJillMouthController(entity);
    const panel = document.createElement('fieldset');Object.assign(panel.style,{display:'flex',flexWrap:'wrap',minWidth:'0',gap:'4px'});
    const legend = document.createElement('legend');legend.textContent = '口の同時入力・中間値を確認';panel.append(legend);
    const inputs = new Map();const samples = [];let active = false;let previous = '';
    const controls = () => Object.fromEntries([...inputs].map(([name, input]) => [name, Number(input.value)]));
    for (const [name, title] of [['mouth_close','Close'],['mouth_open','Open'],['smile.L','Smile L'],['smile.R','Smile R']]) {
        const label = document.createElement('label');label.textContent = title;Object.assign(label.style,{display:'inline-flex',alignItems:'center'});
        const input = document.createElement('input');input.type = 'range';input.min = 0;input.max = 1;input.step = .01;input.value = 0;input.setAttribute('aria-label', title);
        input.addEventListener('input', () => {active = true;onManual();controller.set(controls());});
        label.append(input);panel.append(label);inputs.set(name, input);
    }
    document.querySelector('#cases').after(panel);
    app.on('frameend', () => {
        if (!active) return;
        const row = {controls: controls(), instances: controller.read()};
        const key = JSON.stringify(row);
        if (key !== previous) {previous = key;samples.push(row);}
    });
    return {stop() {active = false;controller.set({});for(const input of inputs.values())input.value=0;},report() {return {instanceCount:controller.instanceCount,samples};}};
}
