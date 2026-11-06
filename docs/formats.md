# Formats and limits

[Documentation](README.md)

Matroska is the preservation container. Remux commands copy every stream and preserve metadata and chapters where the destination supports them. An incompatible stream causes failure rather than being silently discarded. Remux verification compares codec types and counts and fully decodes audio/video.

H.264/AAC, HEVC/AAC, and VP9/Opus commands produce viewing copies. FFV1/FLAC produces a lossless-codec Matroska copy, but cannot restore information lost in an earlier encode. Transcodes and picture transforms select the first video and all audio streams. They do not retain subtitles, attachments, or additional video tracks. Keep the original or use a compatible remux when those are required.

Every produced media file is probed and fully decoded before publication. Most duration-preserving operations reject a duration change larger than 0.5 seconds or 1 percent, whichever is greater. Decode success does not prove frame-for-frame or pixel-exact equivalence. Lossless archival certification is not implemented.

Trim re-encodes the requested interval. Mute copies the first video stream. Poster exports one frame. Contact sheets sample twelve frames into a 4 by 3 image and need a known source duration. Audio extraction selects the first audio stream. Black, freeze, and silence detection use fixed documented FFmpeg filter thresholds, so their findings require interpretation.

HDR audit reports signaling only. It does not grade HDR or perform tone mapping. Editing subtitle text, disc decryption, HLS/DASH output, downloads, concatenation, stabilization, and optical-flow interpolation are not implemented.
