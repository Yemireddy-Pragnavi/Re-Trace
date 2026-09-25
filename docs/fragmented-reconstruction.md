# Fragmented-file reconstruction roadmap

**Not implemented.** Current recovery requires contiguous bytes. A candidate that fails validation is listed as rejected; it is not silently labeled recovered.

1. Build a reproducible ground-truth dataset with known two-fragment and multi-fragment files, reordered blocks, missing blocks, decoys and mixed file types. Preserve source and expected output hashes.
2. Implement a read-only block inventory and per-format constraints: PNG chunk lengths/CRCs, JPEG restart/marker consistency, ZIP central-directory offsets and PDF object references.
3. Generate a bounded candidate adjacency graph. Limit candidate counts, file sizes, reconstruction depth, memory and CPU time.
4. Score candidate joins using structural consistency; expose ambiguity rather than force a reconstruction. Require successful parser validation and independent hash comparison for benchmark success.
5. Save fragment offsets, ordering, rejected alternatives, confidence explanation, code version and source hash as evidence provenance. Never modify the source image.
6. Measure precision, recall, false positives, reconstructed-byte accuracy, resource usage and runtime across the generated test corpus.
7. Add a separately labeled experimental recovery mode only after these tests exist. Present uncertain output as a candidate, not evidentially verified recovery.

A future native agent must provide media enumeration, capability checks, explicit device identity confirmation, privilege separation, write protection for recovery, local consent for destructive operations and independent hardware validation. The browser must never imply it directly controls raw devices.
