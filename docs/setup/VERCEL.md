# Vercel setup

Updated 2026-09-13.

1. Open Vercel Dashboard.
2. Click **Add New… → Project** (the UI may also show **New Project**).
3. Under Git repositories, find `snowtone-ai/Grimo` and click **Import**.
4. Framework Preset should detect **Next.js**.
5. Keep Root Directory at repository root.
6. Under **Environment Variables**, add:
   - `NEXT_PUBLIC_GOOGLE_CLIENT_ID`
   - `GEMINI_API_KEY`
7. Add values for **Production**. Add them to Preview/Development only when those environments must exercise the integrations.
8. Click **Deploy**.
9. After the production URL exists, add its exact origin to the Google OAuth client's **Authorized JavaScript origins**, then redeploy/test auth.

Vercel currently supports Node.js 24.x and uses it as the current default for new projects. This repo declares Node 24 so local/CI/production stay aligned.

Changing environment variables on Vercel affects new deployments; redeploy after changes.
