# 🔍 ArchCheck

> **Lightweight Python Architecture Linter & Dependency Mapper**

ArchCheck is an open-source CLI tool and static analyzer that parses Python codebases into directed graphs to detect circular dependencies, analyze module coupling metrics, export interactive visual dependency graphs, and enforce architectural constraints in CI/CD pipelines.

---

## ✨ Core Features

* 🚀 **AST Import Parsing:** Extracts raw Python imports and standard library boundaries using Python's built-in `ast` module.
* 🕸️ **Dependency Graph Engine:** Built on `networkx` to run cycle detection (`simple_cycles`) and calculate coupling metrics (`fan-in`, `fan-out`).
* 📊 **Interactive HTML Graphs:** Renders searchable, color-coded dependency node graphs powered by `pyvis`.
* 🛡️ **YAML Rules Engine:** Enforces modular boundaries via custom `archrules.yaml` constraints (`cannot_import`, `no_cycles`, `max_fan_out`).
* ⚡ **CI/CD Integration:** Integrates into GitHub Actions to automatically fail PRs that break project architecture.

---

## 🛠️ Installation

```bash
# Clone repository
git clone [https://github.com/your-username/archcheck.git](https://github.com/your-username/archcheck.git)
cd archcheck

# Install in editable development mode
pip install -e .[dev]