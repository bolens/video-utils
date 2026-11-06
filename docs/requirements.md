# Requirements

[Documentation](README.md)

GNU/Linux, Bash 4.3+, Python 3.11+, and GNU Make for development shortcuts. No third-party Python packages are used. Python 3.11 and 3.14 run in CI. ShellCheck is required for `make check`.

Video operations require `ffmpeg` and `ffprobe`. Encoders include libx264, libx265, libvpx-vp9, libopus, AAC, FFV1, FLAC, and PNG. Use `ffmpeg -encoders` to inspect your build. Missing encoders are operation failures. Library hashing and inventory need only Python.

Install FFmpeg with the required encoders, plus Python, Make, and ShellCheck for development checks. ImageMagick is not required.

FFmpeg processes local media files. Keep FFmpeg and its codecs maintained. Input protocols and demuxers are restricted to supported local formats. These restrictions do not sandbox the media parser.

No automatic downloads, network enrichment, telemetry, package installation, or source deletion happens when running commands.

## Development checkouts

The checkout folder may be renamed or contain spaces and Unicode. CLI identity
and the default configuration directory remain `video-utils`. Git is required
for the disposable-checkout regression tests; normal media commands do not
require Git. Tests copy only tracked source and isolate HOME/XDG/TMPDIR state.

## Docker

The [Docker guide](docker.md) describes the packaged runtime and its limits.
