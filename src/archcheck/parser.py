import ast
from pathlib import Path
from typing import List, NamedTuple

class ImportInfo(NamedTuple):
    module: str
    lineno: int
    is_relative: bool

def extract_imports_from_file(file_path: Path, base_dir: Path = None) -> List[ImportInfo]:
    """
    Parses a Python file using AST and returns a list of imported module names.
    Resolves relative imports to absolute package module paths when base_dir is provided.
    """
    imports: List[ImportInfo] = []
    
    try:
        content = file_path.read_text(encoding="utf-8")
        tree = ast.parse(content, filename=str(file_path))
    except Exception:
        return imports

    # Calculate current module's package path (e.g., ecommerce_app/routes.py -> ecommerce_app)
    current_package_parts = []
    if base_dir:
        try:
            rel_path = file_path.relative_to(base_dir)
            current_package_parts = list(rel_path.parent.parts)
        except ValueError:
            pass

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(ImportInfo(module=alias.name, lineno=node.lineno, is_relative=False))
        elif isinstance(node, ast.ImportFrom):
            module_name = node.module or ""
            level = node.level  # level > 0 indicates relative import (e.g. from . import db)

            if level > 0:
                # Resolve relative import level against current package parts
                base_parts = current_package_parts[: max(0, len(current_package_parts) - level + 1)]
                if module_name:
                    resolved_parts = base_parts + [module_name]
                else:
                    resolved_parts = base_parts
                
                full_module = ".".join([p for p in resolved_parts if p])
                if full_module:
                    imports.append(ImportInfo(module=full_module, lineno=node.lineno, is_relative=True))
            else:
                if module_name:
                    imports.append(ImportInfo(module=module_name, lineno=node.lineno, is_relative=False))

    return imports