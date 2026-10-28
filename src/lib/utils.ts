export const clamp = (val: number, min = 0, max = 1): number =>
  Math.min(max, Math.max(min, val));

export const lerp = (start: number, end: number, t: number): number =>
  start + (end - start) * t;

export const norm = (val: number, start: number, end: number): number =>
  clamp((val - start) / (end - start));

export const easeInOutCubic = (x: number): number =>
  x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;

export const prefersReducedMotion = (): boolean =>
  typeof window !== 'undefined' &&
  window.matchMedia('(prefers-reduced-motion: reduce)').matches;

export const padZero = (n: number, len = 2): string =>
  String(n).padStart(len, '0');

