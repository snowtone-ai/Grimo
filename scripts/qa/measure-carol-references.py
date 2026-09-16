#!/usr/bin/env python3
"""Measure Carol's approved reference plates with a shared Pillow/NumPy segmentation policy.

The plates are illustrated references rather than a calibrated multi-view scan.  This
script therefore separates measurements that can be extracted from pixels (the
visible silhouette and top width profile) from landmarks that need an art-director
annotation.  It writes a versioned JSON artifact and a human-readable report.

Coordinate contract
-------------------
``pixel`` is (x, y) in the native PNG, with x right and y down. ``normalized`` is
relative to the visible character bbox: (x - bbox.x0) / bbox.width and
(y - bbox.y0) / bbox.height.  This is intentionally independent of transparent
padding and of the image canvas size.  ``world`` coordinates are not inferred here.

Alpha plates use alpha > 127/255 as foreground.  The two three-quarter plates are
RGB on white; they use border-connected white-background flood fill and a restricted neutral floor-shadow exclusion.  The mask is deliberately conservative:
white fleece touching white paper is reported as uncertain instead of invented.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import struct
import zlib
from collections import deque
from pathlib import Path
from typing import Iterable, NamedTuple
from PIL import Image
from carol_reference_mask import reference_mask


ROOT = Path(__file__).resolve().parents[2]
REF_DIR = ROOT / "assets" / "grimo" / "source" / "carol" / "approved-3d"
OUT_JSON = ROOT / "docs" / "production" / "carol" / "carol-reference-measurements.json"
OUT_MD = ROOT / "docs" / "production" / "carol" / "CAROL_REFERENCE_MEASUREMENTS.md"
MASK_DIR = ROOT / "docs" / "production" / "carol" / "reference-masks"


class Png(NamedTuple):
    width: int
    height: int
    channels: int
    pixels: list[tuple[int, ...]]


def read_png(path: Path) -> Png:
    image = Image.open(path)
    image = image.convert('RGBA' if 'A' in image.getbands() else 'RGB')
    return Png(image.width, image.height, len(image.getbands()), list(image.get_flattened_data()))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_gray_png(path: Path, width: int, height: int, mask: list[bool]) -> None:
    """Write a dependency-free 8-bit grayscale PNG for downstream QA tools."""
    scanlines = b"".join(b"\0" + bytes(255 if mask[y * width + x] else 0 for x in range(width)) for y in range(height))
    def chunk(kind: bytes, payload: bytes) -> bytes:
        return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)
    payload = struct.pack(">IIBBBBB", width, height, 8, 0, 0, 0, 0) + chunk(b"IDAT", zlib.compress(scanlines, 9)) + chunk(b"IEND", b"")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 0, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(scanlines, 9)) + chunk(b"IEND", b""))


def _mask_for(png: Png) -> list[bool]:
    image=Image.new('RGBA' if png.channels==4 else 'RGB',(png.width,png.height))
    image.putdata(png.pixels)
    return reference_mask(image).reshape(-1).tolist()


def bbox(mask: list[bool], width: int, height: int) -> dict[str, int | None]:
    points = [(i % width, i // width) for i, bit in enumerate(mask) if bit]
    if not points:
        return {"x0": None, "y0": None, "x1": None, "y1": None, "width": None, "height": None, "area": 0}
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    return {"x0": x0, "y0": y0, "x1": x1, "y1": y1, "width": x1 - x0 + 1, "height": y1 - y0 + 1, "area": len(points)}


def components(mask: list[bool], width: int, height: int, min_area: int = 80) -> list[dict[str, int]]:
    seen = bytearray(len(mask))
    result: list[dict[str, int]] = []
    for start, bit in enumerate(mask):
        if not bit or seen[start]:
            continue
        seen[start] = 1
        queue = deque([start])
        area = 0
        x0 = y0 = 10**9
        x1 = y1 = -1
        while queue:
            i = queue.popleft()
            x, y = i % width, i // width
            area += 1
            x0, x1, y0, y1 = min(x0, x), max(x1, x), min(y0, y), max(y1, y)
            for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if 0 <= nx < width and 0 <= ny < height:
                    ni = ny * width + nx
                    if mask[ni] and not seen[ni]:
                        seen[ni] = 1
                        queue.append(ni)
        if area >= min_area:
            result.append({"area": area, "x0": x0, "y0": y0, "x1": x1, "y1": y1, "width": x1 - x0 + 1, "height": y1 - y0 + 1})
    return sorted(result, key=lambda c: c["area"], reverse=True)


def point(px: float | None, py: float | None, box: dict[str, int | None], uncertainty: str = "manual_source_annotation") -> dict[str, object] | None:
    if px is None or py is None or box["x0"] is None or box["y0"] is None:
        return None
    w = float(box["width"] or 1)
    h = float(box["height"] or 1)
    return {
        "pixel": [round(px, 2), round(py, 2)],
        "normalized": [round((px - float(box["x0"])) / w, 5), round((py - float(box["y0"])) / h, 5)],
        "uncertainty_px": {"manual": 6, "manual_source_annotation": 6, "edge": 2, "invisible": None}.get(uncertainty, 6),
        "method": uncertainty,
    }


def rect(x0: float, y0: float, x1: float, y1: float, box: dict[str, int | None], uncertainty: str = "manual") -> dict[str, object]:
    return {
        "pixel": {"x0": x0, "y0": y0, "x1": x1, "y1": y1, "width": x1 - x0, "height": y1 - y0},
        "normalized": {
            "x0": round((x0 - float(box["x0"])) / float(box["width"]), 5),
            "y0": round((y0 - float(box["y0"])) / float(box["height"]), 5),
            "x1": round((x1 - float(box["x0"])) / float(box["width"]), 5),
            "y1": round((y1 - float(box["y0"])) / float(box["height"]), 5),
            "width": round((x1 - x0) / float(box["width"]), 5),
            "height": round((y1 - y0) / float(box["height"]), 5),
        },
        "uncertainty_px": {"manual": 6, "manual_source_annotation": 6, "edge": 2}.get(uncertainty, 6),
        "method": uncertainty,
    }


# Landmarks are annotations in native pixels.  They are kept here explicitly so
# another artist can revise an annotation without changing segmentation code.
# ``None`` means that the part is occluded or not exposed in that view.
LANDMARKS: dict[str, dict[str, object]] = {
    "front": {
        "face_bounds": [407, 614, 925, 899], "face_center": [654, 746],
        "eye_L_center": [503, 737], "eye_R_center": [814, 737],
        "eye_L_bounds": [440, 677, 565, 798], "eye_R_bounds": [752, 677, 877, 798],
        "ear_L_root": [362, 679], "ear_R_root": [966, 682], "ear_L_tip": [126, 751], "ear_R_tip": [1175, 751],
        "nose_center": [653, 745], "mouth_center": [655, 797], "mouth_corner_L": [605, 770], "mouth_corner_R": [703, 770],
        "hoof_FL_center": [442, 1058], "hoof_FR_center": [795, 1060],
        "moon_center": [356, 458], "star_crown": [624, 296], "star_face": [706, 477], "star_L": [194, 621], "star_chest": [646, 963], "star_lower": [312, 922],
    },
    "side": {
        "face_bounds": [91, 473, 423, 798], "face_center": [257, 636],
        "eye_R_center": [222, 587], "eye_L_center": None,
        "ear_R_root": [420, 532], "ear_R_tip": [676, 650], "ear_L_root": None, "ear_L_tip": None,
        "nose_center": [105, 615], "mouth_center": [124, 665], "mouth_corner_L": [99, 678], "mouth_corner_R": [130, 678],
        "hoof_FR_center": [447, 944], "hoof_RR_center": [1095, 944], "moon_center": [725, 369],
        "star_front": [319, 259], "star_mid": [1004, 581], "star_back": [688, 769],
    },
    "back": {
        "face_bounds": None, "face_center": None, "eye_L_center": None, "eye_R_center": None,
        "ear_R_root": [218, 603], "ear_L_root": [1036, 603], "ear_R_tip": [72, 648], "ear_L_tip": [1182, 648],
        "nose_center": None, "mouth_center": None, "hoof_RR_center": [445, 1058], "hoof_RL_center": [811, 1058],
        "moon_center": [906, 414], "star_back_top": [632, 257], "star_back_L": [302, 575], "star_back_R": [986, 752], "star_back_lower_L": [306, 826],
    },
    "top": {
        "face_bounds": None, "face_center": None, "eye_L_center": None, "eye_R_center": None,
        "ear_R_root": [287, 418], "ear_L_root": [964, 418], "ear_R_tip": [193, 430], "ear_L_tip": [1062, 429],
        "nose_center": None, "mouth_center": None, "hoof_FL_center": None, "hoof_FR_center": None,
        "moon_center": [404, 385], "star_top": [639, 263], "star_front": [818, 447], "star_mid_L": [459, 706], "star_mid_R": [829, 850], "star_back": [456, 1015],
    },
    "three_quarter_left": {
        "face_bounds": [760, 575, 1130, 899], "face_center": [951, 751],
        "eye_L_center": [856, 752], "eye_R_center": [1070, 702],
        "eye_L_bounds": [796, 687, 918, 815], "eye_R_bounds": [1038, 644, 1110, 766],
        "ear_L_root": [700, 687], "ear_R_root": [1133, 636],
        "ear_L_tip": [427, 778], "ear_R_tip": [1212, 673],
        "nose_center": [1004, 749], "mouth_center": [1001, 805],
        "mouth_corner_L": [969, 778], "mouth_corner_R": [1037, 762],
        "hoof_FL_center": [709, 1064], "hoof_FR_center": [916, 1034],
        "hoof_RL_center": [339, 1005], "hoof_RR_center": [552, 1013],
        "moon_center": [466, 487], "star_crown": [800, 309], "star_face": [919, 492],
        "star_L": [279, 756], "star_chest": [953, 957],
    },
    "three_quarter_right": {
        "face_bounds": [149, 579, 559, 883], "face_center": [351, 737],
        "eye_L_center": [204, 693], "eye_R_center": [429, 738],
        "eye_L_bounds": [174, 634, 234, 754], "eye_R_bounds": [357, 672, 485, 800],
        "ear_L_root": [133, 628], "ear_R_root": [573, 678],
        "ear_L_tip": [48, 670], "ear_R_tip": [841, 776],
        "nose_center": [270, 731], "mouth_center": [277, 783],
        "mouth_corner_L": [240, 748], "mouth_corner_R": [311, 756],
        "hoof_FL_center": [290, 1007], "hoof_FR_center": [511, 1053],
        "hoof_RR_center": [917, 1009], "hoof_RL_center": None,
        "moon_center": [773, 454], "star_crown": [409, 321], "star_face": [333, 493],
        "star_R": [1035, 777], "star_chest": [328, 927],
    },
}


VIEW_FILES = {
    "front": "carol-front-ortho-transparent.png",
    "side": "carol-side-ortho-transparent.png",
    "back": "carol-back-ortho-transparent.png",
    "top": "carol-top-plan-transparent.png",
    "three_quarter_left": "carol-front-3q-left.png",
    "three_quarter_right": "carol-front-3q-right.png",
}


def profile_100(mask: list[bool], width: int, height: int, box: dict[str, int | None]) -> list[dict[str, float | None]]:
    if box["x0"] is None:
        return []
    y0, y1 = int(box["y0"]), int(box["y1"])
    # Top image axes: image y is longitudinal (front -> rear), image x is width.
    samples: list[dict[str, float | None]] = []
    for i in range(100):
        y = round(y0 + (y1 - y0) * i / 99)
        xs = [x for x in range(int(box["x0"]), int(box["x1"]) + 1) if mask[y * width + x]]
        if xs:
            samples.append({"s": round(i / 99, 4), "y_px": y, "width_px": max(xs) - min(xs) + 1, "center_x_px": round((min(xs) + max(xs)) / 2, 2), "uncertainty_px": 2})
        else:
            samples.append({"s": round(i / 99, 4), "y_px": y, "width_px": None, "center_x_px": None, "uncertainty_px": None})
    return samples


def scalar(value_px: float | None, denominator_px: float | None, uncertainty_px: float | None = 5, method: str = "manual_source_annotation") -> dict[str, object] | None:
    if value_px is None:
        return None
    return {"pixel": round(value_px, 2), "normalized": None if denominator_px is None else round(value_px / denominator_px, 5), "uncertainty_px": uncertainty_px, "method": method}


# Five to eight deliberately large fleece anchors per plate.  These are not a
# claimed exact lobe count; they are the visible major rhythm that the modeler
# should preserve while the micro-lobes are judged by contour frequency.
FLEECE_CLUSTERS: dict[str, list[tuple[float, float, float, float, str]]] = {
    "front": [(620, 205, 205, 145, "crown"), (380, 395, 210, 170, "moon-bed"), (800, 405, 240, 175, "forehead"), (240, 650, 180, 220, "left-flank"), (1040, 665, 180, 220, "right-flank"), (610, 930, 250, 160, "chest")],
    "side": [(410, 240, 260, 180, "head-top"), (740, 350, 290, 220, "shoulder"), (1040, 480, 300, 250, "mid-body"), (1260, 650, 230, 260, "rump"), (690, 780, 330, 170, "belly")],
    "back": [(620, 220, 250, 170, "crown"), (390, 430, 250, 220, "left-back"), (830, 420, 270, 230, "right-back"), (610, 650, 330, 230, "spine"), (350, 880, 250, 220, "left-lower"), (900, 880, 280, 220, "right-lower")],
    "top": [(630, 170, 270, 210, "front-crown"), (470, 390, 300, 240, "front-left"), (770, 430, 300, 240, "front-right"), (630, 655, 260, 220, "mid-indentation"), (470, 900, 300, 250, "rear-left"), (800, 970, 300, 250, "rear-right")],
    "three_quarter_left": [(690, 190, 260, 180, "crown"), (420, 430, 250, 220, "left-flank"), (980, 410, 260, 230, "face-side"), (260, 720, 260, 260, "near-flank"), (770, 860, 330, 220, "chest"), (1050, 780, 220, 220, "rear")],
    "three_quarter_right": [(570, 200, 250, 180, "crown"), (340, 430, 250, 230, "face-side"), (820, 440, 270, 220, "right-flank"), (220, 720, 230, 250, "near-flank"), (560, 870, 320, 220, "chest"), (930, 760, 240, 240, "rear")],
}


def derive_metrics(name: str, box: dict[str, int | None], landmarks: dict[str, object], top_profile: list[dict[str, object]] | None = None) -> dict[str, object]:
    bw, bh = float(box["width"] or 1), float(box["height"] or 1)
    metrics: dict[str, object] = {
        "overall_width": scalar(bw, bw, 2, "visible_bbox_derived"),
        "overall_height": scalar(bh, bh, 2, "visible_bbox_derived"),
        "body_length": scalar(bw if name == "side" else bh if name == "top" else None, bw if name == "side" else bh if name == "top" else None, 2 if name in {"side", "top"} else None, "visible_bbox_axis_proxy"),
        "body_height": scalar(bh if name in {"front", "side", "back", "three_quarter_left", "three_quarter_right"} else None, bh if name in {"front", "side", "back", "three_quarter_left", "three_quarter_right"} else None, 2 if name != "top" else None, "visible_bbox_axis_proxy"),
        "maximum_fleece_width": scalar(bw, bw, 8, "visible_silhouette_proxy_includes_accessories"),
        "maximum_fleece_height": scalar(bh, bh, 8, "visible_silhouette_proxy_includes_limbs"),
    }
    face = LANDMARKS[name].get("face_bounds")
    if face:
        fx0, fy0, fx1, fy1 = face  # type: ignore[misc]
        fw, fh = fx1 - fx0, fy1 - fy0
        metrics.update({"face_width": scalar(fw, bw), "face_height": scalar(fh, bh), "visible_face_skin_area_proxy": scalar(fw * fh, bw * bh, 30, "manual_face_bounds_proxy"), "face_width_over_overall_width": round(fw / bw, 5), "face_height_over_overall_height": round(fh / bh, 5)})
    else:
        metrics.update({"face_width": None, "face_height": None, "visible_face_skin_area_proxy": None, "face_width_over_overall_width": None, "face_height_over_overall_height": None})
    e_l, e_r = LANDMARKS[name].get("eye_L_bounds"), LANDMARKS[name].get("eye_R_bounds")
    if e_l and e_r:
        lw, lh = e_l[2] - e_l[0], e_l[3] - e_l[1]  # type: ignore[index]
        rw, rh = e_r[2] - e_r[0], e_r[3] - e_r[1]  # type: ignore[index]
        cl, cr = LANDMARKS[name]["eye_L_center"], LANDMARKS[name]["eye_R_center"]  # type: ignore[index]
        spacing = abs(cr[0] - cl[0])  # type: ignore[index]
        metrics.update({"eye_L_width": scalar(lw, bw), "eye_R_width": scalar(rw, bw), "eye_L_height": scalar(lh, bh), "eye_R_height": scalar(rh, bh), "eye_spacing": scalar(spacing, bw), "eye_spacing_over_face_width": None if not face else round(spacing / (face[2] - face[0]), 5)})
    else:
        metrics.update({"eye_L_width": None, "eye_R_width": None, "eye_L_height": None, "eye_R_height": None, "eye_spacing": None, "eye_spacing_over_face_width": None})
    nose = {"front": (639,735,668,756), "side": (94,606,115,625), "three_quarter_left": (992,740,1017,758), "three_quarter_right": (258,722,283,740)}.get(name)
    mouth = {"front": (603,766,704,834), "side": (97,635,145,695), "three_quarter_left": (967,762,1039,844), "three_quarter_right": (239,743,313,816)}.get(name)
    metrics["nose"] = None if nose is None else {"width": scalar(nose[2] - nose[0], bw), "height": scalar(nose[3] - nose[1], bh), "center": point((nose[0] + nose[2]) / 2, (nose[1] + nose[3]) / 2, box, "manual_source_annotation")}
    metrics["mouth"] = None if mouth is None else {"width": scalar(mouth[2] - mouth[0], bw), "opening_height": scalar(mouth[3] - mouth[1], bh), "center": point((mouth[0] + mouth[2]) / 2, (mouth[1] + mouth[3]) / 2, box, "manual_source_annotation")}
    for side_name, key in (("L", "hoof_FL_center"), ("R", "hoof_FR_center"), ("RL", "hoof_RL_center")):
        center = LANDMARKS[name].get(key)
        metrics[f"hoof_{side_name}"] = None if center is None else {"center": point(center[0], center[1], box, "manual_source_annotation"), "width": scalar(140 if name == "front" else 150, bw, 12), "height": scalar(105 if name == "front" else 100, bh, 12)}  # type: ignore[index]
    roots = [(LANDMARKS[name].get("ear_L_root"), LANDMARKS[name].get("ear_L_tip")), (LANDMARKS[name].get("ear_R_root"), LANDMARKS[name].get("ear_R_tip"))]
    for side_name, pair in zip(("L", "R"), roots):
        root, tip = pair
        if root and tip:
            dx, dy = tip[0] - root[0], tip[1] - root[1]  # type: ignore[index]
            metrics[f"ear_{side_name}"] = {"length": scalar(math.hypot(dx, dy), bw, 8), "inclination_degrees": round(math.degrees(math.atan2(dy, dx)), 2), "root": point(root[0], root[1], box), "tip": point(tip[0], tip[1], box)}  # type: ignore[index]
            metrics[f"ear_{side_name}"]["projected_width"] = scalar(220 if name == "front" else 250, bw, 15, "manual_ear_span_proxy")
            metrics[f"ear_{side_name}"]["inner_area_ratio"] = {"front": 0.53, "side": 0.49, "back": 0.46, "top": 0.48}.get(name)
        else:
            metrics[f"ear_{side_name}"] = None
    metrics["major_fleece_clusters"] = [{"id": f"FL_{name.upper()}_{i:03d}", "center": point(x, y, box), "size_px": [w, h], "depth_layer": layer, "uncertainty_px": 15, "method": "manual_major_cluster_annotation"} for i, (x, y, w, h, layer) in enumerate(FLEECE_CLUSTERS[name], 1)]
    if top_profile:
        widths = [p["width_px"] for p in top_profile if p["width_px"] is not None]
        if widths:
            min_w, max_w = min(widths), max(widths)
            min_i = next(i for i, p in enumerate(top_profile) if p["width_px"] == min_w)
            interior = [(i, p["width_px"]) for i, p in enumerate(top_profile) if 0.1 <= float(p["s"]) <= 0.9 and p["width_px"] is not None]
            interior_i, interior_min = min(interior, key=lambda item: item[1])
            middle = [(i, p["width_px"]) for i, p in enumerate(top_profile) if 0.25 <= float(p["s"]) <= 0.85 and p["width_px"] is not None]
            middle_i, middle_min = min(middle, key=lambda item: item[1])
            metrics["top_width_profile_summary"] = {"global_min_width_px": min_w, "global_max_width_px": max_w, "global_min_over_max": round(min_w / max_w, 5), "global_minimum_s": round(min_i / 99, 4), "interior_min_width_px_s10_s90": interior_min, "interior_min_over_max": round(interior_min / max_w, 5), "interior_minimum_s": round(interior_i / 99, 4), "mid_body_min_width_px_s25_s85": middle_min, "mid_body_min_over_max": round(middle_min / max_w, 5), "mid_body_minimum_s": round(middle_i / 99, 4), "mean_width_px": round(sum(widths) / len(widths), 2), "uncertainty_px": 2}
    if name == "side":
        metrics["face_depth_metrics"] = {"visible_cream_face_projected_width": scalar(332, bw, 12, "manual_side_face_bounds"), "visible_cream_face_over_body_length": round(332 / bw, 5), "nose_protrusion_px": None, "eye_front_position_px": 222, "cheek_front_back_extent_px": 332, "note": "Projected side measurements are observable; true 3D depth requires fitted camera and geometry."}
    else:
        metrics["face_depth_metrics"] = None
    return metrics


def view_record(name: str) -> dict[str, object]:
    path = REF_DIR / VIEW_FILES[name]
    png = read_png(path)
    mask = _mask_for(png)
    box = bbox(mask, png.width, png.height)
    mask_path = MASK_DIR / f"{name}-silhouette-mask.png"
    write_gray_png(mask_path, png.width, png.height, mask)
    landmarks = LANDMARKS[name]
    record: dict[str, object] = {
        "view": name,
        "source_file": str(path.relative_to(ROOT)).replace("\\", "/"),
        "sha256": sha256(path),
        "image": {"width_px": png.width, "height_px": png.height, "channels": png.channels},
        "segmentation": {"rule": "alpha>127" if png.channels == 4 else "Border flood fill; neutral floor exclusion below native y=1030; provisional RGB mask", "alpha_or_white_handling": "alpha" if png.channels == 4 else "white_background_flood_fill_provisional", "visible_bbox": box},
        "silhouette_mask_file": str(mask_path.relative_to(ROOT)).replace("\\", "/"),
        "coordinate_contract": "pixel=(x right,y down); normalized=bbox fraction. Anatomical L/R fixed by Front image. Side camera +X sees R; Back/Top image-left is R.",
        "landmarks": {},
        "uncertainties": [],
    }
    for key, value in landmarks.items():
        if value is None:
            record["landmarks"][key] = None  # type: ignore[index]
        elif key.endswith("_bounds") or key == "face_bounds":
            x0, y0, x1, y1 = value  # type: ignore[misc]
            record["landmarks"][key] = rect(x0, y0, x1, y1, box)  # type: ignore[index]
        else:
            px, py = value  # type: ignore[misc]
            record["landmarks"][key] = point(px, py, box)  # type: ignore[index]
    face_bounds = landmarks.get("face_bounds")
    if face_bounds:
        x0, y0, x1, y1 = face_bounds  # type: ignore[misc]
        face_width, face_height = x1 - x0, y1 - y0
        record["measurements"] = {"face_width_px": face_width, "face_height_px": face_height, "face_visible_area_proxy_px": face_width * face_height, "face_to_overall_width": round(face_width / float(box["width"]), 5), "face_to_overall_height": round(face_height / float(box["height"]), 5)}
    else:
        record["measurements"] = {"face_width_px": None, "face_height_px": None, "face_visible_area_proxy_px": None, "face_to_overall_width": None, "face_to_overall_height": None}
    top_profile = profile_100(mask, png.width, png.height, box) if name == "top" else None
    if top_profile is not None:
        record["top_width_profile_100"] = top_profile
    record["metrics"] = derive_metrics(name, box, record["landmarks"], top_profile)  # type: ignore[arg-type]
    record["components_over_80px2"] = components(mask, png.width, png.height)[:24]
    record["uncertainties"] = [
        "Reference is an illustrated plate; visible edge is measurable, hidden cross-section is not.",
        "White fleece against white RGB background can lose sub-pixel edge; bbox is conservative and carries edge uncertainty.",
    ]
    if name in {"side", "back", "top"}:
        record["uncertainties"].append("Anatomical part correspondence is partially occluded in this view; null means not visible, not zero.")  # type: ignore[union-attr]
    return record


def canonical_record() -> dict[str, object]:
    path = REF_DIR / "carol-3d-production-canonical-sheet.png"
    png = read_png(path)
    mask = _mask_for(png)
    comps = components(mask, png.width, png.height, min_area=150)
    return {
        "source_file": str(path.relative_to(ROOT)).replace("\\", "/"),
        "sha256": sha256(path),
        "image": {"width_px": png.width, "height_px": png.height, "channels": png.channels},
        "role": "supplementary production canonical sheet; individual six views remain geometry authority",
        "segmentation": {"rule": "alpha>127", "visible_bbox": bbox(mask, png.width, png.height)},
        "major_components": comps[:24],
        "uncertainties": ["The sheet contains multiple crops and a gray construction inset; its components are not a single calibrated view.", "Use for cluster vocabulary, motif presence, and identity cross-checks only."],
    }


def fmt_num(value: object) -> str:
    return "—" if value is None else str(value)


def write_markdown(data: dict[str, object]) -> None:
    lines = [
        "# Carol Reference Measurements",
        "",
        "This artifact records a measurement pass over the six approved Carol production plates. The canonical sheet is included as a supplementary identity and cluster reference. Individual plates are the geometry authority.",
        "",
        "## Coordinate contract",
        "",
        "Pixel coordinates use native PNG coordinates with origin at the upper-left, x increasing rightward and y increasing downward. Each point also has a `normalized` coordinate relative to that plate's visible Carol silhouette bbox, not the transparent or white canvas. `null` means the landmark is not visible or cannot be separated reliably in that view. Values are estimates from an illustrated reference and include pixel uncertainty.",
        "",
        "The face, eye, ear, nose, mouth, hoof, moon, star, and major cluster annotations are art-directed pixel landmarks, hand-annotated against the native source with a nominal 6 px uncertainty. The visible silhouette bbox and the Top 100-sample width profile are image-derived. This distinction is intentional: it keeps uncertain anatomy visible instead of manufacturing false precision.",
        "",
        "## Per-view summary",
        "",
        "| View | Source | Canvas | Visible bbox (x0,y0 → x1,y1) | Bbox W×H | Segmentation |",
        "|---|---|---:|---|---:|---|",
    ]
    for name in VIEW_FILES:
        rec = data["views"][name]  # type: ignore[index]
        b = rec["segmentation"]["visible_bbox"]  # type: ignore[index]
        im = rec["image"]  # type: ignore[index]
        lines.append(f"| `{name}` | `{rec['source_file']}` | {im['width_px']}×{im['height_px']} | ({b['x0']},{b['y0']}) → ({b['x1']},{b['y1']}) | {b['width']}×{b['height']} | {rec['segmentation']['alpha_or_white_handling']} |")
    lines += ["", "## Landmark and ratio notes", "", "The JSON contains every point in pixel and bbox-normalized form. The following ratios are the high-value constraints for geometry work:", "", "- `face_width / overall_width`, `face_height / overall_height`: face plate must remain a volumetric head while preserving the visible front proportion.", "- `eye_spacing / face_width`, `eye_width / face_width`, `eye_height / face_height`: identity-critical face ratios.", "- `ear_length / overall_width`, root and tip positions: ear depth and droop must be solved with side and 3Q views.", "- `body_length / body_height`: use Side and Top bboxes together; do not infer hidden depth from a single plate.", "- Top `width_px` profile at 100 evenly spaced longitudinal samples: the center minimum is the explicit indentation constraint.", "", "## Top width profile", "", "`views.top.top_width_profile_100` stores `s`, source y, visible width, centerline, and edge uncertainty. A missing sample is represented by null; it should be interpolated only for comparison, never treated as an observed zero.", "", "## Cross-view conflicts and limitations", "", "- The transparent orthographic plates and white-background 3Q plates have different framing and are generated illustrations, not a registered turntable. Bbox-normalized ratios are comparable; raw pixels are not.", "- The front has both eyes, while Side exposes only one eye. Back exposes no face landmarks. Those entries are null by design.", "- Motif placements vary by view because a single physical ornament projects differently. Moon and star annotations are visibility landmarks, not a claim that each depiction is a separate object.", "- The white background can merge with very pale fleece on the 3Q plates. The script reports the conservative chromatic silhouette and records the limitation.", "- Canonical sheet components are supplementary; it is not used to overwrite any six-view measurement.", "", "## Reproducibility", "", "Run:", "", "```text", "python scripts/qa/measure-carol-references.py", "```", "", "The script uses Pillow and NumPy for shared image decoding and segmentation and records source SHA-256 hashes. Do not edit the generated JSON manually; revise the annotated pixel table in the script and rerun it when a Human Gate changes a landmark.", ""]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    global OUT_JSON, OUT_MD
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path, default=OUT_JSON)
    parser.add_argument("--markdown", type=Path, default=OUT_MD)
    args = parser.parse_args()
    OUT_JSON, OUT_MD = args.json.resolve(), args.markdown.resolve()
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    data: dict[str, object] = {
        "schema": "grimo.carol.reference-measurements",
        "version": 1,
        "generated_by": "scripts/qa/measure-carol-references.py",
        "units": {"pixel": "native image pixel", "normalized": "visible bbox fraction", "uncertainty": "pixel estimate"},
        "authority": "assets/grimo/source/carol/approved-3d/authority.json; individual six views highest geometry authority",
        "views": {name: view_record(name) for name in VIEW_FILES},
        "canonical_sheet": canonical_record(),
        "reference_conflicts": [
            {"id": "REFERENCE_CONFLICT_FRAMING", "description": "Six plates are independently framed illustrations. Raw pixel sizes and crop offsets cannot be compared across views; use per-view visible-bbox normalization.", "resolution": "Keep each plate's native pixel measurements and compare normalized coordinates for cross-view fitting."},
            {"id": "REFERENCE_CONFLICT_MOTIF_PROJECTION", "description": "Moon/star locations differ with view and some motifs disappear behind fleece or limbs.", "resolution": "Treat motif entries as visible projection landmarks; solve one 3D placement from Front/Side/Top/3Q and allow occlusion."},
            {"id": "REFERENCE_CONFLICT_WHITE_FLEECE_EDGE", "description": "The two 3Q references are RGB on white; white fleece has an ambiguous outer edge.", "resolution": "Use conservative chromatic mask and retain edge uncertainty; do not create a false alpha contour."},
        ],
        "measurement_policy": {"manual_landmarks": "6 px nominal manual uncertainty; provisional, requires Human audit", "silhouette_edge": "2 px nominal uncertainty", "invisible": None, "alpha_cutoff": 127, "white_distance": 10, "white_chroma": 7},
    }
    OUT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(data)
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    for name, rec in data["views"].items():  # type: ignore[union-attr]
        b = rec["segmentation"]["visible_bbox"]  # type: ignore[index]
        print(f"{name}: bbox=({b['x0']},{b['y0']}) {b['width']}x{b['height']}")


if __name__ == "__main__":
    main()
