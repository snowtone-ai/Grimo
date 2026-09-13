# Migration from Grimoire

Because IndexedDB is origin-scoped, a deployment on a new Vercel origin cannot see data stored by the old Grimoire origin even if the database name is identical.

Formal migration path:
1. Open old Grimoire.
2. Export its JSON backup.
3. Open Grimo Settings → Data (to be wired in the UI milestone).
4. Import the legacy JSON.
5. Import is additive/upsert-only; it does not clear existing rows.
6. Legacy drop rows are deduplicated by `[taskId+dateKey]` rather than their auto-increment IDs.

Do not delete the old production deployment until migration and production acceptance are complete.
