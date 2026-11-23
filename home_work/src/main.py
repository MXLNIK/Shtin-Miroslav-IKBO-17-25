import argparse
import sys

from lark.exceptions import UnexpectedInput

from src.evaluator import evaluate_text
from src.xml_converter import convert_to_xml


EXIT_SUCCESS = 0
EXIT_ERROR = 1


def create_argument_parser():
    """Создает обработчик аргументов командной строки"""
    parser = argparse.ArgumentParser(
        description="Транслятор конфигурационного языка в XML"
    )
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Путь к выходному XML-файлу"
    )
    return parser


def translate_text(text):
    """Преобразует исходный текст конфигурации в XML"""
    values = evaluate_text(text)
    return convert_to_xml(values)


def main():
    """Запускает транслятор и обрабатывает ошибки"""
    parser = create_argument_parser()
    args = parser.parse_args()

    try:
        source = sys.stdin.read()
        xml_text = translate_text(source)

        with open(args.output, "w", encoding="utf-8") as file:
            file.write(xml_text)

        print(f"XML сохранен в файл: {args.output}")
        return EXIT_SUCCESS

    except (UnexpectedInput, ValueError, OSError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return EXIT_ERROR


if __name__ == "__main__":
    sys.exit(main())
