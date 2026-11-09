ArchCheck

ArchCheck is a lightweight Python tool that analyzes project dependencies and helps identify architectural issues in Python codebases.
It builds dependency graphs, detects circular dependencies, and checks architectural rules defined in a YAML configuration file.

Features

Extracts imports from Python files.
Builds an interactive dependency graph.
Detects circular dependencies.
Generates HTML reports.
Checks architectural rules using YAML configuration.

Tech Stack
Python, Typer, NetworkX, PyYAML, PyVis, Rich.

Installation

git clone https://github.com/kajalsahu02/archcheck.git
cd archcheck

python -m venv .venv
.venv\Scripts\activate

pip install -e .

Usage

Analyze a project:
archcheck analyze path/to/project
Generates an interactive HTML dependency graph and displays analysis in the terminal.

Check architectural rules:
archcheck check path/to/project --config examples/archrules.yaml
Checks the project against the rules defined in the YAML file and reports any violations.

Run Tests
pytest

License
MIT
