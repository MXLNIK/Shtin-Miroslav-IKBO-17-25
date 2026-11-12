import unittest
from src.ordering import get_load_order


class TestOrdering(unittest.TestCase):
    """Тестирует порядок загрузки"""

    def test_load_order(self):
        """Проверяет правильность порядка"""
        graph = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": [],
            "D": []
        }

        result = get_load_order(graph, "A")

        self.assertEqual(result[-1], "A")
        self.assertLess(result.index("D"), result.index("B"))

    def test_cycle(self):
        """Проверяет обнаружение циклов"""
        graph = {
            "A": ["B"],
            "B": ["A"]
        }

        with self.assertRaises(ValueError):
            get_load_order(graph, "A")

    def test_empty_dependencies(self):
        """Проверяет пакет без зависимостей"""
        self.assertEqual(get_load_order({"A": []}, "A"), ["A"])


if __name__ == "__main__":
    unittest.main()