import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { NodeIO } from "@gltf-transform/core";
import { validateBytes, validateString, version as validatorVersion } from "gltf-validator";

const TRIANGLES = 4;
const TRIANGLE_STRIP = 5;
const TRIANGLE_FAN = 6;

function countTriangles(mode, count) {
  if (mode === TRIANGLES) return Math.floor(count / 3);
  if (mode === TRIANGLE_STRIP || mode === TRIANGLE_FAN) return Math.max(0, count - 2);
  return 0;
}

function getPrimitiveMetrics(primitive) {
  const indices = primitive.getIndices?.();
  const positions = primitive.getAttribute?.("POSITION");
  const count = indices?.getCount?.() ?? positions?.getCount?.() ?? 0;
  const mode = primitive.getMode?.() ?? TRIANGLES;
  const targets = primitive.getTargets?.() ?? [];
  const materials = primitive.getMaterial?.();

  return {
    triangles: countTriangles(mode, count),
    vertices: positions?.getCount?.() ?? 0,
    morphTargets: Array.isArray(targets) ? targets.length : Object.keys(targets).length,
    material: materials ?? null,
  };
}

function collectMetrics(document, bytes) {
  const root = document.getRoot();
  const primitives = root.listMeshes().flatMap((mesh) => mesh.listPrimitives());
  const primitiveMetrics = primitives.map(getPrimitiveMetrics);
  const materialSet = new Set(primitiveMetrics.map((item) => item.material).filter(Boolean));
  const joints = root.listSkins().flatMap((skin) => skin.getJoints?.() ?? []);
  const jointSet = new Set(joints);

  return {
    fileSizeBytes: bytes,
    triangleCount: primitiveMetrics.reduce((sum, item) => sum + item.triangles, 0),
    vertexCount: primitiveMetrics.reduce((sum, item) => sum + item.vertices, 0),
    materialCount: Math.max(materialSet.size, root.listMaterials().length),
    textureCount: root.listTextures().length,
    deformBoneCount: jointSet.size,
    morphTargetCount: primitiveMetrics.reduce((sum, item) => sum + item.morphTargets, 0),
    animationClips: root.listAnimations().map((animation, index) => animation.getName() || `Animation_${index + 1}`),
  };
}

function summarizeIssues(report) {
  const issues = report?.issues ?? {};
  const messages = Array.isArray(issues.messages) ? issues.messages : [];
  return {
    errors: issues.numErrors ?? 0,
    warnings: issues.numWarnings ?? 0,
    infos: issues.numInfos ?? 0,
    messages: messages.slice(0, 50).map((message) => ({
      code: message.code,
      severity: message.severity,
      message: message.message,
      pointer: message.pointer,
    })),
  };
}

export async function inspectGlb(inputPath) {
  const absolutePath = path.resolve(inputPath);
  const bytes = await fs.readFile(absolutePath);
  const extension = path.extname(absolutePath).toLowerCase();
  const validatorReport = extension === ".gltf"
    ? await validateString(bytes.toString("utf8"), { uri: absolutePath })
    : await validateBytes(new Uint8Array(bytes), { uri: absolutePath });
  const io = new NodeIO();
  const document = await io.read(absolutePath);

  return {
    file: absolutePath,
    validatorVersion,
    validator: summarizeIssues(validatorReport),
    metrics: collectMetrics(document, bytes.length),
  };
}

export function isMain(moduleUrl) {
  return path.resolve(fileURLToPath(moduleUrl)) === path.resolve(process.argv[1] ?? "");
}
