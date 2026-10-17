// Run with playwright-cli --session <session> run-code --filename <this file>.
// Open the bounded viewer on 8848 or static viewer on 8849 before running.
async (page) => {
    const url = new URL(page.url());
    if (url.hostname !== '127.0.0.1' || !['8848','8849'].includes(url.port)) throw Error('Expected local Jill v006 review');
    await page.reload();
    await page.setViewportSize({width:1560,height:1150});
    await page.getByRole('button',{name:'neutral',exact:true}).waitFor();
    const staticOnly = await page.getByRole('button',{name:'再生 / 停止',exact:true}).isDisabled();
    await page.getByRole('button',{name:'顔 / 全身',exact:true}).click();
    const evidence = 'docs/production/jill/mouth-integration-v006/';
    if (!staticOnly) {
        for (const name of ['neutral','mouth-closed','mouth-small','mouth-large','smile-L','smile-R','open-smile','closed-open-smile','combined','blink-half','blink-full','wings-open','wings-fold','tail']) {
            await page.getByRole('button',{name,exact:true}).click();await page.waitForTimeout(180);
            await page.screenshot({fullPage:true,path:evidence+'runtime-'+name+'.png'});
        }
        await page.getByRole('button',{name:'再生 / 停止',exact:true}).click();await page.waitForTimeout(4500);
        await page.getByRole('button',{name:'再生 / 停止',exact:true}).click();
        await page.getByRole('button',{name:'neutral',exact:true}).click();await page.waitForTimeout(200);
        await page.screenshot({fullPage:true,path:evidence+'runtime-recovery.png'});
    }
    const names = ['Close','Open','Smile L','Smile R'];
    async function input(index, value) {
        await page.getByRole('slider',{name:names[index],exact:true}).evaluate((element,value)=>{element.value=value;element.dispatchEvent(new Event('input',{bubbles:true}));},String(value));
    }
    for (const close of [0,.25,.5,.75,1]) for (const open of [0,.5,1]) {
        for (const [index,value] of [close,open,1,.5].entries()) await input(index,value);
        await page.waitForTimeout(180);await page.evaluate(()=>window.scrollTo(0,0));
        await page.screenshot({fullPage:true,path:evidence+(staticOnly?'static-':'')+'direct-c'+close+'-o'+open+'.png'});
    }
    for (let index=0;index<=20;index++) {
        await input(0,1-index/20);await page.waitForTimeout(65);
        await page.locator('canvas').screenshot({path:'output/playwright/jill-v006-'+(staticOnly?'static':'clip')+'-transition-'+String(index).padStart(2,'0')+'.png'});
    }
    await page.getByRole('button',{name:'neutral',exact:true}).click();await page.waitForTimeout(200);
    await page.getByRole('button',{name:'確認状態を保存',exact:true}).click();
}
