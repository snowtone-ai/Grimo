import { AppShell } from "@/components/app-shell/AppShell";
import { ShushuStage } from "@/components/grimo/ShushuStage";

export default function GrimoPage() {
  return (
    <AppShell title="グリモ">
      <ShushuStage />
    </AppShell>
  );
}
