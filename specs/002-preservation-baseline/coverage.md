# Requirement coverage

| Requirement | Source and acceptance evidence |
| --- | --- |
| FR-001 | `lib/catalog.json`, `scripts/generate.py`, and `scripts/check.py` generated-drift checks. |
| FR-002 | `lib/core.py:execute` and `publish`; `tests/test_common.py` covers failed writers/verifiers, publication races, cleanup, and preserved existing files. |
| FR-003 | `lib/core.py:discover` and `execute`; common filename, exclusion, collision, and mixed-batch tests. |
| FR-004 | `lib/domain.py:INPUT`, `probe`, `decode`, and `write`; functional tests compare compressed packet payloads, stream order, codecs, languages, and dispositions. |
| FR-005 | `lib/core.py:common`, catalog read operations, manifest-response round trips, no-content-read summary tests, and comparison tests. |
| FR-006 | `mcp/server.py`, allowed-root/initialize/request validation tests in `tests/test_common.py`. |
| FR-007 | `lib/core.py:ordered_work` and `execute`; common scheduling tests and mixed valid/corrupt functional batches with one and two workers. |

## Verification receipt

On 2026-09-05, `make check test-all` passed 64 tests with no failures or skips against the inspected base. `make check` also passed after adding this baseline. A separate self-review traced catalog generation, dry-run authority, discovery, staged verification and publication, batch failures, and MCP restrictions through the named source and test assertions. No unresolved requirement gap was found within this baseline. This proves the named fixture contracts, not every possible media file or external parser implementation. Hosted checks and delivery are recorded in the PR.

## Legacy completion receipt, 2026-09-06

[Legacy contracts](legacy-contracts.md) and [37-tool coverage](legacy-coverage.md)
map all seven remuxes, four transcodes, nine transform/extraction outputs, ten
inspection/detection tools, seven shared library tools and their support surfaces.
The detailed mapping distinguishes stream-copy from re-encoding, metadata limits,
fixed detection thresholds, structural verification and preservation evidence.

FR-008 is owned by `lib/core.py` module identity and `lib/domain.py` detector error
translation. The two missing-executable tests in `tests/test_common.py` use real
CLI subprocesses with isolated PATH and a synthetic probe. Inspection/applied
conversion without ffprobe and verification/all three detectors without ffmpeg
returned the wrong dependency classification before the fix. They now return 2,
retain sources, and publish no output; dry-run planning remains available.

`make check test-all` passed all 71 tests with zero skips, including all conversions,
packet/metadata remux preservation, transforms/reports, partial batches, invalid
times, parallel posters, MCP and publication races. Syntax, ShellCheck, generated
drift, local links and action pins passed. Shared core/MCP source comparison
confirmed the same import-boundary cause as Image Utils; Archiving Utils already
shared its CLI exception identity.

Separate self-review checked both module and direct-subprocess paths, retained
operation status for codec/data failures, complete catalog mapping, local protocol
restrictions, and output verification limits. No independent reviewer was used.
No personal media, live service, generated site or version release was involved.
Candidate/main CI and exact published GHCR digest checks remain delivery gates
recorded by the PR.
