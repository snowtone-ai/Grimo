# Google Cloud setup for Grimo

Verified against current Google Workspace web-app quickstarts on 2026-09-13. Grimo reuses the existing OAuth client if possible; it does **not** require a client secret in the browser.

## 1. Select the existing Cloud project
1. Open **Google Cloud Console**.
2. Click the project selector in the top bar.
3. Select the same project currently used by Grimoire.

Creating another project is unnecessary when the existing client/API configuration is still valid.

## 2. Ensure APIs are enabled
For each API:
1. Open **Navigation menu → APIs & Services → Library**.
2. Search **Gmail API** → open it → click **Enable** if the page shows Enable.
3. Search **Google Calendar API** → open it → click **Enable** if needed.

## 3. Check Google Auth Platform
1. Open **Navigation menu → Google Auth Platform → Branding**.
2. If Google says the platform is not configured, click **Get Started**.
3. **App Information → App name:** `Grimo`.
4. Choose the **User support email** → **Next**.
5. **Audience:** for a personal/non-Workspace account use **External**. `Internal` is only available/appropriate for a Google Workspace organization whose users alone will use the app.
6. Enter the contact email → accept the Google API Services User Data Policy → continue/create.

If the project is already configured, edit Branding/Audience rather than creating another OAuth setup.

## 4. Test-user access when Audience is External + Testing
1. Open **Google Auth Platform → Audience**.
2. Find **Test users**.
3. Click **Add users**.
4. Add the Google account that will use Grimo.
5. Save.

Keep the app in Testing while it is personal development. Do not start verification/public publishing merely to develop Grimo.

## 5. Confirm only the required scopes
Open **Google Auth Platform → Data Access** and confirm Grimo requests only:
- `https://www.googleapis.com/auth/gmail.readonly`
- `https://www.googleapis.com/auth/calendar.readonly`

Do not add write scopes unless a later product decision explicitly requires them.

## 6. Reuse or create the Web OAuth client
1. Open **Google Auth Platform → Clients**.
2. Prefer the existing Web client used by Grimoire; open it.
3. If none exists, click **Create Client** → **Application type → Web application** → Name `Grimo Web`.
4. Under **Authorized JavaScript origins**, click **Add URI** and add:
   - `http://localhost:3000`
   - the final Vercel production origin, e.g. `https://<project>.vercel.app`
5. Save/Create.
6. Copy the **Client ID**. A Web client secret is not used by Grimo's GIS browser token flow.

Do not add arbitrary Vercel preview domains: OAuth JavaScript origins are exact origins, not a wildcard. Add a preview origin only when you intentionally use Google integration on that preview.

## 7. Local environment
Create `.env.local` (never commit it):
```env
NEXT_PUBLIC_GOOGLE_CLIENT_ID=<Web OAuth Client ID>
GEMINI_API_KEY=<existing Gemini key>
```

Restart `pnpm dev` after changing environment variables.
