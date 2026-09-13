import { AppShell } from "@/components/app-shell/AppShell";
import { CarolViewport } from "@/components/grimo/CarolViewport";

export default function GrimoPage() {
  return (
    <AppShell title="グリモ">
      <section className="grimo-stage" aria-labelledby="carol-title">
        <div className="stage-copy">
          <p className="eyebrow">夢雲のひつじ</p>
          <h1 id="carol-title">Carol</h1>
          <p>今日は、すこし近くにいたいみたい。</p>
        </div>
        <CarolViewport />
        <p className="stage-hint">キャロルの様子を、そっと見守ってみよう</p>
      </section>
    </AppShell>
  );
}
