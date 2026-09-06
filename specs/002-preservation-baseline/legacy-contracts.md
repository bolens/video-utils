# Legacy capability contracts

Retrospective audit at `4ce0604`, 2026-09-06. This extends [spec.md](spec.md)
with concrete behavior for all 37 existing video/library commands and their
supporting entry points. [Legacy coverage](legacy-coverage.md) maps source and
native acceptance owners.

## Contract authority

The [CLI reference](../../docs/cli.md), [catalog](../../docs/catalog.md),
[format limits](../../docs/formats.md), [requirements](../../docs/requirements.md),
and [MCP guide](../../docs/mcp.md) are normative parts of this specification.
Catalog-generated help remains single-sourced. Existing
[Docker](../002-docker-runtime/spec.md) and
[development](../002-development-environments/spec.md) specifications retain their
scope. This records existing behavior retrospectively; FR-008 is an explicit
corrective requirement, not a claim that missing-dependency reporting already worked.

## Shared execution

- **LC-001, CLI/configuration:** Dispatcher help/list, version, generated command
  wrappers and Make aliases MUST retain the same catalog identities. JSON config
  accepts only `roots` and `jobs`; explicit paths/jobs take precedence. Config and
  path components must not be symlinks. Jobs are integers from 1 to 32, default 1.
  Unknown options/tools and invalid configuration return 2. No input matches
  return failure, including an empty tree. Size requires WIDTHxHEIGHT with dimensions 1–99999. Start is finite and
  nonnegative (default 0 seconds), duration finite and positive (default 10).
  Inherited quality/archive-limit options retain validation but do not change
  the catalog-selected codec settings.
- **LC-002, discovery/exclusions:** Regular-file discovery MUST recurse without
  following symlinks, deduplicate overlapping absolute paths, preserve filename
  bytes through argument arrays, and return stable bytewise path order. Extension
  matching is case-insensitive. Repeated exclusions match case-sensitive relative
  path globs, including newline names; empty patterns are invalid. Exclusions
  filter both tree-comparison sides and full expected/actual manifest sets.

- **LC-003, write planning/publication:** Every writer MUST require an explicit
  output or output directory. Explicit output requires exactly one source;
  output-directory mode appends the catalog suffix to the relative source name.
  Reject duplicate target mappings, existing destinations, source replacements,
  and targets replacing source inputs. Default execution plans writes;
  `--dry-run` overrides `--apply` and suppresses success/failure report writes.
  Applied writes verify private staging before no-clobber publication, retain
  sources, and remove failed staging. Concurrent publishers must have at most
  one winner.
- **LC-004, batches/results:** Bounded worker submission MUST retain at most
  twice the worker count outstanding jobs, preserve result order, and retain
  successful outputs when another source fails. JSON stdout separates results
  and failures; progress belongs on stderr unless quiet. Dependency failures
  return 2, other operation failures 1, successful execution 0. Requested JSON
  reports cannot overwrite existing paths and publication failure must fail the
  run. FR-008 preserves missing-executable status across domain imports.
  Read-only commands reject apply/output options but may write explicitly
  requested reports. Discovery/result memory still grows with input count.

## Video operation contracts

- **LC-005, remux:** The seven catalog remux directions MUST copy every source
  stream and map container metadata/chapters where the destination supports them.
  Five target Matroska; MKV/MOV-to-MP4 target MP4 with faststart. Incompatible
  streams must fail rather than be silently dropped. Verification probes and
  fully decodes output audio/video, comparing ordered stream codec types/names
  and counts. The multi-audio MP4 fixture additionally compares compressed packet
  bytes/order, audio language/default disposition, container title, and retained
  source bytes. This does not certify every timing or metadata convention.
- **LC-006, viewing copies and transforms:** Four transcodes select the first
  video stream and all audio streams, omitting subtitles, attachments and extra
  video tracks. H.264 uses libx264 CRF 20/medium with AAC 192k; HEVC uses libx265
  CRF 24 with AAC; WebM uses VP9 CRF 32/zero target bitrate with Opus; FFV1 uses
  level 3 with FLAC in Matroska. FFV1 cannot restore earlier encoding losses.
  MP4 targets enable faststart. Picture transforms use the default H.264/AAC
  Matroska path: trim re-encodes the selected start/duration; resize fits the
  requested aspect-preserving box with even dimensions and may upscale; strip
  removes metadata/chapters; deinterlace uses yadif; rotate uses clockwise
  transpose. Mute instead copies only the first video, dropping audio. Audio
  extraction encodes the first audio as FLAC. Poster exports one PNG at start;
  contact sheet samples twelve frames into a 4-by-3 PNG with 320-pixel tile width
  and requires known positive duration. All writers currently require a source
  with a non-attached-picture video stream, including audio extraction.
- **LC-007, inspection and detection:** Metadata returns probe format, stream
  and chapter data; stream/chapter commands return their respective arrays.
  Verification fully decodes audio/video and reports stream count. Subtitle/audio
  audits filter stream metadata by type. HDR audit returns signaling fields
  (pixel format, color space/transfer/primaries and side data), not grading or tone
  mapping. Black detection uses first video with `d=0.5:pix_th=0.1`; freeze uses
  first video with `n=-60dB:d=2`; silence uses first audio with `n=-50dB:d=1`.
  They return matching FFmpeg event lines with successful status; findings need
  interpretation. Decoder failures fail, and missing detector executables use
  dependency status under FR-008.
- **LC-008, verification and local boundaries:** Inputs MUST use file/pipe
  protocols and the explicit local demuxer allowlist in `lib/domain.py`; HLS/DASH
  and network downloads are outside the command contract. Subprocess filenames
  use argument arrays. Applied output must contain its expected audio/video
  stream and fully decode before no-clobber publication. Except trim/poster/
  contact-sheet, when both durations are available a difference exceeding the
  greater of 0.5 seconds and 1% fails. Missing duration is not invented. These
  checks are structural integrity evidence, not frame/pixel equivalence or archival
  certification. Missing executables return 2; installed encoders failing or
  unavailable codec support return 1. Restrictions do not sandbox hostile media.
  No package installation, source deletion, disc decryption, subtitle editing,
  concatenation, stabilization or optical-flow interpolation is included.

## Local library operations

- **LC-009, inventory and summary:** `library-inventory` MUST report absolute
  and relative paths and file sizes. `library-summary` reports count, total bytes,
  zero-byte count, min/max sizes and lowercase final-extension groups, treating
  trailing-dot names as extensionless consistently across supported Python
  versions. Summary must not read file contents, hash, or invoke codecs. Empty
  discovery is a failure, rather than a fabricated successful zero-file report.
- **LC-010, duplicates:** `library-dupes` MUST report exact SHA-256 groups with
  at least two files, hashing only files whose sizes have another candidate.
  It neither deletes nor hardlinks files; reported duplicates are data, so their
  presence does not itself change a successful exit status to failure.
- **LC-011, manifests:** `hash-manifest` MUST emit relative names, byte sizes,
  and SHA-256 without ambiguous duplicate relative paths. `hash-verify` accepts
  the documented direct manifest and command-response forms, validates schemas
  and checksums, and compares the complete expected/actual key union. Missing,
  changed, and extra files all fail. Uppercase checksum hex normalizes; malformed,
  unsafe, ambiguous or symlink manifest paths fail. A manifest is only as trusted
  as its independently supplied source.
- **LC-012, tree/path findings:** `tree-diff` MUST compare SHA-256 and presence
  across the full union, reporting left-only/right-only/changed relative names.
  Equal files are omitted and ambiguous left-side relative names fail.
  `path-audit` reports control characters, Windows-reserved punctuation,
  components over 240 filename bytes, and trailing dot/space. It does not rename
  or claim exhaustive cross-platform filename validation. Findings from either
  command are successful structured reports, not operational errors.

## MCP and support surfaces

- **LC-013, MCP:** Local newline-delimited JSON-RPC MUST require existing allowed
  roots at startup, initialize before listing/calling tools, and expose only read
  catalog operations without additional path-bearing arguments. Hash verification
  and tree comparison stay excluded. Calls accept only 1–100 string paths,
  reject symlink components and outside-root paths, ignore user config, and run
  one worker with no report paths. Notifications receive no response. Preserve
  the documented protocol negotiation, 1 MiB input and 4 MiB serialized-result
  limits, JSON-only stdout, tool `isError` and JSON-RPC error distinctions.
  Result limits apply after execution. No HTTP, authentication, cancellation,
  arbitrary argument forwarding, write mode, or background tasks are implied.
- **LC-014, maintenance/site:** Catalog generation MUST keep wrappers, tool
  Makefiles, command references and the static site synchronized. Browser search
  combines case-insensitive text with exact category selection and updates the
  count/empty state. Theme toggling retains a stored valid light/dark preference
  or the default dark theme, tolerating storage denial. Copying the preview
  command reports clipboard failure and offers manual selection. These controls
  and diagrams do not gain access to media. Existing site/link/accessibility/responsive checks and Pages
  deployment gates remain part of delivery. Architecture diagram sources and
  their evidence are maintained separately from generated catalog output.
  Test fixtures, native codec notices, repository checks, hooks and Spec Kit
  updater templates are supporting contracts, not untracked runtime features.

Changes to existing behavior must update these contracts and the relevant native
fixtures together. New features require their own prospective specification.
