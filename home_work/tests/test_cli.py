import os
import tempfile
import unittest

from unittest.mock import patch

from src.main import main


class TestCLI(unittest.TestCase):
    """Проверяет работу интерфейса командной строки"""

    def test_successful_translation(self):
        """Проверяет успешную запись XML в файл."""
        with tempfile.TemporaryDirectory() as directory:
            output = os.path.join(directory, "result.xml")

            with patch("sys.argv", ["main", "-o", output]):
                with patch("sys.stdin.read", return_value="0o10"):
                    result = main()

            self.assertEqual(result, 0)

            with open(output, encoding="utf-8") as file:
                content = file.read()

            self.assertIn("<number>8</number>", content)

    def test_invalid_syntax(self):
        """Проверяет обработку синтаксической ошибки"""
        with tempfile.TemporaryDirectory() as directory:
            output = os.path.join(directory, "result.xml")

            with patch("sys.argv", ["main", "-o", output]):
                with patch("sys.stdin.read", return_value="dict(name = )"):
                    with patch("sys.stderr"):
                        result = main()

            self.assertEqual(result, 1)
            self.assertFalse(os.path.exists(output))

    def test_unknown_variable(self):
        """Проверяет обработку неизвестной переменной"""
        with tempfile.TemporaryDirectory() as directory:
            output = os.path.join(directory, "result.xml")

            with patch("sys.argv", ["main", "-o", output]):
                with patch("sys.stdin.read", return_value="unknown"):
                    with patch("sys.stderr"):
                        result = main()

            self.assertEqual(result, 1)

    def test_output_error(self):
        """Проверяет обработку ошибки записи файла"""
        with patch("sys.argv", ["main", "-o", "missing/result.xml"]):
            with patch("sys.stdin.read", return_value="0o10"):
                with patch("sys.stderr"):
                    result = main()

        self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()
