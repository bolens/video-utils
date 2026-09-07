# Documentation

Video stream handling, verified output, and generated command contracts.

## Start here

| Need | Owning document |
| --- | --- |
| Use the project | [README.md](../README.md) |
| Change the repository | [AGENTS.md](../AGENTS.md) |
| Deliver or recover | [RELEASING.md](../RELEASING.md) |
| Plan substantial changes | [.specify/memory/project-guide.md](../.specify/memory/project-guide.md) |
| Non-negotiable constraints | [.specify/memory/constitution.md](../.specify/memory/constitution.md) |

## Architecture

[Architecture](architecture.md) owns the shared engine and ffmpeg boundary. The
[catalog](../lib/catalog.json) generates wrappers and command references. Stream selection, remux
versus transcode, metadata, and verification depend on the selected operation. Keep local protocol
and demuxer restrictions intact.

## Deployment and recovery

[Requirements](requirements.md) owns codec availability. [Container usage](docker.md) owns mounts
and invocation. [RELEASING.md](../RELEASING.md) owns source, Pages, and container delivery.
Regenerate catalog-derived surfaces through the existing generator.

## Database and state

There is no application database. Original media stays intact and publication must not overwrite
existing files. [CLI behavior](cli.md) owns explicit writes and output rules. [MCP](mcp.md) is
restricted to read-only operations within configured roots. Reports do not substitute for verified
output media.

## Documentation maintenance

Keep decisions, invariants, failure modes, and recovery requirements in the owning document. Link to
commands, defaults, schemas, and generated catalogs instead of copying them. Change the owner and
affected references together. Update this index when adding or moving a guide, and verify relative
links and heading anchors. Historical specs and audits describe their recorded revision, not current
runtime proof. A topic without an implementation stays explicitly unimplemented.

## Topic guides

- [Contributing](../CONTRIBUTING.md)
- [Architecture](architecture.md)
- [Tool catalog](catalog.md)
- [CLI contract](cli.md)
- [Development environments](development-environments.md)
- [Docker](docker.md)
- [Formats and limits](formats.md)
- [MCP server](mcp.md)
- [Relationship to audio-utils](parity.md)
- [Release procedure](releasing.md)
- [Requirements](requirements.md)

- [Editor setup](../.vscode/README.md)
- [License scope and attribution](../THIRD_PARTY_NOTICES.md)
- [Development container](../.devcontainer/README.md)
