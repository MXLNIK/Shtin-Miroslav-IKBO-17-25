import json
from pathlib import Path


def load_test_repository(filename):
    """Загружает тестовый граф из JSON"""
    path = Path(filename)

    if not path.is_file():
        raise FileNotFoundError("Тестовый репозиторий не найден")

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def validate_graph(graph):
    """Проверяет структуру тестового графа"""
    if not isinstance(graph, dict):
        raise ValueError("Граф должен быть словарем")

    for package, dependencies in graph.items():
        if not package.isalpha() or not package.isupper():
            raise ValueError("Имена пакетов должны быть большими латинскими буквами")

        if not isinstance(dependencies, list):
            raise ValueError("Зависимости должны быть списками")

        for dependency in dependencies:
            if not isinstance(dependency, str):
                raise ValueError("Некорректное имя зависимости")

            if not dependency.isalpha() or not dependency.isupper():
                raise ValueError("Некорректное имя пакета")

    return True


def get_test_dependencies(graph, package):
    """Получает прямые зависимости тестового пакета"""
    if package not in graph:
        raise ValueError(f"Пакет {package} отсутствует")

    return graph[package]


def build_graph(graph, package, max_depth, filter_substring):
    """Строит граф зависимостей рекурсивным BFS"""
    result = {}
    visited = set()

    def bfs(queue):
        """Рекурсивно обрабатывает очередь BFS"""
        if not queue:
            return

        current, depth = queue.pop(0)

        if current in visited:
            bfs(queue)
            return

        visited.add(current)

        if depth >= max_depth:
            result[current] = []
            bfs(queue)
            return

        dependencies = graph.get(current, [])
        dependencies = [
            item for item in dependencies
            if filter_substring not in item
        ]

        result[current] = dependencies

        for dependency in dependencies:
            if dependency not in visited:
                queue.append((dependency, depth + 1))

        bfs(queue)

    bfs([(package, 0)])
    return result