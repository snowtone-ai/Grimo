"""Render the standard Carol review views from a prepared Blender scene.

This script intentionally does not create a scene or a Carol asset. It fails
before rendering when the production prerequisites are not present.
"""

import argparse
import sys
from pathlib import Path

import bpy


CAPTURES = ("front", "three-quarter", "side", "back", "silhouette", "clay")
CAMERAS = {name: f"Carol_Camera_{name.replace('-', '_')}" for name in CAPTURES}


def parse_args():
    parser = argparse.ArgumentParser(description="Render standard Carol Human Gate captures.")
    parser.add_argument("--output-dir", type=Path, required=True, help="Repository-relative or absolute output directory.")
    return parser.parse_args()


def require_scene():
    missing = [f"camera '{name}'" for name in CAMERAS.values() if bpy.data.objects.get(name) is None]
    if bpy.data.objects.get("Carol_Model") is None:
        missing.append("object 'Carol_Model'")
    if missing:
        raise RuntimeError("Carol Gate prerequisites missing: " + ", ".join(missing))


def render_captures(output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    scene = bpy.context.scene
    for capture, camera_name in CAMERAS.items():
        scene.camera = bpy.data.objects[camera_name]
        scene.render.filepath = str(output_dir / f"carol-{capture}.png")
        bpy.ops.render.render(write_still=True)


def main():
    args = parse_args()
    try:
        require_scene()
        render_captures(args.output_dir)
    except (OSError, RuntimeError) as error:
        print(f"Carol Gate render failed: {error}", file=sys.stderr)
        return 1
    print(f"Carol Gate renders written to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
