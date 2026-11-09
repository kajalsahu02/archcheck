from archcheck.graph import DependencyGraph


def test_cycle_detection():
    graph = DependencyGraph()

    # Create a circular dependency loop: orders -> payments -> shipping -> orders
    graph.add_dependency("app.orders", "app.payments")
    graph.add_dependency("app.payments", "app.shipping")
    graph.add_dependency("app.shipping", "app.orders")

    cycles = graph.find_cycles()

    assert len(cycles) == 1
    assert cycles[0][0] == cycles[0][-1]  # Confirms loop closes on itself


def test_fan_in_fan_out():
    graph = DependencyGraph()

    # app.routes uses app.users and app.orders
    graph.add_dependency("app.routes", "app.users")
    graph.add_dependency("app.routes", "app.orders")

    # app.orders also uses app.users
    graph.add_dependency("app.orders", "app.users")

    # Check metrics
    assert graph.get_fan_out("app.routes") == 2  # Depends on 2 modules
    assert graph.get_fan_in("app.users") == 2    # Used by 2 modules