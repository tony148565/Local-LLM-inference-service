import json

VALID_ACTIONS = {"ignore", "log_event", "notify", "alert"}
VALID_PRIORITY = {"low", "medium", "high"}

class EventDecisionService:
    def __init__(self, router):
        self.router = router

    @staticmethod
    def build_prompt(events: list) -> str:
        return f"""
你是一個監控系統決策模組。

以下是偵測到的事件資料：
{json.dumps(events, ensure_ascii=False, indent=2)}

請根據以下規則判斷：

1. 若沒有任何事件，action 必須是 ignore，priority 必須是 low。
2. 若事件為一般短時間 person_staying，action 應為 log_event，priority 為 low。
3. 若 person_staying 持續時間明顯偏長（例如大於 30 秒），action 應至少為 notify。
4. 若多人同時長時間停留，action 可提升為 notify 或 alert。
5. 若事件僅為一般移動或正常活動，action 應為 ignore 或 log_event，不應升級。
6. 請優先根據 duration、事件數量、事件類型判斷，不要一律視為正常。

【輸出限制】
請只輸出合法 JSON，不要輸出任何其他文字。

action 只能是以下其中之一：
- ignore
- log_event
- notify
- alert

priority 只能是以下其中之一：
- low
- medium
- high

格式如下：
{{
  "action": "...",
  "priority": "...",
  "reason": "..."
}}
"""

    @staticmethod
    def parse_json(text: str) -> dict:
        raw_text = text.strip()

        if raw_text.startswith("```json"):
            raw_text = raw_text[len("```json"):].strip()
        elif raw_text.startswith("```"):
            raw_text = raw_text[len("```"):].strip()

        if raw_text.endswith("```"):
            raw_text = raw_text[:-3].strip()

        try:
            return json.loads(raw_text)
        except Exception:
            return {
                "action": "parse_error",
                "priority": "high",
                "reason": raw_text,
            }
    
    def normalize(self, decision: dict) -> dict:
        action = decision.get("action")
        priority = decision.get("priority")

        if action not in VALID_ACTIONS:
            action = "log_event"

        if priority not in VALID_PRIORITY:
            priority = "low"

        return {
            "action": action,
            "priority": priority,
            "reason": decision.get("reason", "")
        }
    
    def decide(self, events: list, max_tokens: int = 256) -> dict:
        prompt = self.build_prompt(events)
        result = self.router.generate(prompt, max_tokens=max_tokens)
        parsed = self.parse_json(result["text"])
        return self.normalize(parsed)