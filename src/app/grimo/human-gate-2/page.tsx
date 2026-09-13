import Link from "next/link";
import { CarolViewport } from "@/components/grimo/CarolViewport";
import { CAROL_IDLE_VARIANTS, parseCarolIdleVariant } from "@/grimo/motion/carol-motion";

export default async function CarolHumanGateTwoPage({ searchParams }: { searchParams: Promise<{ idleVariant?: string }> }) {
  const { idleVariant: requestedVariant } = await searchParams;
  const idleVariant = parseCarolIdleVariant(requestedVariant ?? null);
  const candidate = CAROL_IDLE_VARIANTS[idleVariant];

  return (
    <main className="human-gate" aria-labelledby="human-gate-title">
      <header className="human-gate__header">
        <div>
          <p className="eyebrow">Human Gate 2 · Carol idle / presence</p>
          <h1 id="human-gate-title">{candidate.label}</h1>
          <p>{candidate.description}</p>
        </div>
        <Link href="/grimo" className="human-gate__exit">グリモへ戻る</Link>
      </header>
      <CarolViewport key={idleVariant} />
      <nav className="human-gate__variants" aria-label="アイドル候補">
        {Object.values(CAROL_IDLE_VARIANTS).map((variant) => (
          <Link
            key={variant.id}
            href={`/grimo/human-gate-2?idleVariant=${variant.id}`}
            className={variant.id === idleVariant ? "human-gate__variant is-selected" : "human-gate__variant"}
            aria-current={variant.id === idleVariant ? "page" : undefined}
          >
            {variant.id}
          </Link>
        ))}
      </nav>
      <p className="human-gate__instruction">Chrome を全画面表示にし、A → B → C の順で各候補を30秒ずつ見比べてください。切替ごとに同じ初期状態から再生されます。</p>
    </main>
  );
}
