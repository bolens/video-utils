# Plan: Video preservation and local library tools

The [specification](spec.md) preserves existing behavior. Use the project guide
and constitution for implementation constraints. Keep upstream-managed templates,
helpers, and integration manifests unchanged.

## Source ownership

- `lib/core.py`
- `lib/domain.py`
- `lib/catalog.json`
- `mcp/server.py`
- `scripts/generate.py`
- `tests/test_common.py`
- `tests/test_functional.py`
- `docs/formats.md`

## Constitution check

Preserve explicit local write authority, source retention, no-clobber publication, Python 3.11 compatibility, and the catalog/shared-engine boundary. The original retrofit changed documentation only. The legacy completion pass repairs dependency-status propagation without adding a codec, protocol, write mode, or live service.

## Validation

```sh
make check test-all
```

Run checks in an isolated checkout. Commands are instructions, not evidence of
a pass. Record results in `coverage.md`, keep incomplete work in `tasks.md`, and
follow `RELEASING.md` for reviewed delivery. No live operation is required solely
to create this retrospective baseline.

## Legacy completion audit, 2026-09-06

Map all 37 catalog commands and supporting surfaces. Verify shared core/MCP
contracts against the archive/image peers and separately trace video remux,
transcode, transform, inspection and detector behavior. Specify actual stream
selection, codec settings, duration checks and metadata/fidelity limits.
Repair FR-008 by sharing the script/import module identity and translating a
missing direct detector executable into the same dependency exception. Use real
CLI subprocesses with isolated PATH and a stub probe; never require a real media
file or installed decoder to prove missing-executable handling.
