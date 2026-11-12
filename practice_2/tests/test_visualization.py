import unittest
import os

from src.visualization import generate_mermaid, generate_svg


class TestVisualization(unittest.TestCase):
    """Тестирует визуализацию"""

    @staticmethod
    def create_graph():
        """Создает тестовый граф"""
        return {
            "A": ["B"],
            "B": ["C"],
            "C": []
        }

    def test_mermaid(self):
        """Проверяет создание Mermaid"""
        graph = self.create_graph()
        result = generate_mermaid(graph)

        self.assertIn("A --> B", result)
        self.assertIn("B --> C", result)

    def test_svg(self):
        """Проверяет создание SVG"""
        graph = self.create_graph()
        filename = "test_graph.svg"

        generate_svg(graph, filename)

        self.assertTrue(os.path.isfile(filename))

        with open(filename, encoding="utf-8") as file:
            content = file.read()

        self.assertIn("<svg", content)
        self.assertIn("</svg>", content)

        os.remove(filename)


if __name__ == "__main__":
    unittest.main()