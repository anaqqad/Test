// Exact Euclidean distance transform (Felzenszwalb & Huttenlocher), used to turn territory masks into
// signed distance fields. Interpolating two SDFs and thresholding at 0 morphs one border into the next,
// which handles pockets, enclaves and islands that polygon morphing cannot.

const INF = 1e20;

function edt1d(f: Float64Array, n: number, d: Float64Array, v: Int32Array, z: Float64Array) {
  let k = 0;
  v[0] = 0;
  z[0] = -INF;
  z[1] = INF;
  for (let q = 1; q < n; q++) {
    let s = (f[q] + q * q - (f[v[k]] + v[k] * v[k])) / (2 * q - 2 * v[k]);
    while (s <= z[k]) {
      k--;
      s = (f[q] + q * q - (f[v[k]] + v[k] * v[k])) / (2 * q - 2 * v[k]);
    }
    k++;
    v[k] = q;
    z[k] = s;
    z[k + 1] = INF;
  }
  k = 0;
  for (let q = 0; q < n; q++) {
    while (z[k + 1] < q) k++;
    d[q] = (q - v[k]) * (q - v[k]) + f[v[k]];
  }
}

// Squared distance from every pixel to the nearest pixel where `seed` is true.
function edt2d(seed: (i: number) => boolean, w: number, h: number): Float64Array {
  const grid = new Float64Array(w * h);
  for (let i = 0; i < w * h; i++) grid[i] = seed(i) ? 0 : INF;
  const n = Math.max(w, h);
  const f = new Float64Array(n), d = new Float64Array(n), z = new Float64Array(n + 1), v = new Int32Array(n);
  for (let x = 0; x < w; x++) {
    for (let y = 0; y < h; y++) f[y] = grid[y * w + x];
    edt1d(f, h, d, v, z);
    for (let y = 0; y < h; y++) grid[y * w + x] = d[y];
  }
  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) f[x] = grid[y * w + x];
    edt1d(f, w, d, v, z);
    for (let x = 0; x < w; x++) grid[y * w + x] = d[x];
  }
  return grid;
}

// Positive inside the mask, negative outside, in pixels. Clamped to +-limit to keep Float32 tidy.
export function signedDistance(mask: Uint8Array, w: number, h: number, limit = 4096): Float32Array {
  const out = new Float32Array(w * h);
  let any = false;
  for (let i = 0; i < mask.length; i++) if (mask[i]) { any = true; break; }
  if (!any) return out.fill(-limit);
  const toInside = edt2d((i) => mask[i] !== 0, w, h);
  const toOutside = edt2d((i) => mask[i] === 0, w, h);
  for (let i = 0; i < out.length; i++) {
    const s = mask[i] ? Math.sqrt(toOutside[i]) - 0.5 : 0.5 - Math.sqrt(toInside[i]);
    out[i] = s > limit ? limit : s < -limit ? -limit : s;
  }
  return out;
}
