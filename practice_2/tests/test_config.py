import unittest
from src.config import validate_config


class TestConfig(unittest.TestCase):
    """Тестирует проверку конфигурации"""

    def setUp(self):
        """Создает тестовую конфигурацию"""
        self.config = {
            "package_name": "org.example:demo:1.0",
            "repository_url": "https://repo1.maven.org/maven2",
            "test_repository": "test_repository.json",
            "test_mode": "true",
            "output_file": "graph.svg",
            "max_depth": "3",
            "filter_substring": "test"
        }

    def test_valid_config(self):
        """Проверяет правильную конфигурацию"""
        self.assertTrue(validate_config(self.config))

    def test_invalid_depth(self):
        """Проверяет неправильную глубину"""
        self.config["max_depth"] = "-1"

        with self.assertRaises(ValueError):
            validate_config(self.config)

    def test_invalid_package(self):
        """Проверяет неправильное имя пакета"""
        self.config["package_name"] = "demo"

        with self.assertRaises(ValueError):
            validate_config(self.config)

    def test_invalid_mode(self):
        """Проверяет неправильный режим"""
        self.config["test_mode"] = "maybe"

        with self.assertRaises(ValueError):
            validate_config(self.config)

    def test_invalid_output(self):
        """Проверяет неправильный формат результата"""
        self.config["output_file"] = "graph.txt"

        with self.assertRaises(ValueError):
            validate_config(self.config)


if __name__ == "__main__":
    unittest.main()