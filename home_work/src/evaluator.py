from lark import Transformer
from lark.exceptions import VisitError

from src.config_parser import parse_text


OCTAL_BASE = 8


class ConfigEvaluator(Transformer):
    """Вычисляет значения выражений конфигурационного языка"""

    def __init__(self):
        """Создает таблицу переменных"""
        super().__init__()
        self.variables = {}

    def start(self, items):
        """Возвращает результаты обработки всех конструкций"""
        return list(items)

    def number(self, items):
        """Преобразует восьмеричное число в десятичное"""
        return int(str(items[0]), OCTAL_BASE)

    def variable(self, items):
        """Сохраняет значение объявленной переменной"""
        name = str(items[0])
        value = items[1]
        self.variables[name] = value
        return value

    def variable_name(self, items):
        """Возвращает значение ранее объявленной переменной"""
        name = str(items[0])

        if name not in self.variables:
            raise ValueError(
                f"Переменная '{name}' не объявлена"
            )

        return self.variables[name]

    def expression(self, items):
        """Вычисляет сумму элементов выражения"""
        return sum(items)

    def absolute(self, items):
        """Возвращает абсолютное значение числа"""
        return abs(items[0])

    def constant(self, items):
        """Возвращает результат константного выражения"""
        return items[0]

    def pair(self, items):
        """Возвращает пару имени и значения"""
        return str(items[0]), items[1]

    def dictionary(self, items):
        """Преобразует словарь в обычный Python-словарь"""
        pairs = [item for item in items if item is not None]
        return dict(pairs)


def evaluate_text(text):
    """Разбирает текст и вычисляет его конструкции"""
    tree = parse_text(text)
    evaluator = ConfigEvaluator()

    try:
        return evaluator.transform(tree)
    except VisitError as error:
        raise error.orig_exc from None
