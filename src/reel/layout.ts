/**
 * Ken Burns layout as plain numbers, so the picture and the safe-zone QC mask use the same maths:
 * scale the image to cover the frame, multiply by the zoom, put the focus point at the anchor and
 * clamp so no edge of the image ever shows.
 */
export type Rect = { x: number; y: number; w: number; h: number };

export const coverLayout = (
  iw: number,
  ih: number,
  W: number,
  H: number,
  focus: [number, number],
  anchor: [number, number],
  zoom: number,
): Rect => {
  const s = Math.max(W / iw, H / ih) * Math.max(1, zoom);
  const w = iw * s;
  const h = ih * s;
  const x = Math.min(0, Math.max(W - w, anchor[0] * W - focus[0] * w));
  const y = Math.min(0, Math.max(H - h, anchor[1] * H - focus[1] * h));
  return { x, y, w, h };
};

/** A box in 0..1 image coordinates -> pixels on screen, for an image drawn at `r`. */
export const mapBox = (b: [number, number, number, number], r: Rect): Rect => ({
  x: r.x + b[0] * r.w,
  y: r.y + b[1] * r.h,
  w: (b[2] - b[0]) * r.w,
  h: (b[3] - b[1]) * r.h,
});

/** Fit an image crop inside a box (contain), returning the full image rect and the crop's rect. */
export const fitCrop = (iw: number, ih: number, crop: [number, number, number, number], box: Rect): { image: Rect; crop: Rect } => {
  const cw = (crop[2] - crop[0]) * iw;
  const ch = (crop[3] - crop[1]) * ih;
  const s = Math.min(box.w / cw, box.h / ch);
  const cropRect = { x: box.x + (box.w - cw * s) / 2, y: box.y + (box.h - ch * s) / 2, w: cw * s, h: ch * s };
  return {
    image: { x: cropRect.x - crop[0] * iw * s, y: cropRect.y - crop[1] * ih * s, w: iw * s, h: ih * s },
    crop: cropRect,
  };
};

/**
 * coverLayout for a crop of the image: the crop [x0,y0,x1,y1] (0..1) covers the frame, and the
 * returned rect is where the whole image must be drawn (the parent clips the rest).
 */
export const coverCrop = (
  iw: number,
  ih: number,
  W: number,
  H: number,
  crop: [number, number, number, number],
  focus: [number, number],
  anchor: [number, number],
  zoom: number,
): Rect => {
  const cw = (crop[2] - crop[0]) * iw;
  const ch = (crop[3] - crop[1]) * ih;
  const r = coverLayout(cw, ch, W, H, focus, anchor, zoom);
  const s = r.w / cw;
  return { x: r.x - crop[0] * iw * s, y: r.y - crop[1] * ih * s, w: iw * s, h: ih * s };
};
