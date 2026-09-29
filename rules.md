# Re-Trace — Engineering rules

These conventions help people and AI coding assistants improve the existing project without losing its evidence trail or overstating what it can do. Read [prd.md](prd.md), [architecture.md](architecture.md) and the relevant source before editing. Current explicit user instructions take precedence over this project guidance; ask when a consequential requirement remains ambiguous.

## Keep the product coherent

Work inside the current repository and preserve working routes, the three separate core modules, existing case data and the established charcoal/orange design. Prefer a focused change to a broad rewrite. Do not introduce a new framework, backend service or dependency merely to make a small change easier.

Keep cloud and local behavior explicit. A local test passing is not proof that the deployed Edge Function or browser journey works. Do not weaken a production check to make the demo easier.

## Preserve evidence

- Original uploaded sources remain intact. Sanitization operates on controlled copies.
- Check source and recovered-file hashes at the boundaries where they matter.
- Validate file structure before presenting a candidate as recovered. Record rejection and incomplete-scan conditions honestly.
- Never replace measured outcomes with seeded success indicators or fabricated performance numbers.
- Never describe a browser operation as physical HDD/SSD/NVMe erasure.
- Never turn heuristic confidence into a probability or infer general accuracy from the eight-artifact fixture.

## Enforce access on the server

Cloud case access requires the configured account/domain approval, verified email, active session and MFA checks. UI visibility is not authorization. Keep RLS enabled and review API, RPC and Storage paths together when changing access.

Roles must come from server-controlled data. Do not trust user metadata to authorize access. Do not approve a public email provider or a broad domain suffix as a convenience. Admin changes must preserve an audit record, including before/after values where implemented.

Never put service-role keys, passwords, bearer tokens, private signing keys, MFA secrets or real evidence files in commits or tool output. Do not collect raw biometrics. Public publishable configuration is not a substitute for authorization.

## Change data deliberately

Use versioned migrations for schema changes. Preserve existing rows and review grants and policies before deployment. Test access changes with isolated or rollback-only fixtures. Do not silently reapply migrations to an existing database, reset production data or rewrite historical audit events.

Changing a visible contact address does not authorize changing the administrator account. Account migration, domain approval and privilege changes need an explicit intended identity and scope.

## Make the interface truthful and usable

Show loading, pending approval, denied access, incomplete processing and failure states. Give the user a concrete next step. Keep keyboard focus visible, labels accessible, layouts responsive and decorative motion compatible with reduced-motion preferences.

The access-request form requires only an email. Its current action opens a prepared email; it must not say that a request was delivered automatically. Sign-in remains a separate password/MFA flow.

## Verify the changed risk

| Change | Relevant check |
|---|---|
| Frontend source or navigation | `npm run build --prefix frontend`; inspect affected browser journeys when available |
| Cloud carving or fixture | `npm run test:engines --prefix supabase` |
| Python processing or local API | Run `python -m pytest -q` from `backend` in the configured virtual environment |
| Database authorization | Review and run `supabase/tests/access-policy.sql` with its rollback boundary intact |
| Reports or canonicalization | Check valid signatures/PDF hashes and rejection of altered payloads |

Use installed lockfiles and pinned dependencies. Add tests for meaningful new behavior or a regression risk; avoid tests that merely repeat implementation details. Do not rerun unrelated checks for a prose-only update.

## Leave a reviewable result

Before pushing, read the current remote branch and preserve changes made by others. Keep commits focused, avoid force pushes and state exactly what was tested. Update [tasks.md](tasks.md) when acceptance status changes and [memory.md](memory.md) when a lasting decision changes. A GitHub push, a successful build and a live deployment are three different outcomes; report them separately.
