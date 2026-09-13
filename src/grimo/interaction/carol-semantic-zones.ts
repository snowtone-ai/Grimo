export const CAROL_SOURCE_SIZE = { width: 768, height: 493 } as const;

export type CarolZoneMeaning = "liked" | "normal" | "mild-dislike" | "special" | "excluded";
export type CarolSemanticZoneId =
  | "eyes-mouth"
  | "moon-stars"
  | "feet"
  | "tail"
  | "head-top"
  | "cheeks-ear-bases"
  | "body-fleece-back";

type Point = readonly [x: number, y: number];
type EllipseShape = { type: "ellipse"; center: Point; radius: Point };
type PolygonShape = { type: "polygon"; points: readonly Point[] };

export type CarolSemanticZone = {
  id: CarolSemanticZoneId;
  meaning: CarolZoneMeaning;
  label: string;
  shapes: readonly (EllipseShape | PolygonShape)[];
};

// Normalized geometry is intentionally independent of the colored touch-map PNG.
// Priority is significant: excluded/special/local zones precede the broad fleece zone.
export const CAROL_SEMANTIC_ZONES: readonly CarolSemanticZone[] = [
  {
    id: "eyes-mouth",
    meaning: "excluded",
    label: "eyes and inside mouth",
    shapes: [
      { type: "ellipse", center: [0.598, 0.60], radius: [0.038, 0.095] },
      { type: "ellipse", center: [0.755, 0.57], radius: [0.037, 0.09] },
      { type: "ellipse", center: [0.69, 0.69], radius: [0.031, 0.038] },
    ],
  },
  {
    id: "moon-stars",
    meaning: "special",
    label: "moon and stars",
    shapes: [
      { type: "ellipse", center: [0.35, 0.45], radius: [0.083, 0.15] },
      { type: "ellipse", center: [0.57, 0.30], radius: [0.045, 0.07] },
      { type: "ellipse", center: [0.61, 0.53], radius: [0.043, 0.065] },
      { type: "ellipse", center: [0.29, 0.78], radius: [0.038, 0.06] },
      { type: "ellipse", center: [0.72, 0.77], radius: [0.035, 0.055] },
    ],
  },
  {
    id: "feet",
    meaning: "mild-dislike",
    label: "feet",
    shapes: [
      { type: "ellipse", center: [0.40, 0.92], radius: [0.055, 0.075] },
      { type: "ellipse", center: [0.56, 0.94], radius: [0.06, 0.07] },
      { type: "ellipse", center: [0.72, 0.92], radius: [0.052, 0.075] },
    ],
  },
  {
    id: "tail",
    meaning: "mild-dislike",
    label: "tail area",
    shapes: [{ type: "ellipse", center: [0.19, 0.77], radius: [0.065, 0.10] }],
  },
  {
    id: "head-top",
    meaning: "liked",
    label: "head top",
    shapes: [{ type: "ellipse", center: [0.67, 0.35], radius: [0.20, 0.22] }],
  },
  {
    id: "cheeks-ear-bases",
    meaning: "liked",
    label: "cheeks and ear bases",
    shapes: [
      { type: "ellipse", center: [0.51, 0.64], radius: [0.07, 0.12] },
      { type: "ellipse", center: [0.82, 0.59], radius: [0.065, 0.11] },
      { type: "ellipse", center: [0.43, 0.61], radius: [0.075, 0.09] },
      { type: "ellipse", center: [0.89, 0.52], radius: [0.065, 0.08] },
    ],
  },
  {
    id: "body-fleece-back",
    meaning: "normal",
    label: "body fleece and back",
    shapes: [
      {
        type: "polygon",
        points: [
          [0.12, 0.31], [0.25, 0.12], [0.55, 0.02], [0.88, 0.17],
          [0.98, 0.47], [0.92, 0.85], [0.69, 0.94], [0.32, 0.91], [0.12, 0.73],
        ],
      },
    ],
  },
] as const;

function pointInPolygon(point: Point, polygon: readonly Point[]): boolean {
  let inside = false;
  for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
    const [xi, yi] = polygon[i];
    const [xj, yj] = polygon[j];
    const intersects = yi > point[1] !== yj > point[1]
      && point[0] < ((xj - xi) * (point[1] - yi)) / (yj - yi) + xi;
    if (intersects) inside = !inside;
  }
  return inside;
}

function contains(shape: EllipseShape | PolygonShape, point: Point): boolean {
  if (shape.type === "polygon") return pointInPolygon(point, shape.points);
  const dx = (point[0] - shape.center[0]) / shape.radius[0];
  const dy = (point[1] - shape.center[1]) / shape.radius[1];
  return dx * dx + dy * dy <= 1;
}

export function hitTestCarolZone(sourceX: number, sourceY: number): CarolSemanticZone | null {
  const point: Point = [sourceX / CAROL_SOURCE_SIZE.width, sourceY / CAROL_SOURCE_SIZE.height];
  return CAROL_SEMANTIC_ZONES.find((zone) => zone.shapes.some((shape) => contains(shape, point))) ?? null;
}
