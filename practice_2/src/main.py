import xml.etree.ElementTree as element_tree

from src.config import load_config, validate_config
from src.repository import get_dependencies
from src.graph import (
    load_test_repository,
    validate_graph,
    get_test_dependencies,
    build_graph
)
from src.ordering import get_load_order
from src.visualization import generate_mermaid, generate_svg
from src.repository import get_maven_graph


def print_config(config):
    """Выводит параметры конфигурации"""
    print("\nПараметры приложения:")

    for key, value in config.items():
        print(f"{key} = {value}")


def print_dependencies(dependencies):
    """Выводит список зависимостей."""
    print("\nПрямые зависимости:")

    for dependency in dependencies:
        print(dependency)


def main():
    """Запускает приложение"""
    try:
        config = load_config()
        validate_config(config)
        print_config(config)
        package = config["package_name"]

        if config["test_mode"].lower() == "true":
            graph = load_test_repository(config["test_repository"])
            validate_graph(graph)
            dependencies = get_test_dependencies(graph, package)
        else:
            graph = get_maven_graph(
                config["repository_url"],
                package,
                int(config["max_depth"]),
                config["filter_substring"]
            )
            dependencies = graph.get(package, [])

        print_dependencies(dependencies)
        result = build_graph(
            graph,
            package,
            int(config["max_depth"]),
            config["filter_substring"]
        )

        print("\nПорядок загрузки:")
        for number, name in enumerate(get_load_order(result, package), 1):
            print(f"{number}. {name}")
        mermaid = generate_mermaid(result)
        print("\nMermaid:")
        print(mermaid)
        generate_svg(result, config["output_file"])
        print(f"\nSVG сохранен: {config['output_file']}")
    except (ValueError, FileNotFoundError, OSError, element_tree.ParseError) as error:
        print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()