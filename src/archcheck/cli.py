from pathlib import Path
import typer
from rich.console import Console
from rich.table import Table

from archcheck.parser import extract_imports_from_file
from archcheck.stdlib import is_stdlib_module
from archcheck.graph import DependencyGraph
from archcheck.report import print_terminal_report, generate_html_report
from archcheck.rules import load_rules, evaluate_rules

app = typer.Typer(
    help="ArchCheck: Lightweight Architecture Linter & Dependency Mapper",
    add_completion=False,
)
console = Console()


@app.command()
def analyze(
    target_dir: Path = typer.Argument(
        ...,
        help="Path to the target Python project directory to analyze",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
    ),
    output: Path = typer.Option(
        Path("archcheck_report.html"),
        "--output",
        "-o",
        help="Path for the output HTML graph report",
    ),
    open_browser: bool = typer.Option(
        True,
        "--open/--no-open",
        help="Automatically open the generated report in your default browser",
    ),
):
    """Analyzes a codebase directory, prints metrics, and generates an interactive HTML graph."""
    console.print(f"[bold cyan]Scanning directory:[/bold cyan] {target_dir}")

    graph = DependencyGraph()
    py_files = list(target_dir.rglob("*.py"))

    if not py_files:
        console.print("[yellow]Warning:[/yellow] No Python (.py) files found in the specified directory.")
        raise typer.Exit(code=0)

    # Parse files and build dependency graph
    for file_path in py_files:
        relative_path = file_path.relative_to(target_dir)
        module_name = ".".join(relative_path.with_suffix("").parts)

        imports = extract_imports_from_file(file_path, base_dir=target_dir)
        for imp in imports:
            if not is_stdlib_module(imp.module):
                graph.add_dependency(module_name, imp.module)

    # Run graph algorithms
    cycles = graph.find_cycles()

    # Render terminal output & HTML report
    print_terminal_report(graph, cycles)
    generate_html_report(graph, cycles, output, open_browser=open_browser)


@app.command()
def check(
    target_dir: Path = typer.Argument(
        ...,
        help="Path to the target Python project directory to check",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
    ),
    config: Path = typer.Option(
        Path("archrules.yaml"),
        "--config",
        "-c",
        help="Path to the architecture rules YAML file",
    ),
):
    """Checks architectural rules against archrules.yaml and exits with code 1 if violated."""
    console.print(f"[bold cyan]Linting architecture for:[/bold cyan] {target_dir}")

    if not config.exists():
        console.print(f"[bold red]Error:[/bold red] Rules config file '{config}' not found.")
        raise typer.Exit(code=1)

    rules = load_rules(config)
    if not rules:
        console.print(f"[yellow]Warning:[/yellow] No valid rules found in '{config}'.")
        raise typer.Exit(code=0)

    graph = DependencyGraph()
    py_files = list(target_dir.rglob("*.py"))

    for file_path in py_files:
        relative_path = file_path.relative_to(target_dir)
        module_name = ".".join(relative_path.with_suffix("").parts)

        imports = extract_imports_from_file(file_path, base_dir=target_dir)
        for imp in imports:
            if not is_stdlib_module(imp.module):
                graph.add_dependency(module_name, imp.module)

    cycles = graph.find_cycles()
    violations = evaluate_rules(graph, rules, cycles)

    if violations:
        console.print(f"\n[bold red]❌ {len(violations)} ARCHITECTURAL VIOLATIONS DETECTED:[/bold red]\n")
        table = Table(show_header=True, header_style="bold red")
        table.add_column("Rule Name", style="yellow")
        table.add_column("Violation Details", style="white")

        for v in violations:
            table.add_row(v.rule_name, v.description)

        console.print(table)
        raise typer.Exit(code=1)
    else:
        console.print("\n[bold green]✓ All architecture rules passed successfully![/bold green]")


def main():
    app()


if __name__ == "__main__":
    main()