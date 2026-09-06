# Legacy implementation coverage

Audit at `4ce0604`, 2026-09-06. All 37 catalog entries are mapped below.
[Legacy contracts](legacy-contracts.md) supplies the acceptance rules; generated
[CLI references](../../docs/cli.md) retain exact options. LC-001–004 apply to every
CLI command, LC-008 to domain video operations, and LC-013 to the restricted MCP
subset. Fixture links identify acceptance owners; they do not certify arbitrary
codecs, metadata or frame-perfect preservation.

| Tool | Contract | Implementation | Acceptance fixtures |
| --- | --- | --- | --- |
| `library-inventory` | LC-009 | [lib/core.py](../../lib/core.py) | [tests/test_common.py](../../tests/test_common.py) |
| `library-summary` | LC-009 | [lib/core.py](../../lib/core.py) | [tests/test_common.py](../../tests/test_common.py) |
| `library-dupes` | LC-010 | [lib/core.py](../../lib/core.py) | [tests/test_common.py](../../tests/test_common.py) |
| `hash-manifest` | LC-011 | [lib/core.py](../../lib/core.py) | [tests/test_common.py](../../tests/test_common.py) |
| `hash-verify` | LC-011 | [lib/core.py](../../lib/core.py) | [tests/test_common.py](../../tests/test_common.py) |
| `tree-diff` | LC-012 | [lib/core.py](../../lib/core.py) | [tests/test_common.py](../../tests/test_common.py) |
| `path-audit` | LC-012 | [lib/core.py](../../lib/core.py) | [tests/test_common.py](../../tests/test_common.py) |
| `mp4-to-mkv` | LC-005 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `mov-to-mkv` | LC-005 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `avi-to-mkv` | LC-005 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `webm-to-mkv` | LC-005 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `ts-to-mkv` | LC-005 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `mkv-to-mp4` | LC-005 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `mov-to-mp4` | LC-005 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `video-to-h264` | LC-006 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `video-to-hevc` | LC-006 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `video-to-webm` | LC-006 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `video-to-ffv1` | LC-006 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `video-trim` | LC-006 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `video-resize` | LC-006 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `video-mute` | LC-006 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `video-strip` | LC-006 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `video-deinterlace` | LC-006 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `video-rotate` | LC-006 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `video-audio-extract` | LC-006 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `video-poster` | LC-006 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `video-contact-sheet` | LC-006 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `video-metadata` | LC-007 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `video-streams` | LC-007 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `video-chapters` | LC-007 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `video-verify` | LC-007 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `video-subtitle-audit` | LC-007 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `video-audio-audit` | LC-007 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `video-hdr-audit` | LC-007 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `video-black-detect` | LC-007 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `video-freeze-detect` | LC-007 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `video-silence-detect` | LC-007 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |

## Supporting surfaces

| Contract | Source owner | Acceptance owner and limits |
| --- | --- | --- |
| LC-001–004 / FR-008 | [Dispatcher](../../bin/video-utils), [core](../../lib/core.py), [catalog](../../lib/catalog.json), generated wrappers/Makefiles | [Common tests](../../tests/test_common.py): missing executables across domain/direct detector calls, planning, config, discovery/exclusions, reports, publication races and bounded workers; [checkout tests](../../tests/test_checkout_portability.py) cover renamed/Unicode directories. |
| LC-005–008 | [Domain engine](../../lib/domain.py) | [Functional tests](../../tests/test_functional.py): all conversion commands, multi-audio packet/metadata remux, transforms, reports, mixed batches, corrupt-input non-publication, output collisions, invalid times and parallel posters. |
| LC-013 | [MCP server](../../mcp/server.py) | MCP fixtures in [common tests](../../tests/test_common.py): read-only selection, allowed-root enforcement, protocol/input validation and refusal of extra arguments. |
| LC-014 | [Generator](../../scripts/generate.py), [checker](../../scripts/check.py), [Make rules](../../lib/tool.mk), [site](../../site/), [architecture data](../../docs/diagrams/architecture.json) | `make check` verifies generated drift, syntax, links, wrapper lint and action pins; [repository tests](../../tests/test_repository_checks.py) exercise the checker. [Browser evidence](../../docs/evidence/README.md) remains separate from media fixtures. |
| Existing Docker/development specs | [Dockerfile](../../Dockerfile), [Docker fixtures](../../scripts/test-docker.py), [development launcher](../../scripts/development-container.py), locked devenv files | [Docker spec](../002-docker-runtime/spec.md), [development spec](../002-development-environments/spec.md), [launcher tests](../../tests/test_development_container.py). Container validation uses disposable inputs. |
| Delivery/governance | [Workflows](../../.github/workflows/), [hooks](../../.githooks/), [playbook](../../RELEASING.md), [Spec Kit](../../.specify/) | Native and hosted checks, protected squash merge, main CI/Pages and GHCR digest verification. Installed integration templates alone do not prove feature completion. |

New commands or changed behavior must update their owning contract and fixtures.
Execution results and limitations belong in [coverage](coverage.md) and the PR.
