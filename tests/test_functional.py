from pathlib import Path
import json
import shutil
import subprocess
import unittest
from test_common import Fixture, core


@unittest.skipUnless(
    shutil.which("ffmpeg") and shutil.which("ffprobe"), "missing dependency: FFmpeg"
)
class Video(Fixture):
    def test_remux_preserves_all_packet_payloads_and_audio_languages(self):
        source = self.inputs / "two tracks [1]\n.mp4"
        subprocess.run(
            ["ffmpeg", "-v", "error", "-nostdin", "-f", "lavfi", "-i",
             "testsrc2=size=32x24:rate=10", "-f", "lavfi", "-i",
             "sine=frequency=440:sample_rate=48000", "-f", "lavfi", "-i",
             "sine=frequency=880:sample_rate=48000", "-map", "0:v", "-map",
             "1:a", "-map", "2:a", "-t", "1", "-c:v", "libx264",
             "-threads", "1", "-c:a", "aac", "-metadata", "title=Preserved title",
             "-metadata:s:a:0", "language=eng", "-metadata:s:a:1", "language=fra",
             "-disposition:a:0", "default", "-disposition:a:1", "0", str(source)],
            check=True, capture_output=True, env=self.env, timeout=60,
        )
        original = source.read_bytes()
        target = self.work / "remuxed.mkv"
        self.cli("mp4-to-mkv", "--apply", "-o", target, source)

        def inspect(path):
            return json.loads(subprocess.run(
                ["ffprobe", "-v", "error", "-show_streams", "-show_format",
                 "-show_packets", "-show_data_hash", "sha256", "-of", "json", str(path)],
                check=True, capture_output=True, env=self.env, timeout=30,
            ).stdout)

        before, after = inspect(source), inspect(target)
        expected_streams = [("video", "h264"), ("audio", "aac"), ("audio", "aac")]
        for data in (before, after):
            self.assertEqual([(s["codec_type"], s["codec_name"])
                              for s in data["streams"]], expected_streams)
            self.assertEqual([s.get("tags", {}).get("language") for s in data["streams"][1:]],
                             ["eng", "fra"])
            self.assertEqual([s["disposition"]["default"] for s in data["streams"][1:]],
                             [1, 0])
            self.assertEqual(data["format"].get("tags", {}).get("title"), "Preserved title")
        for index in range(3):
            with self.subTest(stream=index):
                packets = [[(p["size"], p["data_hash"]) for p in data["packets"]
                            if p["stream_index"] == index] for data in (before, after)]
                self.assertTrue(packets[0])
                self.assertEqual(packets[1], packets[0])
        self.assertEqual(source.read_bytes(), original)

    def test_mixed_batch_preserves_success_and_reports_failure(self):
        source = self.seed().rename(self.inputs / "zz-good.mkv")
        corrupt = self.file("00-corrupt.mkv", b"invalid input")
        before = {path: path.read_bytes() for path in (source, corrupt)}
        for jobs in (1, 2):
            with self.subTest(jobs=jobs):
                output = self.work / ("batch-" + str(jobs))
                success_log = self.work / ("success-" + str(jobs) + ".json")
                failure_log = self.work / ("failure-" + str(jobs) + ".json")
                response = json.loads(self.cli(
                    "video-mute", "--apply", "-j", jobs, "--output-dir", output,
                    "-S", success_log, "-L", failure_log, self.inputs, code=1,
                ).stdout)
                self.assertEqual([r["path"] for r in response["results"]], [str(source)])
                self.assertEqual([r["path"] for r in response["failures"]], [str(corrupt)])
                self.assertEqual(response["results"][0]["status"], "written")
                self.assertEqual(response["failures"][0]["status"], "failed")
                self.assertEqual(json.loads(success_log.read_text()), response["results"])
                self.assertEqual(json.loads(failure_log.read_text()), response["failures"])
                published = Path(response["results"][0]["output"])
                self.cli("video-verify", published)
                self.assertFalse(Path(response["failures"][0]["output"]).exists())
                self.assertEqual(list(output.iterdir()), [published])
                for path, original in before.items():
                    self.assertEqual(path.read_bytes(), original)

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
