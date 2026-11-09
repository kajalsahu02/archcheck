import sys


def is_stdlib_module(module_name: str) -> bool:
    """Checks if a given module name belongs to Python's standard library."""
    if not module_name:
        return False

    # Get root module name (e.g., 'os.path' -> 'os')
    root_module = module_name.lstrip(".").split(".")[0]
    return root_module in sys.stdlib_module_names