from pathlib import Path
from typing import Dict, List, Any
import yaml
from archcheck.graph import DependencyGraph


class RuleViolation:
    """Represents a broken architectural rule."""

    def __init__(self, rule_name: str, description: str, severity: str = "ERROR"):
        self.rule_name = rule_name
        self.description = description
        self.severity = severity

    def __repr__(self):
        return f"[{self.severity}] {self.rule_name}: {self.description}"


def load_rules(config_path: Path) -> List[Dict[str, Any]]:
    """Loads and parses the archrules.yaml configuration file."""
    if not config_path.exists():
        return []

    try:
        content = config_path.read_text(encoding="utf-8")
        parsed = yaml.safe_load(content)
        return parsed.get("rules", []) if parsed else []
    except Exception:
        return []


def evaluate_rules(graph: DependencyGraph, rules: List[Dict[str, Any]], cycles: List[List[str]]) -> List[RuleViolation]:
    """Evaluates configured architecture rules against the dependency graph."""
    violations: List[RuleViolation] = []

    for rule in rules:
        name = rule.get("name", "Unnamed Rule")
        rule_type = rule.get("type")

        # 1. Rule Type: cannot_import (Forbidden Dependencies)
        if "from" in rule and "cannot_import" in rule:
            source = rule["from"]
            forbidden_target = rule["cannot_import"]

            if graph.graph.has_edge(source, forbidden_target):
                violations.append(
                    RuleViolation(
                        rule_name=name,
                        description=f"Forbidden dependency found: '{source}' imports '{forbidden_target}'",
                    )
                )

        # 2. Rule Type: no_cycles (Circular Dependency Ban)
        elif rule_type == "no_cycles":
            if cycles:
                for cycle in cycles:
                    cycle_str = " -> ".join(cycle)
                    violations.append(
                        RuleViolation(
                            rule_name=name,
                            description=f"Circular dependency loop detected: {cycle_str}",
                        )
                    )

        # 3. Rule Type: max_fan_out (Coupling Limit)
        elif rule_type == "max_fan_out":
            limit = rule.get("limit", 10)
            for module in graph.get_all_modules():
                fan_out = graph.get_fan_out(module)
                if fan_out > limit:
                    violations.append(
                        RuleViolation(
                            rule_name=name,
                            description=f"Module '{module}' exceeds coupling limit: fan-out is {fan_out} (max allowed: {limit})",
                        )
                    )

    return violations