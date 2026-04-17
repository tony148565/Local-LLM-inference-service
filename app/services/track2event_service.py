class Track2EventService:
    def __init__(self, track2event_tool):
        self.track2event_tool = track2event_tool

    def run(self, params: dict) -> dict:
        result = self.track2event_tool.run(params)

        return {
            "success": result["success"],
            "returncode": result["returncode"],
            "command": result["command"],
            "stdout": result["stdout"],
            "stderr": result["stderr"],
        }