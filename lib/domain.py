"""Local container conversion and video inspection with full decode checks."""

import json
from core import publish, run

INPUT = [
    "-protocol_whitelist",
    "file,pipe",
    "-format_whitelist",
    "mov,matroska,webm,avi,mpeg,mpegts,flv,ogg,asf,gif,image2",
]


def probe(path):
    return json.loads(
        run(
            [
                "ffprobe",
                "-v",
                "error",
                *INPUT,
                "-show_format",
                "-show_streams",
                "-show_chapters",
                "-of",
                "json",
                str(path),
            ]
        )
    )


def decode(path):
    run(
        [
            "ffmpeg",
            "-v",
            "error",
            "-xerror",
            "-nostdin",
            *INPUT,
            "-i",
            str(path),
            "-map",
            "0:v?",
            "-map",
            "0:a?",
            "-f",
            "null",
            "-",
        ]
    )


def inspect(tool, source, args):
    op = tool["operation"]
    data = probe(source)
    if op == "metadata":
        return data
    if op == "streams":
        return data.get("streams", [])
    if op == "chapters":
        return data.get("chapters", [])
    if op == "verify":
        decode(source)
        return {"verified": True, "streams": len(data.get("streams", []))}
    if op == "subtitle-audit":
        return [s for s in data.get("streams", []) if s.get("codec_type") == "subtitle"]
    if op == "audio-audit":
        return [s for s in data.get("streams", []) if s.get("codec_type") == "audio"]
    if op == "hdr-audit":
        return [
            {
                k: s.get(k)
                for k in (
                    "index",
                    "pix_fmt",
                    "color_space",
                    "color_transfer",
                    "color_primaries",
                    "side_data_list",
                )
            }
            for s in data.get("streams", [])
            if s.get("codec_type") == "video"
        ]
    filters = {
        "black-detect": "blackdetect=d=0.5:pix_th=0.1",
        "freeze-detect": "freezedetect=n=-60dB:d=2",
        "silence-detect": "silencedetect=n=-50dB:d=1",
    }
    if op in filters:
        import subprocess

        flag = "-af" if op == "silence-detect" else "-vf"
        stream = "0:a:0" if op == "silence-detect" else "0:v:0"
        result = subprocess.run(
            [
                "ffmpeg",
                "-hide_banner",
                "-nostdin",
                *INPUT,
                "-i",
                str(source),
                "-map",
                stream,
                flag,
                filters[op],
                "-f",
                "null",
                "-",
            ],
            capture_output=True,
            timeout=3600,
            check=False,
        )
        if result.returncode:
            raise RuntimeError(result.stderr.decode("utf-8", "replace")[-4000:])
        marker = {
            "black-detect": "black_start:",
            "freeze-detect": "freezedetect",
            "silence-detect": "silence_",
        }[op]
        return {
            "events": [
                line
                for line in result.stderr.decode("utf-8", "replace").splitlines()
                if marker in line
            ]
        }
    raise ValueError("unsupported operation: " + op)


def write(tool, source, target, args):
    op = tool["operation"]
    before = probe(source)
    videos = [
        s
        for s in before["streams"]
        if s.get("codec_type") == "video"
        and not s.get("disposition", {}).get("attached_pic")
    ]
    if not videos:
        raise ValueError("input has no video stream")
    options = [
        "-map",
        "0:v:0",
        "-map",
        "0:a?",
        "-map_metadata",
        "0",
        "-map_chapters",
        "0",
    ]
    codec = [
        "-c:v",
        "libx264",
        "-crf",
        "20",
        "-preset",
        "medium",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
    ]
    mux = tool.get("mux", "matroska")
    if op == "remux":
        options = ["-map", "0", "-map_metadata", "0", "-map_chapters", "0"]
        codec = ["-c", "copy"]
    elif op == "transcode":
        if tool.get("codec") == "vp9":
            codec = ["-c:v", "libvpx-vp9", "-crf", "32", "-b:v", "0", "-c:a", "libopus"]
        elif tool.get("codec") == "ffv1":
            codec = ["-c:v", "ffv1", "-level", "3", "-c:a", "flac"]
        elif tool.get("codec") == "hevc":
            codec = ["-c:v", "libx265", "-crf", "24", "-c:a", "aac"]
    elif op == "trim":
        options += ["-ss", str(args.start), "-t", str(args.duration)]
    elif op == "resize":
        w, h = args.size.split("x")
        options += [
            "-vf",
            f"scale={w}:{h}:force_original_aspect_ratio=decrease:force_divisible_by=2",
        ]
    elif op == "mute":
        options = ["-map", "0:v:0", "-map_metadata", "0", "-map_chapters", "0", "-an"]
        codec = ["-c:v", "copy"]
    elif op == "strip":
        options += ["-map_metadata", "-1", "-map_chapters", "-1"]
    elif op == "deinterlace":
        options += ["-vf", "yadif"]
    elif op == "rotate":
        options += ["-vf", "transpose=1"]
    elif op == "audio-extract":
        options = ["-map", "0:a:0", "-vn"]
        codec = ["-c:a", "flac"]
    elif op in ("poster", "contact-sheet"):
        options = ["-map", "0:v:0", "-an", "-ss", str(args.start)]
        if op == "contact-sheet":
            duration = float(before.get("format", {}).get("duration", 0))
            if duration <= 0:
                raise ValueError("contact sheet requires a known duration")
            options += ["-vf", f"fps=12/{duration},scale=320:-1,tile=4x3"]
        options += ["-frames:v", "1", "-update", "1"]
        codec = ["-c:v", "png"]
    else:
        raise ValueError("unsupported operation: " + op)
    if mux == "mp4":
        options += ["-movflags", "+faststart"]

    def writer(temp):
        run(
            [
                "ffmpeg",
                "-v",
                "error",
                "-xerror",
                "-nostdin",
                "-n",
                *INPUT,
                "-i",
                str(source),
                *options,
                *codec,
                "-threads",
                "1",
                "-f",
                mux,
                str(temp),
            ]
        )

    def verify(temp):
        # Output formats are generated locally, so allow the audio-only extraction too.
        data = json.loads(
            run(
                [
                    "ffprobe",
                    "-v",
                    "error",
                    "-show_streams",
                    "-show_format",
                    "-of",
                    "json",
                    str(temp),
                ]
            )
        )
        kind = "audio" if op == "audio-extract" else "video"
        if not any(s.get("codec_type") == kind for s in data.get("streams", [])):
            raise ValueError("output is missing expected stream")
        run(
            [
                "ffmpeg",
                "-v",
                "error",
                "-xerror",
                "-nostdin",
                "-i",
                str(temp),
                "-map",
                "0:v?",
                "-map",
                "0:a?",
                "-f",
                "null",
                "-",
            ]
        )
        if op == "remux":
            a = [(s["codec_type"], s.get("codec_name")) for s in before["streams"]]
            b = [(s["codec_type"], s.get("codec_name")) for s in data["streams"]]
            if a != b:
                raise ValueError("remux changed stream codecs or count")
        if op not in ("trim", "poster", "contact-sheet"):
            old = float(before.get("format", {}).get("duration", 0))
            new = float(data.get("format", {}).get("duration", 0))
            if old and new and abs(old - new) > max(0.5, old * 0.01):
                raise ValueError("output duration differs unexpectedly")

    publish(target, writer, verify)
