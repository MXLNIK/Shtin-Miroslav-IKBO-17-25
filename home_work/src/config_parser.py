from lark import Lark


GRAMMAR = r"""
    start: item*

    ?item: variable
         | value

    variable: "var" NAME ":=" value

    ?value: expression

    ?expression: atom ("+" atom)*

    ?atom: NUMBER             -> number
         | NAME               -> variable_name
         | dictionary
         | "abs" "(" expression ")" -> absolute
         | "(" expression ")"
         | ".{" expression "}."    -> constant

    dictionary: "dict" "(" [pair ("," pair)* [","]] ")"

    pair: NAME "=" value

    NAME: /[a-zA-Z]+/

    NUMBER: /0[oO][0-7]+/

    COMMENT: /(?s:--\[\[.*?\]\])/

    %ignore COMMENT
    %import common.WS
    %ignore WS
"""


def create_parser():
    """Создает синтаксический анализатор языка"""
    return Lark(GRAMMAR, parser="lalr")


def parse_text(text):
    """Преобразует исходный текст в синтаксическое дерево"""
    parser = create_parser()
    return parser.parse(text)
