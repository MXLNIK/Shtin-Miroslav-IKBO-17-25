
import unittest
from src.graph import build_graph, validate_graph


class TestGraph(unittest.TestCase):
    """Тестирует построение графа"""

    def setUp(self):
        """Создает тестовый граф"""
        self.graph = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["D"],
            "D": ["A"]
        }

    def test_bfs(self):
        """Проверяет обход графа"""
        result = build_graph(self.graph, "A", 3, "")
        self.assertEqual(
            set(result.keys()),
            {"A", "B", "C", "D"}
        )

    def test_depth(self):
        """Проверяет ограничение глубины"""
        result = build_graph(self.graph, "A", 1, "")
        self.assertEqual(result["A"], ["B", "C"])
        self.assertEqual(result["B"], [])

    def test_filter(self):
        """Проверяет фильтрацию пакетов"""
        result = build_graph(self.graph, "A", 3, "B")
        self.assertNotIn("B", result["A"])

    def test_cycle(self):
        """Проверяет циклические зависимости"""
        result = build_graph(self.graph, "A", 5, "")
        self.assertEqual(len(result), 4)

    def test_invalid_graph(self):
        """Проверяет некорректный граф"""
        with self.assertRaises(ValueError):
            validate_graph({"a": []})


if __name__ == "__main__":
    unittest.main()
