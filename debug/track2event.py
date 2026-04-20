import json
from pathlib import Path

from app.dependencies import event_decision_service

CASE_DIR = Path(__file__).parent / "cases"


def load_case(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    case_files = sorted(CASE_DIR.glob("*.json"))

    for case_file in case_files:
        events = load_case(case_file)
        result = event_decision_service.decide(events)

        print("=" * 80)
        print(f"CASE: {case_file.name}")
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()