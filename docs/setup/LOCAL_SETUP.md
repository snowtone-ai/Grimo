# Local setup

1. Install **Node.js 24 LTS**.
2. Clone `snowtone-ai/Grimo` and open the repository root.
3. Run `corepack enable`.
4. Run `pnpm install`. The first successful install creates `pnpm-lock.yaml`; commit that lockfile before normal development.
5. Copy `.env.example` to `.env.local` and enter the existing values for `NEXT_PUBLIC_GOOGLE_CLIENT_ID` and `GEMINI_API_KEY`. Never commit `.env.local`.
6. Run `pnpm context:check`.
7. Run `pnpm verify`.
8. Run `pnpm dev` and open `http://localhost:3000`.

Expected initial routes: `/` redirects from the startup preference; `/tasks`, `/grimo`, `/calendar`, `/settings` render the Foundation shell.
