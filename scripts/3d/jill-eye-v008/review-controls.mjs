/** Optional local eye QA; direct Morph weights after actual rendered frames. */
export function installEyeReview({app,entity,onManual}) {
    const instances=[...new Set(entity.findComponents('render').flatMap(c=>c.meshInstances).map(m=>m.morphInstance).filter(Boolean))];
    const names=['FACE_Blink.L','FACE_Blink.R'];
    if(!instances.length||instances.some(i=>names.some(n=>!i.morph.targets.some(t=>t.name===n))))throw Error('Missing Jill blink Morphs');
    const panel=document.createElement('fieldset'),legend=document.createElement('legend');legend.textContent='瞬きの中間・左右別入力';panel.append(legend);
    const inputs=new Map(),samples=[];let active=false,previous='';
    const controls=()=>Object.fromEntries([...inputs].map(([name,input])=>[name,Number(input.value)]));
    for(const [index,name] of names.entries()) {
        const label=document.createElement('label');label.textContent=index?'Blink R':'Blink L';const input=document.createElement('input');input.type='range';input.min=0;input.max=1;input.step=.01;input.value=0;input.setAttribute('aria-label',label.textContent);
        input.addEventListener('input',()=>{active=true;onManual();for(const instance of instances)for(const [n,v]of Object.entries(controls()))instance.setWeight(n,v);});label.append(input);panel.append(label);inputs.set(name,input);
    }
    document.querySelector('#cases').after(panel);
    app.on('frameend',()=>{if(!active)return;const row={controls:controls(),instances:instances.map(i=>Object.fromEntries(names.map(n=>[n,i.getWeight(n)])))};const key=JSON.stringify(row);if(key!==previous){previous=key;samples.push(row);}});
    return {stop(){active=false;for(const i of instances)for(const n of names)i.setWeight(n,0);for(const input of inputs.values())input.value=0;},report(){return {instanceCount:instances.length,samples};}};
}
