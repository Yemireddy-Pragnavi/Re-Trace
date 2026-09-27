# Current repository decision — 27 September 2026

The user chose to retain `tevi87637-ship-it/Re-Trace` as the canonical repository. The latest source is being published there. Use [Vercel deployment instructions](VERCEL-DEPLOYMENT.md). The migration instructions below describe the earlier, superseded plan.

# Open and publish the complete project

The supplied ZIP contains the full frontend, Python backend, Supabase schema and Edge Function source, tests, and VS Code configuration. The destination repository was empty and the connected GitHub account had pull=true, push=false on 25 September 2026; no write or repository transfer was attempted.

## Run with the same Supabase

Extract the ZIP, open Re-Trace in VS Code, then run:

```powershell
cd frontend
Copy-Item .env.example .env
npm ci
npm run dev
```

Open http://localhost:5173. The example configuration uses the existing Supabase project noqdtxwvgqkgrkpsbhpi. Do not rerun migrations, replace keys, or create a new Supabase project. Existing accounts, cases and storage remain there.

## Publish to your empty destination repository

From the extracted Re-Trace root, signed into GitHub as an account with write access:

```powershell
git init -b main
git add .
git commit -m "Import complete Re-Trace project with unified theme and motion"
git remote add origin https://github.com/YPragnavi/Re-Trace.git
git push -u origin main
```

If the destination has acquired commits since this package was prepared, clone it first and copy the source files into that checkout, then commit and push normally. Do not force push. The previous repository is not deleted.

## UI update

Dashboard header: Home page returns to the landing page and retains the session. Login and reset screens: Back to home. All application screens use charcoal, warm neutral text and orange accents. Landing lighting, flowing connections, halo, scan and bloom effects animate; Pause motion stops decorative animation. System reduced-motion preferences disable animation throughout.

Validation: TypeScript and production build passed. Browser visual and signed-in cloud end-to-end checks were not executed for this update. Supabase configuration, data, SQL and Edge Functions were not changed.
