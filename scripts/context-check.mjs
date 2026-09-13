import { readFile, access } from "node:fs/promises";

const required = [
  "AGENTS.md", "tasks.md", "xp.md", "docs/state.md", "docs/decisions.md", "docs/repo-map.md"
];
const budgets = new Map([["AGENTS.md", 5500], ["tasks.md", 5000], ["xp.md", 5000]]);
let failed = false;
for (const path of required) {
  try { await access(path); } catch { console.error(`missing context file: ${path}`); failed = true; continue; }
  const text = await readFile(path, "utf8");
  const budget = budgets.get(path);
  if (budget && Buffer.byteLength(text, "utf8") > budget) {
    console.error(`${path} exceeds context budget ${budget} bytes`); failed = true;
  }
}
if (failed) process.exit(1);
console.log("context entry points OK");
