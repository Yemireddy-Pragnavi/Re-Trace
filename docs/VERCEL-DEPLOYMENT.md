# Deploy the current Re-Trace version

Use repository **tevi87637-ship-it/Re-Trace**, branch **main**.

## Vercel project settings

- Root Directory: `frontend`
- Framework Preset: `Vite`
- Install Command: `npm ci`
- Build Command: `npm run build`
- Output Directory: `dist`
- Node.js: 22.x

Keep `frontend/vercel.json`; it rewrites application routes to index.html so /login, /app/admin and password-reset links work on reload.

Production builds now default to the existing cloud backend even when Vercel has no VITE variables. The committed fallback URL and publishable key are public client configuration. A service-role key must never be placed in the frontend.

If you already set environment variables, confirm these values in Production (and Preview if used):

```
VITE_RUNTIME=cloud
VITE_SUPABASE_URL=https://noqdtxwvgqkgrkpsbhpi.supabase.co
VITE_SUPABASE_PUBLISHABLE_KEY=sb_publishable_9sro6BlSGp9C4QIppNbzZQ_pXG0SzDw
```

Remove or correct any `VITE_RUNTIME=local` override. VITE values are embedded at build time: changing them requires a new deployment. NEXT_PUBLIC variables are not used by this Vite application.

Deploy the newest main-branch commit. If Vercel is connected to another repository, reconnect/import this canonical repository. Do not redeploy an older commit. After a successful deployment, hard-refresh /login. It should show the charcoal/orange **Sign in to your workspace** interface, not the cyan **Local development workspace** interface.

## Existing backend

The cloud backend is the already deployed Supabase retrace-api Edge Function, PostgreSQL, Auth and private Storage. Vercel hosts the frontend. The Python backend is only for the separate local development mode; it is not required for this cloud deployment. Do not reset Supabase or reapply the existing migrations to the existing project.

For email verification and password reset, the project owner should add the actual Vercel /login and /reset-password URLs to Supabase Auth's redirect allowlist. For the currently supplied domain these are:

- https://re-trace-niil.vercel.app/login
- https://re-trace-niil.vercel.app/reset-password

The initial admin is tevi87637@gmail.com; use the existing password, complete authenticator MFA, then open Admin Oversight. Domain and individual approval are still required for other users. No Supabase configuration or data was changed by this GitHub publication.

Validation: latest frontend passes TypeScript and Vite production build with the cloud environment values deliberately blank, exercising the public production fallback. Live Vercel deployment and browser login verification are not performed by this source publication.

Vercel's Vite SPA routing reference: https://vercel.com/docs/frameworks/frontend/vite#using-vite-to-make-spas
