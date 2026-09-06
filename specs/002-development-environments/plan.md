# Implementation plan

Own devenv configuration and lock, adapter/tests, CI, ignores, and developer documentation. Reuse all native checks and functional tests with the pinned FFmpeg tool closure. Preserve runtime source, generated site, and VERSION.

Stage the complete candidate before isolated-checkout tests; they copy tracked files. Verify native devenv and actual Podman, then current-head Docker/macOS and existing runtime CI. Follow protected delivery and post-merge runtime publication verification. Apple execution remains separately unverified.
