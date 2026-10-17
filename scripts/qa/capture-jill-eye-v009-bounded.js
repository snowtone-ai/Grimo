async (page) => {
    const E='docs/production/jill/eye-join-v009/';await page.goto('http://127.0.0.1:8854');
    await page.getByRole('button',{name:'combined',exact:true}).waitFor();await page.setViewportSize({width:1560,height:1080});
    for(const name of ['neutral','mouth-closed','mouth-small','mouth-large','blink-half','blink-full','wings-open','wings-fold','tail','combined']) {
        await page.getByRole('button',{name,exact:true}).click();await page.waitForTimeout(150);await page.screenshot({path:E+`bounded-${name}.png`,fullPage:true});
    }
    await page.getByRole('button',{name:'neutral',exact:true}).click();await page.getByRole('button',{name:'再生 / 停止',exact:true}).click();await page.waitForTimeout(4500);await page.getByRole('button',{name:'再生 / 停止',exact:true}).click();
    await page.getByRole('button',{name:'neutral',exact:true}).click();await page.waitForTimeout(150);await page.screenshot({path:E+'bounded-recovery.png',fullPage:true});await page.getByRole('button',{name:'確認状態を保存',exact:true}).click();
}
