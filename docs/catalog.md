# Tool catalog

37 commands. Generated from `lib/catalog.json`.

| Command | Category | Mode | Purpose |
|---|---|---|---|
| [`library-inventory`](../util/library/library-inventory/) | library | read | List file sizes and relative paths. |
| [`library-summary`](../util/library/library-summary/) | library | read | Summarize file counts, byte sizes, empty files, and extensions without reading contents. |
| [`library-dupes`](../util/library/library-dupes/) | library | read | Find exact SHA-256 duplicates without deleting files. |
| [`hash-manifest`](../util/library/hash-manifest/) | library | read | Print a JSON SHA-256 manifest for the input tree. |
| [`hash-verify`](../util/library/hash-verify/) | library | read | Verify file presence and hashes against a JSON manifest. |
| [`tree-diff`](../util/library/tree-diff/) | library | read | Compare file hashes and presence against another tree. |
| [`path-audit`](../util/library/path-audit/) | library | read | Report filename portability issues. |
| [`mp4-to-mkv`](../conversion/mp4-to-mkv/) | conversion | write | Copy all streams from MP4 to MKV without re-encoding. |
| [`mov-to-mkv`](../conversion/mov-to-mkv/) | conversion | write | Copy all streams from MOV to MKV without re-encoding. |
| [`avi-to-mkv`](../conversion/avi-to-mkv/) | conversion | write | Copy all streams from AVI to MKV without re-encoding. |
| [`webm-to-mkv`](../conversion/webm-to-mkv/) | conversion | write | Copy all streams from WEBM to MKV without re-encoding. |
| [`ts-to-mkv`](../conversion/ts-to-mkv/) | conversion | write | Copy all streams from TS to MKV without re-encoding. |
| [`mkv-to-mp4`](../conversion/mkv-to-mp4/) | conversion | write | Copy all streams from MKV to MP4 without re-encoding. |
| [`mov-to-mp4`](../conversion/mov-to-mp4/) | conversion | write | Copy all streams from MOV to MP4 without re-encoding. |
| [`video-to-h264`](../conversion/video-to-h264/) | conversion | write | Create an H.264/AAC MP4 viewing copy. |
| [`video-to-hevc`](../conversion/video-to-hevc/) | conversion | write | Create an HEVC/AAC MP4 viewing copy. |
| [`video-to-webm`](../conversion/video-to-webm/) | conversion | write | Create a VP9/Opus WebM viewing copy. |
| [`video-to-ffv1`](../conversion/video-to-ffv1/) | conversion | write | Create an FFV1/FLAC Matroska copy. Does not restore lost quality. |
| [`video-trim`](../util/transform/video-trim/) | transform | write | Re-encode a clip from a start time and duration. |
| [`video-resize`](../util/transform/video-resize/) | transform | write | Fit video inside a bounding box with even dimensions. |
| [`video-mute`](../util/transform/video-mute/) | transform | write | Copy the first video stream without audio. |
| [`video-strip`](../util/transform/video-strip/) | transform | write | Re-encode without global metadata or chapters. |
| [`video-deinterlace`](../util/transform/video-deinterlace/) | transform | write | Apply the yadif deinterlacing filter. |
| [`video-rotate`](../util/transform/video-rotate/) | transform | write | Rotate video 90 degrees clockwise. |
| [`video-audio-extract`](../util/transform/video-audio-extract/) | transform | write | Extract the first audio stream to FLAC. |
| [`video-poster`](../util/transform/video-poster/) | transform | write | Export a PNG frame at a chosen time. |
| [`video-contact-sheet`](../util/transform/video-contact-sheet/) | transform | write | Export twelve sampled frames in a 4 by 3 PNG grid. |
| [`video-metadata`](../util/audit/video-metadata/) | audit | read | Report container, streams, tags, and chapters. |
| [`video-streams`](../util/audit/video-streams/) | audit | read | List stream codec and format details. |
| [`video-chapters`](../util/audit/video-chapters/) | audit | read | List chapter time ranges and titles. |
| [`video-verify`](../util/audit/video-verify/) | audit | read | Decode video and audio streams with errors treated as failures. |
| [`video-subtitle-audit`](../util/audit/video-subtitle-audit/) | audit | read | List subtitle streams and language tags. |
| [`video-audio-audit`](../util/audit/video-audio-audit/) | audit | read | List audio tracks, codecs, and channel layouts. |
| [`video-hdr-audit`](../util/audit/video-hdr-audit/) | audit | read | Report color signaling and HDR side data. |
| [`video-black-detect`](../util/audit/video-black-detect/) | audit | read | Detect black intervals using FFmpeg thresholds. |
| [`video-freeze-detect`](../util/audit/video-freeze-detect/) | audit | read | Detect frozen picture intervals. |
| [`video-silence-detect`](../util/audit/video-silence-detect/) | audit | read | Detect silent intervals in the first audio track. |
