import unittest
import xml.etree.ElementTree as element_tree

from src.xml_converter import convert_to_xml


class TestXmlConverter(unittest.TestCase):
    """Проверяет преобразование данных в XML"""

    def test_empty_config(self):
        """Проверяет пустую конфигурацию"""
        result = convert_to_xml([])
        root = element_tree.fromstring(result)

        self.assertEqual(root.tag, "config")
        self.assertEqual(len(root), 0)

    def test_number(self):
        """Проверяет преобразование числа"""
        result = convert_to_xml([8])
        root = element_tree.fromstring(result)

        self.assertEqual(root[0].tag, "number")
        self.assertEqual(root[0].text, "8")

    def test_dictionary(self):
        """Проверяет преобразование словаря"""
        result = convert_to_xml([
            {"name": 8}
        ])

        root = element_tree.fromstring(result)

        self.assertEqual(root[0].tag, "dict")
        self.assertEqual(
            root[0][0][0].text,
            "name"
        )
        self.assertEqual(
            root[0][0][1][0].text,
            "8"
        )

    def test_nested_dictionary(self):
        """Проверяет вложенные словари"""
        result = convert_to_xml([
            {"server": {"port": 40}}
        ])

        root = element_tree.fromstring(result)

        self.assertEqual(
            root[0][0][1][0].tag,
            "dict"
        )

    def test_multiple_values(self):
        """Проверяет несколько значений"""
        result = convert_to_xml([8, 16, 24])
        root = element_tree.fromstring(result)

        self.assertEqual(len(root), 3)

    def test_special_characters(self):
        """Проверяет обработку XML-символов"""
        result = convert_to_xml([
            {"name": "<server>"}
        ])

        root = element_tree.fromstring(result)

        self.assertEqual(
            root[0][0][1][0].text,
            "<server>"
        )

    def test_xml_declaration(self):
        """Проверяет наличие XML-заголовка"""
        result = convert_to_xml([8])

        self.assertTrue(
            result.startswith("<?xml")
        )


if __name__ == "__main__":
    unittest.main()
