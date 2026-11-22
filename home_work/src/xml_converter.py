import xml.etree.ElementTree as element_tree


XML_ENCODING = "utf-8"
XML_VERSION = "1.0"
ROOT_TAG = "config"
DICTIONARY_TAG = "dict"
ITEM_TAG = "item"
NAME_TAG = "name"
VALUE_TAG = "value"
NUMBER_TAG = "number"
TEXT_TAG = "text"


def add_dictionary(parent, dictionary):
    """Добавляет словарь в XML"""
    element = element_tree.SubElement(parent, DICTIONARY_TAG)

    for name, value in dictionary.items():
        item = element_tree.SubElement(element, ITEM_TAG)
        name_element = element_tree.SubElement(item, NAME_TAG)
        name_element.text = str(name)
        value_element = element_tree.SubElement(item, VALUE_TAG)
        add_value(value_element, value)


def add_value(parent, value):
    """Добавляет значение в XML"""
    if isinstance(value, dict):
        add_dictionary(parent, value)
    elif isinstance(value, int):
        element = element_tree.SubElement(parent, NUMBER_TAG)
        element.text = str(value)
    else:
        element = element_tree.SubElement(parent, TEXT_TAG)
        element.text = str(value)


def convert_to_xml(values):
    """Преобразует результаты вычислений в XML"""
    root = element_tree.Element(ROOT_TAG)

    for value in values:
        add_value(root, value)

    tree = element_tree.ElementTree(root)
    element_tree.indent(tree, space="    ")

    return element_tree.tostring(
        root,
        encoding=XML_ENCODING,
        xml_declaration=True
    ).decode(XML_ENCODING)
