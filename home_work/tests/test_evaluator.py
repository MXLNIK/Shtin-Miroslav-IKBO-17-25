import unittest

from src.evaluator import evaluate_text


class TestEvaluator(unittest.TestCase):
    """Проверяет вычисление выражений"""

    def test_octal_number(self):
        """Проверяет преобразование восьмеричного числа"""
        result = evaluate_text("0o10")
        self.assertEqual(result, [8])

    def test_addition(self):
        """Проверяет сложение двух чисел"""
        result = evaluate_text("0o10 + 0o20")
        self.assertEqual(result, [24])

    def test_absolute(self):
        """Проверяет вычисление абсолютного значения"""
        result = evaluate_text("abs(0o10)")
        self.assertEqual(result, [8])

    def test_variable_declaration(self):
        """Проверяет объявление переменной"""
        result = evaluate_text("var count := 0o10")
        self.assertEqual(result, [8])

    def test_variable_usage(self):
        """Проверяет использование переменной"""
        text = """
        var first := 0o10
        var second := first + 0o20
        second
        """

        result = evaluate_text(text)
        self.assertEqual(result, [8, 24, 24])

    def test_constant_expression(self):
        """Проверяет константное выражение"""
        text = """
        var number := 0o10
        .{number + 0o20}.
        """

        result = evaluate_text(text)
        self.assertEqual(result, [8, 24])

    def test_nested_expression(self):
        """Проверяет вложенное выражение"""
        result = evaluate_text("abs(0o10 + 0o20)")
        self.assertEqual(result, [24])

    def test_dictionary(self):
        """Проверяет вычисление словаря"""
        result = evaluate_text(
            "dict(first = 0o10, second = 0o20)"
        )

        self.assertEqual(
            result,
            [{"first": 8, "second": 16}]
        )

    def test_nested_dictionary(self):
        """Проверяет вычисление вложенного словаря"""
        result = evaluate_text(
            "dict(server = dict(port = 0o50))"
        )

        self.assertEqual(
            result,
            [{"server": {"port": 40}}]
        )

    def test_unknown_variable(self):
        """Проверяет ошибку неизвестной переменной"""
        with self.assertRaises(ValueError):
            evaluate_text("unknown")

    def test_variable_in_dictionary(self):
        """Проверяет использование переменной в словаре"""
        text = """
        var port := 0o50
        dict(server = port)
        """

        result = evaluate_text(text)

        self.assertEqual(
            result[1],
            {"server": 40}
        )


if __name__ == "__main__":
    unittest.main()
