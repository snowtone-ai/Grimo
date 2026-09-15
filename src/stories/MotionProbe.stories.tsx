import type { Meta, StoryObj } from '@storybook/nextjs-vite';

import { MotionProbe } from './MotionProbe';

const meta = {
  title: 'Toolchain/Motion Probe',
  component: MotionProbe,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs', 'test'],
} satisfies Meta<typeof MotionProbe>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};
