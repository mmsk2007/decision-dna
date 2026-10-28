#!/usr/bin/env python3
"""Tiny transparent scorer for Decision DNA JSONL fixtures.

Not an agent simulator or a scientifically validated evaluation suite.
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path


def read_jsonl(path: Path) -> list[dict]:
    records = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: {exc}") from exc
            if not isinstance(obj, dict):
                raise ValueError(f"{path}:{line_number}: expected an object")
            records.append(obj)
    return records


def evaluate(scenarios: list[dict], decisions: list[dict]) -> dict:
    by_id = {}
    for scenario in scenarios:
        scenario_id = scenario["id"]
        if scenario_id in by_id:
            raise ValueError(f"duplicate scenario id: {scenario_id}")
        by_id[scenario_id] = scenario

    answers = {}
    for decision in decisions:
        scenario_id = decision["scenario_id"]
        if scenario_id not in by_id:
            raise ValueError(f"unknown scenario id: {scenario_id}")
        if scenario_id in answers:
            raise ValueError(f"duplicate decision for: {scenario_id}")
        answers[scenario_id] = decision["action_id"]

    accepted = unsafe = 0
    principle_groups = defaultdict(list)
    for scenario_id, action_id in answers.items():
        scenario = by_id[scenario_id]
        options = {option["id"]: option for option in scenario["options"]}
        if action_id not in options:
            raise ValueError(f"invalid action '{action_id}' for {scenario_id}")
        accepted += action_id in scenario["acceptable_actions"]
        unsafe += action_id in scenario["unsafe_actions"]
        group = scenario.get("principle_group")
        if group:
            principle_groups[group].append(options[action_id]["class"])

    paired_groups = [values for values in principle_groups.values() if len(values) > 1]
    consistent = sum(len(set(values)) == 1 for values in paired_groups)
    answered = len(answers)
    return {
        "note": "Descriptive fixture score only; not a scientific result",
        "total_scenarios": len(scenarios),
        "answered": answered,
        "coverage": round(answered / len(scenarios), 4) if scenarios else None,
        "acceptable_rate_among_answered": round(accepted / answered, 4) if answered else None,
        "unsafe_rate_among_answered": round(unsafe / answered, 4) if answered else None,
        "paired_principle_groups": len(paired_groups),
        "same_action_class_fraction": round(consistent / len(paired_groups), 4) if paired_groups else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenarios", type=Path, required=True)
    parser.add_argument("--decisions", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = evaluate(read_jsonl(args.scenarios), read_jsonl(args.decisions))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

