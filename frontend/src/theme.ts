import { createTheme } from '@mantine/core';

export const appTheme = createTheme({
  primaryColor: 'cyan',
  fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif',
  defaultRadius: 'md',
  headings: {
    fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif',
    fontWeight: '700',
  },
  colors: {
    slate: [
      '#eef5fb',
      '#d8e4f0',
      '#b0c6d6',
      '#88a9bf',
      '#658ea9',
      '#507a95',
      '#41617a',
      '#334b5f',
      '#263646',
      '#15202d',
    ],
  },
});
