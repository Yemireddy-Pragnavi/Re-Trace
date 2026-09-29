# Re-Trace — UI and UX direction

The interface should feel like a focused investigation workspace: calm, deliberate and easy to inspect. Its visual quality should help an evaluator understand the evidence, not distract them from it.

## Visual language

| Element | Direction |
|---|---|
| Base | Charcoal and near-black surfaces, including `#090909` and `#151312` |
| Primary accent | Warm orange, principally `#ff6b2d`; the landing uses a closely related ember orange |
| Text | Warm white `#f5f3ef`, with muted warm-neutral supporting text |
| Success and caution | Semantic green and amber, always paired with readable text |
| Typography | Existing Inter/system sans-serif stack; monospace for hashes, offsets and identifiers |
| Shape | Restrained rounded cards, fine borders, subtle warm glows and clear spacing |
| Icons | Existing Lucide set; meaningful labels accompany unfamiliar actions |

Use the current styles as the starting point. Avoid changing the whole theme to introduce a new page. Do not reintroduce visible SIH/NTRO badges: those were intentionally removed from product screens. The project requirements may still reference the brief in documentation.

## Public landing page

Explain the product in this order: what problem it addresses, the three distinct modules, a short demonstration journey, how accountability works, and the prototype’s boundaries. Give visitors a clear route into the secure workspace and a way to understand it without logging in.

Use concrete language such as “Verify the working copy,” “Inspect recovered artifacts,” and “Review the case timeline.” Avoid “100% secure,” “unrecoverable forever,” “tamper-proof,” or unsupported adoption/certification claims.

Animated light, flowing connections, subtle card movement and section reveals already support the design. Motion should suggest relationships, not simulate jobs or create fake live activity. Retain the landing’s motion pause control and respect reduced-motion settings.

## Login and access request

The access notice explains three steps: organization, authorization and verification. It uses a short headline, three readable cards, a concise evaluator note and an expandable real-world example. Distinguish future physical-device work from the functioning image/copy prototype.

Visitors must be able to close the notice, continue to sign-in, or request access. The request form asks only for their email address. Do not display the administrator’s address in the popup. Explain that the prepared request opens in the visitor’s email app and must be sent there. Do not ask for a password before an access request.

Approved users sign in separately and complete authenticator verification. Keep pending-domain, pending-account and suspended-account messages understandable. Never show an approval badge merely because someone entered a familiar organization suffix.

## Workspace and administration

Keep the Home page link visible. Present an active case before the operator chooses sources or starts work. Drive erasure, file/folder erasure and recovery need distinct entry points; do not collapse them into a generic action button.

For erasure, place the working-copy scope next to confirmation. For recovery, show classification, offset, hash and confidence reasons together. Use expandable details for dense technical evidence rather than hiding the reason behind a score.

Admin Oversight should separate access decisions, case assignments, global activity, job results and available authentication records. Explain paging and refresh behavior. A session record is not a claim that someone is online, and an empty provider log is not evidence that no login attempts occurred.

## Interaction quality

Use short entrance transitions and modest hover elevation. Keep lengthy data tables scrollable on small screens without making the entire page overflow. Native dialog behavior should retain focus, keyboard dismissal and semantic labels. Buttons need clear names; focus states must remain visible.

Always design the empty, loading, error, pending and success states alongside the main path. Browser checks should cover desktop and mobile widths, keyboard navigation, reduced motion, dialog focus, error recovery and long identifiers. Source/build checks alone do not establish visual quality; browser verification is still an open acceptance task.
