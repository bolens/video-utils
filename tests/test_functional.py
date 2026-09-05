import json
import shutil
import subprocess
import unittest
from test_common import Fixture, core


@unittest.skipUnless(
    shutil.which("ffmpeg") and shutil.which("ffprobe"), "missing dependency: FFmpeg"
)
class Video(Fixture):
    def seed(self, suffix="mkv"):
        path = self.inputs / ("space [1]\n." + suffix)
        codec = (
            ["-c:v", "libvpx-vp9", "-c:a", "libopus"]
            if suffix == "webm"
            else ["-c:v", "mpeg4" if suffix == "avi" else "libx264", "-c:a", "aac"]
        )
        subprocess.run(
            [
                "ffmpeg",
                "-v",
                "error",
                "-nostdin",
                "-y",
                "-f",
                "lavfi",
                "-i",
                "testsrc2=size=80x60:rate=12",
                "-f",
                "lavfi",
                "-i",
                "sine=frequency=440:sample_rate=48000",
                "-t",
                "2",
                *codec,
                "-threads",
                "1",
                str(path),
            ],
            check=True,
            env=self.env,
            capture_output=True,
            timeout=60,
        )
        return path

    def test_exclude_corrupt_input_from_applied_batch(self):
        source = self.seed()
        before = core.digest(source)
        ignored = self.file("skip-corrupt.mkv", b"not valid media")
        output = self.work / "selected-output"
        result = json.loads(
            self.cli(
                "video-to-h264",
                "--exclude",
                "skip*",
                "--apply",
                "--output-dir",
                output,
                self.inputs,
            ).stdout
        )
        self.assertEqual(len(result["results"]), 1)
        self.assertEqual(result["results"][0]["status"], "written")
        self.assertEqual(result["failures"], [])
        self.assertEqual(core.digest(source), before)
        self.assertEqual(ignored.read_bytes(), b"not valid media")

    def test_every_conversion(self):
        for tool in core.catalog():
            if tool["category"] != "conversion":
                continue
            with self.subTest(tool=tool["name"]):
                source = self.seed(
                    tool["extensions"][0][1:] if tool["operation"] == "remux" else "mkv"
                )
                target = self.work / (tool["name"] + "." + tool["suffix"])
                self.cli(tool["name"], "--apply", "-o", target, source)
                self.cli("video-verify", target)
                self.assertTrue(source.exists())

    def test_transforms_and_reports(self):
        source = self.seed()
        for tool in core.catalog():
            with self.subTest(tool=tool["name"]):
                if tool["category"] == "transform":
                    target = self.work / (tool["name"] + "." + tool["suffix"])
                    self.cli(
                        tool["name"],
                        "--apply",
                        "--size",
                        "40x30",
                        "--duration",
                        "0.5",
                        "--start",
                        "0",
                        "-o",
                        target,
                        source,
                    )
                    self.assertTrue(target.exists())
                    if tool["operation"] == "mute":
                        streams = json.loads(self.cli("video-streams", target).stdout)[
                            "results"
                        ][0]["result"]
                        self.assertFalse(
                            any(s["codec_type"] == "audio" for s in streams)
                        )
                elif tool["category"] == "audit":
                    self.cli(tool["name"], source)

    def test_dry_run_and_corruption(self):
        source = self.seed()
        out = self.work / "out.mp4"
        self.cli("video-to-h264", "-o", out, source)
        self.assertFalse(out.exists())
        self.cli("video-to-h264", "--apply", "--dry-run", "-o", out, source)
        self.assertFalse(out.exists())
        self.cli("video-to-h264", "--apply", "-o", out, source)
        self.cli("video-to-h264", "--apply", "-o", out, source, code=1)
        broken = self.file("broken.mp4", b"bad video")
        target = self.work / "failed.mp4"
        self.cli("video-verify", broken, code=1)
        self.cli("video-to-h264", "--apply", "-o", target, broken, code=1)
        self.assertFalse(target.exists())

    def test_invalid_time_and_parallel(self):
        source = self.seed()
        self.cli(
            "video-trim", "--start", "nan", "-o", self.work / "out.mkv", source, code=2
        )
        self.seed("mp4")
        out = self.work / "batch"
        self.cli("video-poster", "--apply", "-j", "2", "--output-dir", out, self.inputs)
        self.assertEqual(len(list(out.iterdir())), 2)


if __name__ == "__main__":
    unittest.main()
