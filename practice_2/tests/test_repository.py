import unittest
from src.repository import build_pom_url, parse_dependencies


class TestRepository(unittest.TestCase):
    """Тестирует получение Maven-зависимостей"""

    def test_build_url(self):
        """Проверяет формирование URL."""
        url = build_pom_url(
            "https://repo1.maven.org/maven2",
            "org.example:demo:1.0"
        )

        self.assertEqual(
            url,
            "https://repo1.maven.org/maven2/"
            "org/example/demo/1.0/demo-1.0.pom"
        )

    def test_parse_dependencies(self):
        """Проверяет извлечение зависимостей"""
        xml = """
        <project>
            <dependencies>
                <dependency>
                    <groupId>org.example</groupId>
                    <artifactId>library</artifactId>
                    <version>1.0</version>
                </dependency>
            </dependencies>
        </project>
        """

        result = parse_dependencies(xml.encode())

        self.assertEqual(result, ["org.example:library:1.0"])

    def test_empty_dependencies(self):
        """Проверяет отсутствие зависимостей"""
        xml = "<project></project>"

        self.assertEqual(parse_dependencies(xml.encode()), [])


if __name__ == "__main__":
    unittest.main()