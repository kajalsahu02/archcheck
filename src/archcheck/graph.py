from typing import Dict, List, Set, Tuple
import networkx as nx
from archcheck.parser import ImportInfo


class DependencyGraph:
    """Manages the networkx directed graph representing module dependencies."""

    def __init__(self):
        self.graph = nx.DiGraph()

    def add_dependency(self, source_module: str, target_module: str):
        """Adds a directed dependency edge: source_module -> target_module."""
        if source_module and target_module and source_module != target_module:
            self.graph.add_edge(source_module, target_module)

    def find_cycles(self) -> List[List[str]]:
        """Detects circular dependency loops (e.g., ['orders', 'payments', 'orders'])."""
        try:
            raw_cycles = list(nx.simple_cycles(self.graph))
            # Format cycles so the loop completes visually (A -> B -> A)
            formatted_cycles = []
            for cycle in raw_cycles:
                formatted_cycles.append(cycle + [cycle[0]])
            return formatted_cycles
        except Exception:
            return []

    def get_fan_out(self, module_name: str) -> int:
        """Calculates fan-out (out-degree): how many modules this module depends on."""
        if module_name in self.graph:
            return self.graph.out_degree(module_name)
        return 0

    def get_fan_in(self, module_name: str) -> int:
        """Calculates fan-in (in-degree): how many other modules depend on this module."""
        if module_name in self.graph:
            return self.graph.in_degree(module_name)
        return 0

    def get_all_modules(self) -> Set[str]:
        """Returns all modules in the graph."""
        return set(self.graph.nodes())