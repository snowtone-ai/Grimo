import * as pc from "playcanvas";
import { loadShushuCandidate } from "../../assets/grimo/production/shushu/runtime/shushu-v004-loader-v004.mjs";
import { readShushuAsset, shushuAssets } from "./shushu-assets";

// The donor and Engine use a current Application during parsing. Serialize
// ownership across route changes, including an uncancellable in-flight parse.
let previousOwner = Promise.resolve();

// C1 is a neutral display, so render on demand: no invented idle or permanent RAF.
export function mountShushu(host: HTMLElement, report: (text: string) => void, ready: () => void, failed: (error: unknown) => void) {
  const waitForOwner = previousOwner;
  let releaseOwner: () => void = () => {};
  previousOwner = new Promise<void>(resolve => { releaseOwner = resolve; });
  const abort = new AbortController();
  const canvas = document.createElement("canvas");
  canvas.setAttribute("aria-label", "花飾りをつけたシュシュの3D表示");
  canvas.setAttribute("role", "img");
  host.appendChild(canvas);
  let app: pc.Application | undefined;
  let camera: pc.Entity;
  let candidate: Awaited<ReturnType<typeof loadShushuCandidate>> | undefined;
  let observer: ResizeObserver | undefined;
  let disposed = false;
  let loading = true;
  const timeout = window.setTimeout(() => fail(new Error("Shushu load timed out")), 120000);
  const destroy = () => {
    const context = app ? canvas.getContext("webgl2") : null;
    candidate?.dispose(); candidate = undefined;
    // The device is exclusive to this stage. Engine 2.22.2 can retain internal
    // fallback textures after asset unload; drain them while its GL is alive.
    if (app) for (const texture of app.graphicsDevice.textures) texture.destroy();
    app?.destroy(); app = undefined;
    // Release the exclusive browser context too: Engine destroy alone leaves
    // backbuffer/VAO allocations to browser GC on this Engine version.
    context?.getExtension("WEBGL_lose_context")?.loseContext();
    releaseOwner();
  };
  function dispose() {
    if (disposed) return;
    disposed = true;
    abort.abort();
    clearTimeout(timeout);
    observer?.disconnect();
    document.removeEventListener("visibilitychange", render);
    canvas.removeEventListener("webglcontextlost", contextLost);
    canvas.remove();
    // PlayCanvas parsing cannot be cancelled. Keep its device alive only until
    // the in-flight parse settles; then unload it before destroying the app.
    if (!loading) destroy();
  }
  function fail(error: unknown) { if (!disposed) { dispose(); failed(error); } }
  function contextLost(event: Event) { event.preventDefault(); fail(new Error("WebGL context lost")); }
  function render() {
    if (disposed || !candidate || !app || document.hidden) return;
    try {
      const width = Math.max(1, host.clientWidth), height = Math.max(1, host.clientHeight);
      app.resizeCanvas(width, height);
      // Vertical ortho extent grows on narrow screens; preserve full silhouette.
      camera.camera!.orthoHeight = Math.max(.61, .48 / (width / height));
      app.update(0); app.render();
      const ground = camera.camera!.worldToScreen(new pc.Vec3(0, 0, 0));
      host.parentElement?.style.setProperty("--shushu-ground", `${host.offsetTop + ground.y}px`);
    } catch (error) { fail(error); }
  }
  canvas.addEventListener("webglcontextlost", contextLost);
  document.addEventListener("visibilitychange", render);
  void (async () => {
    try {
      await waitForOwner;
      abort.signal.throwIfAborted();
      app = new pc.Application(canvas, { graphicsDeviceOptions: { deviceTypes: ["webgl2"], alpha: true, antialias: true } });
      app.graphicsDevice.maxPixelRatio = Math.min(window.devicePixelRatio || 1, 2);
      app.setCanvasFillMode(pc.FILLMODE_NONE);
      app.setCanvasResolution(pc.RESOLUTION_AUTO);
      app.scene.ambientLight = new pc.Color(.65, .65, .65);
      camera = new pc.Entity("Shushu front camera", app);
      camera.addComponent("camera", { clearColor: new pc.Color(0, 0, 0, 0), projection: pc.PROJECTION_ORTHOGRAPHIC, orthoHeight: .61, nearClip: .01, farClip: 20, toneMapping: pc.TONEMAP_ACES2 });
      camera.setPosition(0, .52, 3); camera.lookAt(0, .52, 0); app.root.addChild(camera);
      const light = new pc.Entity("Shushu soft key");
      light.addComponent("light", { type: "directional", intensity: 1 }); light.setEulerAngles(35, 25, 0); app.root.addChild(light);
      const readAsset = (url: string) => readShushuAsset(url, abort.signal, report);
      const started = performance.now();
      candidate = await loadShushuCandidate({ pc, app, url: shushuAssets.body.url, signal: abort.signal, readAsset,
        equipmentOptions: { flowerUrl: shushuAssets.flower.url, padsUrl: shushuAssets.pads.url, signal: abort.signal, readAsset } });
      abort.signal.throwIfAborted();
      loading = false;
      observer = new ResizeObserver(render); observer.observe(host);
      const frameStart = performance.now();
      render();
      if (disposed) return;
      performance.measure("shushu:load-to-first-render", { start: started, end: performance.now() });
      performance.measure("shushu:first-frame-submit", { start: frameStart, end: performance.now() });
      clearTimeout(timeout); ready();
    } catch (error) { fail(error); }
    finally { loading = false; if (disposed) destroy(); }
  })();
  return dispose;
}
