# video-utils

[![CI](https://github.com/bolens/video-utils/actions/workflows/ci.yml/badge.svg)](https://github.com/bolens/video-utils/actions/workflows/ci.yml)

Remux containers, encode viewing copies, inspect streams, and find picture or audio faults. Batch operations for the life of a video library.

**[Browse the site](https://bolens.github.io/video-utils/)** · [Command catalog](docs/catalog.md) · [Architecture diagram](https://bolens.github.io/video-utils/diagrams/architecture.html)

## Start here

GNU/Linux, Bash 4.3+, and Python 3.11+. See [requirements](docs/requirements.md) for operation-specific dependencies.

```bash
git clone https://github.com/bolens/video-utils.git
cd video-utils
bin/video-utils list
bin/video-utils video-to-h264 --output-dir ./viewing ./masters
# Review the plan, then add --apply to create outputs.
```

37 commands cover conversion, inspection, and library maintenance. Tool directories are thin Bash entry points over a shared Python engine, following the layout and preservation intent of [audio-utils](https://github.com/bolens/audio-utils).

## Working contract

- Writes require `--apply`. `--dry-run` suppresses writes, including report files.
- Sources are retained. Outputs are verified in a temporary directory and published without overwriting existing destinations.
- Inputs can be files or recursive directory trees. Input symlinks are not followed. Filenames travel as arguments, never shell code.
- JSON results go to stdout. Progress and failures go to stderr. Exit codes are 0 success, 1 operation failure, 2 usage or dependency failure.
- `-j 1..32` controls batch concurrency. `--output-dir` preserves relative paths and appends the output suffix to the complete source name.
- The stdio MCP server exposes only read-only tools under explicitly allowed roots.

## Development

```bash
make check
make test
make test-functional
make test-all
make generate
make install-hooks
make -C conversion/video-to-h264 help
```

[Docker](docs/docker.md) · [CLI and configuration](docs/cli.md) · [Formats and limits](docs/formats.md) · [Architecture](docs/architecture.md) · [MCP](docs/mcp.md) · [Tests](tests/README.md) · [Release procedure](docs/releasing.md) · [Contributing](CONTRIBUTING.md)

## Status

Initial 0.1.0 implementation. This is a sibling suite, not a claim of identical feature maturity or codec coverage to audio-utils. The [parity notes](docs/parity.md) explain the implemented conventions and deliberate differences.

[MIT license](LICENSE). External encoders keep their own licenses.

## License scope and attribution

See [third-party notices](THIRD_PARTY_NOTICES.md) for the project license scope,
retained upstream notices, and dependency or asset exceptions.
