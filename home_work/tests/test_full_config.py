import unittest
import xml.etree.ElementTree as element_tree

from pathlib import Path

from src.evaluator import evaluate_text
from src.xml_converter import convert_to_xml


EXAMPLES_DIRECTORY = Path("examples")


class TestFullConfig(unittest.TestCase):
    """Проверяет полные конфигурации и дополнительные конструкции"""

    def test_empty_config(self):
        """Проверяет пустую конфигурацию"""
        self.assertEqual(evaluate_text(""), [])

    def test_empty_dictionary(self):
        """Проверяет пустой словарь"""
        self.assertEqual(evaluate_text("dict()"), [{}])

    def test_dictionary_with_trailing_comma(self):
        """Проверяет словарь с завершающей запятой"""
        result = evaluate_text("dict(first = 0o10,)")

        self.assertEqual(result, [{"first": 8}])

    def test_uppercase_octal_prefix(self):
        """Проверяет восьмеричное число с заглавной буквой"""
        self.assertEqual(evaluate_text("0O10"), [8])

    def test_parentheses(self):
        """Проверяет выражение в круглых скобках"""
        self.assertEqual(evaluate_text("(0o10 + 0o20)"), [24])

    def test_absolute_with_addition(self):
        """Проверяет abs с выражением сложения"""
        self.assertEqual(evaluate_text("abs(0o10 + 0o02)"), [10])

    def test_multiple_variables(self):
        """Проверяет несколько последовательных переменных"""
        text = """
        var first := 0o10
        var second := 0o20
        var third := first + second
        third
        """

        self.assertEqual(
            evaluate_text(text),
            [8, 16, 24, 24]
        )

    def test_variable_in_nested_dictionary(self):
        """Проверяет переменную во вложенном словаре"""
        text = """
        var port := 0o50
        dict(server = dict(port = port))
        """

        result = evaluate_text(text)

        self.assertEqual(
            result[1],
            {"server": {"port": 40}}
        )

    def test_nested_constant_expression(self):
        """Проверяет вложенное константное выражение"""
        text = ".{abs((0o10 + 0o20))}."

        self.assertEqual(evaluate_text(text), [24])

    def test_multiline_comment(self):
        """Проверяет многострочный комментарий"""
        text = """
        --[[
        Комментарий
        в несколько строк
        ]]
        0o10
        """

        self.assertEqual(evaluate_text(text), [8])

    def test_missing_closing_parenthesis(self):
        """Проверяет ошибку незакрытой скобки"""
        with self.assertRaises(Exception):
            evaluate_text("abs(0o10")

    def test_missing_dictionary_value(self):
        """Проверяет ошибку отсутствующего значения"""
        with self.assertRaises(Exception):
            evaluate_text("dict(port = )")

    def test_all_examples(self):
        """Проверяет обработку трех готовых конфигураций"""
        example_names = [
            "server.conf",
            "network.conf",
            "warehouse.conf"
        ]

        for example_name in example_names:
            with self.subTest(example=example_name):
                path = EXAMPLES_DIRECTORY / example_name
                source = path.read_text(encoding="utf-8")
                values = evaluate_text(source)
                xml_text = convert_to_xml(values)

                root = element_tree.fromstring(xml_text)

                self.assertEqual(root.tag, "config")
                self.assertGreater(len(root), 0)


if __name__ == "__main__":
    unittest.main()
