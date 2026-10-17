// Capture actual static GLB in the local viewer through its visible controls.
async (page) => {
    const evidence='docs/production/jill/eye-boundary-v008/';
    const settle=async()=>{await page.setViewportSize({width:1561,height:1080});await page.setViewportSize({width:1560,height:1080});await page.waitForTimeout(200);};
    await page.setViewportSize({width:1560,height:1080});
    await page.goto('http://127.0.0.1:8850');await page.getByRole('button',{name:'neutral',exact:true}).waitFor();await settle();
    await page.screenshot({path:evidence+'runtime-before-body.png',fullPage:true});
    await page.getByRole('button',{name:'顔 / 全身',exact:true}).click();await page.waitForTimeout(200);
    await page.screenshot({path:evidence+'runtime-before-face.png',fullPage:true});
    await page.locator('canvas').screenshot({path:evidence+'runtime-before-neutral-canvas.png'});
    await page.goto('http://127.0.0.1:8851');await page.getByRole('slider',{name:'Blink L',exact:true}).waitFor();await settle();
    await page.screenshot({path:evidence+'runtime-body.png',fullPage:true});
    await page.getByRole('button',{name:'顔 / 全身',exact:true}).click();await page.waitForTimeout(200);
    await page.screenshot({path:evidence+'runtime-face.png',fullPage:true});
    await page.locator('canvas').screenshot({path:evidence+'runtime-neutral-canvas.png'});
    const set=async(name,value)=>page.getByRole('slider',{name,exact:true}).evaluate((e,v)=>{e.value=String(v);e.dispatchEvent(new Event('input',{bubbles:true}));},value);
    for(const b of [.25,.5,.75,1]) {
        await set('Blink L',b);await set('Blink R',b);await page.waitForTimeout(100);
        await page.screenshot({path:evidence+`runtime-blink-${b}.png`,fullPage:true});
    }
    for(const [label,l,r]of [['wink-L',1,0],['wink-R',0,1]]) {
        await set('Blink L',l);await set('Blink R',r);await page.waitForTimeout(100);await page.screenshot({path:evidence+`runtime-${label}.png`,fullPage:true});
    }
    await page.getByRole('button',{name:'neutral',exact:true}).click();
    for(const [label,values]of [['mouth-closed',[1,1,1,1]],['mouth-small',[.5,0,0,0]],['mouth-large',[0,1,0,0]],['combined',[0,.5,1,.5]]]) {
        for(const [i,v]of values.entries())await set(['Close','Open','Smile L','Smile R'][i],v);
        if(label==='combined'){await set('Blink L',.5);await set('Blink R',.5);}
        await page.waitForTimeout(120);await page.screenshot({path:evidence+`runtime-${label}.png`,fullPage:true});
    }
    await page.getByRole('button',{name:'neutral',exact:true}).click();
    for(let i=0;i<=20;i++) {
        const b=1-Math.abs(10-i)/10;await set('Blink L',b);await set('Blink R',b);await page.waitForTimeout(65);
        await page.locator('canvas').screenshot({path:evidence+`runtime-sweep-${String(i).padStart(2,'0')}.png`});
    }
    await page.getByRole('button',{name:'neutral',exact:true}).click();await page.waitForTimeout(200);
    await page.screenshot({path:evidence+'runtime-recovery.png',fullPage:true});
    await page.locator('canvas').screenshot({path:evidence+'runtime-recovery-canvas.png'});
    await page.getByRole('button',{name:'確認状態を保存',exact:true}).click();
}
