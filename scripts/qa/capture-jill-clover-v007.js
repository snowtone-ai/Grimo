// Actual static GLB, front/left-side/left3Q; mouth controller regression.
async (page) => {
    if (new URL(page.url()).origin !== 'http://127.0.0.1:8850') throw Error('Expected local v007 viewer');
    await page.setViewportSize({width:1560,height:1080});
    await page.getByRole('button',{name:'neutral',exact:true}).waitFor();
    const evidence='docs/production/jill/clover-v007/';
    await page.screenshot({path:evidence+'runtime-body.png',fullPage:true});
    const names=['Close','Open','Smile L','Smile R'];
    for (const [label,values] of [['closed',[1,1,1,1]],['small',[.5,0,0,0]],['large',[0,1,0,0]],['smile',[0,.5,1,.5]]]) {
        for (const [i,value] of values.entries()) await page.getByRole('slider',{name:names[i],exact:true}).evaluate((e,v)=>{e.value=String(v);e.dispatchEvent(new Event('input',{bubbles:true}));},value);
        await page.waitForTimeout(150);await page.screenshot({path:evidence+'runtime-'+label+'.png',fullPage:true});
    }
    await page.getByRole('button',{name:'neutral',exact:true}).click();await page.waitForTimeout(200);
    await page.screenshot({path:evidence+'runtime-recovery.png',fullPage:true});
    await page.getByRole('button',{name:'顔 / 全身',exact:true}).click();await page.waitForTimeout(150);
    await page.screenshot({path:evidence+'runtime-face.png',fullPage:true});
    await page.getByRole('button',{name:'確認状態を保存',exact:true}).click();
}
