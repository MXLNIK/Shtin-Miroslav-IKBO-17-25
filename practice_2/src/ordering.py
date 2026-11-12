def get_load_order(graph, package):
    """Определяет порядок загрузки зависимостей"""
    visited = set()
    active = set()
    result = []

    def visit(current):
        """Рекурсивно обходит зависимости"""
        if current in active:
            raise ValueError(f"Обнаружен цикл: {current}")

        if current in visited:
            return

        active.add(current)

        for dependency in graph.get(current, []):
            visit(dependency)

        active.remove(current)
        visited.add(current)
        result.append(current)

    visit(package)
    return result