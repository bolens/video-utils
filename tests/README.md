# Tests

`make test` runs shared CLI, publication, filename, configuration, and MCP tests.
`make test-functional` runs real domain operations on generated fixtures.
`make test-all` runs both tiers and repository-validation tests. Tests use disposable fixtures. CLI subprocesses receive isolated HOME, XDG config/state/cache/data/runtime paths, and TMPDIR values. Fixture encoders use the same environment.

Video tests exercise container remuxing, encoders, transforms, stream reports, corruption, and parallel poster generation.

Without either `ffmpeg` or `ffprobe`, the video functional suite is skipped. Missing encoders cause failures when their fixture or operation runs. The unittest report names every skip. CI installs the core dependencies and retains the report as an artifact. Tests require no personal media and perform no network enrichment.

Shared regression tests also cover direct manifest-response round trips, malformed and ambiguous manifests, size-filtered duplicate hashing, and bounded batch submission with stable result ordering.

Summary tests cover extension grouping, zero-byte files, overlapping roots, symlink exclusion, write refusal, MCP access, and operation without reading contents or invoking codecs.

Exclusion tests cover repeated and case-sensitive patterns, relative paths, multiline names, both comparison roots, full manifest filtering, write plans, and folder-packing refusal.

Publication checks cover writer failure, missing output, rejected verification, sync/link failures, existing destinations, and two concurrent publishers. They assert that failed outputs stay unpublished and staging files are removed.

Mixed valid/corrupt batches run with one and two workers. Functional checks verify successful output, source retention, absent failed output, nonzero exit status, and matching success/failure reports. These cases run in the existing `make test` and `make test-functional` tiers, and together in `make test-all`.

A two-audio-track MP4 remux fixture checks every compressed packet payload and per-stream packet order, stream codecs/counts, audio language/default flags, a container title, and unchanged source bytes. These checks do not certify every container metadata field or timing convention.
