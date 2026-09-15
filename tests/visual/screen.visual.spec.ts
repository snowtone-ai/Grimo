import { expect, test } from '@playwright/test';

const routes = ['/', '/tasks', '/calendar', '/grimo', '/settings'] as const;
const visualBaselinesReady = process.env.VISUAL_BASELINES_READY === '1';

test.describe('Grimo mobile screen foundation', () => {
  test('current screen routes load without a failed response', async ({ page }) => {
    for (const route of routes) {
      const response = await page.goto(route, { waitUntil: 'domcontentloaded' });
      expect(response, `${route} should return a response`).not.toBeNull();
      expect(response?.status(), `${route} should not return an HTTP error`).toBeLessThan(400);
    }
  });

  test('screen baselines match when explicitly enabled', async ({ page }, testInfo) => {
    test.skip(
      !visualBaselinesReady,
      'Baselines are intentionally opt-in until the corresponding product screens stabilize.',
    );

    for (const route of routes) {
      await page.goto(route, { waitUntil: 'networkidle' });
      const routeName = route === '/' ? 'home' : route.slice(1);
      await expect(page).toHaveScreenshot(`${routeName}-${testInfo.project.name}.png`, {
        fullPage: true,
        animations: 'disabled',
        caret: 'hide',
        scale: 'css',
      });
    }
  });
});
