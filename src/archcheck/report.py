import webbrowser
from pathlib import Path
from typing import List, Set
from pyvis.network import Network
from rich.console import Console
from rich.table import Table

from archcheck.graph import DependencyGraph

console = Console()


def print_terminal_report(graph: DependencyGraph, cycles: List[List[str]]):
    """Prints a styled terminal summary using Rich tables."""
    all_modules = graph.get_all_modules()

    console.print("\n[bold blue]=== ARCHCHECK DEPENDENCY ANALYSIS ===[/bold blue]\n")

    # 1. Summary Metrics Table
    summary_table = Table(title="Module Metrics", show_header=True, header_style="bold magenta")
    summary_table.add_column("Module Name", style="cyan")
    summary_table.add_column("Fan-In (Depended On By)", justify="center")
    summary_table.add_column("Fan-Out (Depends On)", justify="center")
    summary_table.add_column("Status", justify="center")

    for module in sorted(all_modules):
        fan_in = graph.get_fan_in(module)
        fan_out = graph.get_fan_out(module)

        # Highlight high coupling (fan-out > 5) as warning
        status = "[red]High Coupling[/red]" if fan_out > 5 else "[green]OK[/green]"
        summary_table.add_row(module, str(fan_in), str(fan_out), status)

    console.print(summary_table)

    # 2. Circular Dependencies Output
    if cycles:
        console.print("\n[bold red]⚠️ CIRCULAR DEPENDENCIES DETECTED:[/bold red]")
        for idx, cycle in enumerate(cycles, 1):
            console.print(f"  {idx}. [yellow]{' -> '.join(cycle)}[/yellow]")
    else:
        console.print("\n[bold green]✓ No circular dependencies found![/bold green]")


def generate_html_report(
    graph: DependencyGraph, 
    cycles: List[List[str]], 
    output_path: Path, 
    open_browser: bool = True
):
    """Generates an interactive HTML dependency graph using Pyvis and optionally opens it in browser."""
    net = Network(height="750px", width="100%", directed=True, notebook=False)

    # Convert cycle nodes to a set for quick highlighting
    cycle_nodes: Set[str] = set()
    for cycle in cycles:
        cycle_nodes.update(cycle)

    # Add nodes with visual colors
    for node in graph.get_all_modules():
        if node in cycle_nodes:
            color = "#ff4d4d"  # Red for circular dependency involvement
            title = f"{node} (Involved in Cycle)"
        elif graph.get_fan_out(node) > 5:
            color = "#ffa500"  # Orange for high fan-out
            title = f"{node} (High Fan-Out: {graph.get_fan_out(node)})"
        else:
            color = "#4da6ff"  # Blue for healthy nodes
            title = node

        net.add_node(node, label=node, color=color, title=title)

    # Add directed edges
    for source, target in graph.graph.edges():
        net.add_edge(source, target)

    net.save_graph(str(output_path))
    console.print(f"\n[bold green]✓ Interactive HTML report generated at:[/bold green] {output_path}")

    # Automatically open the generated HTML file in the user's default browser
    if open_browser:
        resolved_url = output_path.resolve().as_uri()
        webbrowser.open(resolved_url)