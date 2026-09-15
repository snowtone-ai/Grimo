import { AppShell } from "@/components/app-shell/AppShell";

export default function GrimoPage() {
  return (
    <AppShell title="グリモ">
      <section className="grimo-stage" aria-labelledby="grimo-title">
        <div className="stage-copy">
          <p className="eyebrow">PHASE 0</p>
          <h1 id="grimo-title">Grimo 3D reconstruction in progress.</h1>
          <p>Character production will begin in the Full 3D foundation phase.</p>
        </div>
      </section>
    </AppShell>
  );
}
