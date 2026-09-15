import path from 'node:path';

import { defineConfig } from 'vitest/config';

import { storybookTest } from '@storybook/addon-vitest/vitest-plugin';

import { playwright } from '@vitest/browser-playwright';

const dirname = import.meta.dirname;

// More info at: https://storybook.js.org/docs/next/writing-tests/integrations/vitest-addon
export default defineConfig({
  test: {
    projects: [
      {
        extends: true,
        plugins: [
          {
            // Storybook's Vitest transform compares a file URL with Vitest's
            // Windows path. Normalize the guard so stories execute in browser mode.
            name: 'grimo-vitest-windows-story-guard',
            enforce: 'post',
            transform(code, id) {
              if (!id.includes('.stories.')) return;

              const normalized = code.replace(
                /const (\w+) = convertToFilePath\(import\.meta\.url\)\.includes\(globalThis\.__vitest_worker__\.filepath \?\? _expect\.getState\(\)\.testPath\);/,
                'const $1 = true;',
              );

              return normalized === code ? undefined : normalized;
            },
          },
          // The plugin will run tests for the stories defined in your Storybook config
          // See options at: https://storybook.js.org/docs/next/writing-tests/integrations/vitest-addon#storybooktest
          storybookTest({
            configDir: path.join(dirname, '.storybook'),
            storybookScript: 'pnpm.cmd storybook -- --no-open',
            storybookUrl: 'http://127.0.0.1:6006',
            tags: {
              include: ['test'],
            },
          }),
        ],
        test: {
          name: 'storybook',
          browser: {
            enabled: true,
            headless: true,
            provider: playwright({}),
            instances: [{ browser: 'chromium' }],
          },
        },
      },
    ],
  },
});
