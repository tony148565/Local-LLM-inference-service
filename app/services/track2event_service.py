import json
from pathlib import Path


class Track2EventService:
    def __init__(self, track2event_tool):
        self.track2event_tool = track2event_tool
        self.base_dir = Path("/home/tony/Track2Event")

    def _load_json(self, path: str):
        p = Path(path)
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def run(self, params: dict, debug: bool = False) -> dict:
        params.setdefault("tracks_path", str(self.base_dir / "outputs/tracks.json"))
        params.setdefault("analyze_path", str(self.base_dir / "outputs/analyze_result.json"))
        params.setdefault("events_path", str(self.base_dir / "outputs/stationary_events.json"))
        
        result = self.track2event_tool.run(params)

        if not result["success"]:
            return result

        tracks = self._load_json(params["tracks_path"])
        analyze = self._load_json(params["analyze_path"])
        events = self._load_json(params["events_path"])

        response = {
            "success": True,
            "tracks": tracks,
            "analyze": analyze,
            "events": events,
        }

        if debug:
            response["stdout"] = result.get("stdout")
            response["stderr"] = result.get("stderr")

        return response
