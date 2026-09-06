# Tasks

- [x] Implement locked tools, adapters, CI, and documentation.
- [x] Pass native devenv and actual Podman: 69 tests, no codec skips on Linux.
- [x] Verify native Linux/macOS and Linux Docker checks on the recorded main revision.
- [x] Verify merged source delivery and the applicable main-revision workflows.

## Delivery verification — 2026-09-06

The [development workflow](https://github.com/bolens/video-utils/actions/runs/34033547140) passed on
`b25219b5c8b195a3d80940fff9afdca8294c11e6`. Both native platform jobs ran successfully;
the Linux job also executed and passed the Docker development-image check. All
applicable workflows observed for that main revision completed successfully.

Actual Apple container-engine execution remains unverified. Native macOS devenv
validation does not establish that engine's runtime behavior. Existing live-host
and optional dependency limits still apply. Checkout cleanup remains part of each
task's delivery procedure and is not inferred from CI success.
