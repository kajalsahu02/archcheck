from pathlib import Path
from archcheck.graph import DependencyGraph
from archcheck.rules import evaluate_rules, RuleViolation


def test_cannot_import_rule():
    graph = DependencyGraph()
    # Add a forbidden dependency: demo -> app.database
    graph.add_dependency("demo", "app.database")

    rules = [
        {
            "name": "Demo cannot import app.database",
            "from": "demo",
            "cannot_import": "app.database",
        }
    ]

    violations = evaluate_rules(graph, rules, cycles=[])
    assert len(violations) == 1
    assert "Forbidden dependency" in violations[0].description


def test_no_cycles_rule():
    graph = DependencyGraph()
    cycles = [["app.orders", "app.payments", "app.orders"]]

    rules = [{"name": "No cycles allowed", "type": "no_cycles"}]

    violations = evaluate_rules(graph, rules, cycles)
    assert len(violations) == 1
    assert "Circular dependency" in violations[0].description