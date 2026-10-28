// Pure mathematical recreation of the scalloped drip edge from reference
export const SL = 2400;

export const CL: [number, number, number][] = [
  [50, 22, 226],
  [175, 12, 150],
  [310, 30, 250],
  [470, 15, 176],
  [600, 26, 244],
  [760, 34, 290],
  [880, 11, 150],
  [968, 20, 268],
  [1440, 30, 286],
  [1545, 13, 164],
  [1660, 22, 232],
  [1840, 36, 250],
  [1985, 12, 146],
  [2110, 24, 240],
  [2270, 28, 222],
];

export const LL = 44;
export const UL = 60;
export const DL = CL.length;

export const FL = CL.map(([e, t], n) => {
  const [r, i] = CL[(n + 1) % DL];
  const a = e + t;
  const o = r - i + (n + 1 === DL ? SL : 0);
  const s = Math.min((o - a) / 2, UL);
  return { xl: a, xr: o, r: s, foot: LL + s };
});

export const PL = CL.map(([e, t, n], r) => {
  const i = Math.max(FL[(r - 1 + DL) % DL].foot, FL[r].foot);
  return { x: e, y: Math.max(n, i + t * 1.5), r: t };
});

const ml = (e: number) => String(Math.round(e * 10) / 10);

function hl(e: number, t: number) {
  const [n, r] = CL[t];
  const i = PL[t].y - r;
  return `L${ml(n - r + e)} ${ml(i)}A${r} ${r} 0 0 0 ${ml(n + r + e)} ${ml(i)}L${ml(n + r + e)} ${ml(FL[t].foot)}`;
}

const gl = (e: number, t: (typeof FL)[0]) => `A${ml(t.r)} ${ml(t.r)} 0 0 1 ${ml(t.xl + t.r + e)} ${LL}`;

const _l = (e: number, t: (typeof FL)[0]) =>
  `L${ml(t.xr - t.r + e)} ${LL}A${ml(t.r)} ${ml(t.r)} 0 0 1 ${ml(t.xr + e)} ${ml(t.foot)}`;

function vl(e: number) {
  const t = FL[DL - 1];
  let n = _l(e - SL, t);
  for (let idx = 0; idx < DL; idx++) {
    n += hl(e, idx) + gl(e, FL[idx]);
    if (idx < DL - 1) n += _l(e, FL[idx]);
  }
  return n;
}

export const DRIP_SVG_PATH: string = (() => {
  const e = 3600;
  const t = FL[DL - 1];
  const n = t.xl + t.r - 2 * SL;
  const r = t.xl + t.r + SL;
  return `M${ml(n)} ${e}L${ml(n)} ${LL}` + vl(-2400) + vl(0) + vl(SL) + `L${ml(r)} ${e}Z`;
})();

