import type { Preview } from '@storybook/nextjs-vite'

const preview: Preview = {
  // Storybook's Vitest integration tests stories carrying the `test` tag.
  tags: ['test'],
  parameters: {
    controls: {
      matchers: {
       color: /(background|color)$/i,
       date: /Date$/i,
      },
    },

    a11y: {
      // Fail the Storybook/Vitest gate on detectable a11y violations.
      // 'off' - skip a11y checks entirely
      test: 'error'
    }
  },
};

export default preview;
