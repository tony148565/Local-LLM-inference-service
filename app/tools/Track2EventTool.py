import subprocess


class Track2EventTool:
    def __init__(self, python_bin: str, cli_path: str, workdir: str | None = None):
        self.python_bin = python_bin
        self.cli_path = cli_path
        self.workdir = workdir

    def run(self, params: dict) -> dict:
        cmd = [self.python_bin, self.cli_path]

        if params.get("video_path"):
            cmd.extend(["--video", params["video_path"]])
        if params.get("model_path"):
            cmd.extend(["--model", params["model_path"]])
        if params.get("tracks_path"):
            cmd.extend(["--tracks", params["tracks_path"]])
        if params.get("analyze_path"):
            cmd.extend(["--analyze", params["analyze_path"]])
        if params.get("events_path"):
            cmd.extend(["--events", params["events_path"]])

        completed = subprocess.run(
            cmd,
            cwd=self.workdir,
            capture_output=True,
            text=True,
        )

        return {
            "success": completed.returncode == 0,
            "returncode": completed.returncode,
            "command": cmd,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }