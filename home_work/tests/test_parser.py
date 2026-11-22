import unittest

from lark.exceptions import UnexpectedInput

from src.config_parser import parse_text


class TestParser(unittest.TestCase):
    """Проверяет синтаксический анализ конфигурационного языка"""

    def test_number(self):
        """Проверяет распознавание восьмеричного числа"""
        parse_text("0o17")

    def test_dictionary(self):
        """Проверяет распознавание словаря"""
        parse_text("dict(name = 0o10)")

    def test_nested_dictionary(self):
        """Проверяет вложенные словари"""
        parse_text(
            "dict(first = dict(second = 0o10))"
        )

    def test_variable(self):
        """Проверяет объявление переменной"""
        parse_text("var count := 0o10")

    def test_addition(self):
        """Проверяет сложение"""
        parse_text("0o10 + 0o20")

    def test_absolute(self):
        """Проверяет функцию abs"""
        parse_text("abs(0o10)")

    def test_constant_expression(self):
        """Проверяет константное выражение"""
        parse_text(".{0o10 + 0o20}.")

    def test_multiline_comment(self):
        """Проверяет многострочный комментарий"""
        parse_text("--[[ comment ]] 0o10")

    def test_invalid_number(self):
        """Проверяет обнаружение неправильного числа"""
        with self.assertRaises(UnexpectedInput):
            parse_text("0o89")

    def test_invalid_syntax(self):
        """Проверяет обнаружение синтаксической ошибки"""
        with self.assertRaises(UnexpectedInput):
            parse_text("dict(name = )")


if __name__ == "__main__":
    unittest.main()
