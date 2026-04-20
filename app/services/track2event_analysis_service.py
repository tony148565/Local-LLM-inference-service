class Track2EventAnalysisService:
    def __init__(self, track2event_service, event_decision_service):
        self.track2event_service = track2event_service
        self.event_decision_service = event_decision_service

    def run(self, params: dict, debug:bool = False) -> dict:
        track2event_result = self.track2event_service.run(params, debug)

        if not track2event_result["success"]:
            return {
                "success": False,
                "stage": "track2event",
                **track2event_result,
            }

        events = track2event_result.get("events") or []
        decision = self.event_decision_service.decide(events)

        
        response =  {
            "success": True,
            "stage": "completed",
            "decision": decision,
        }
        
        if debug:
            response["track2event"] = track2event_result
        
        return response
    
    def run_with_events(self, events: list, debug: bool = False) -> dict:
        decision = self.event_decision_service.decide(events, debug=debug)

        return {
            "success": True,
            "stage": "completed",
            "source": "injected_events",
            "events": events,
            "decision": decision,
        }