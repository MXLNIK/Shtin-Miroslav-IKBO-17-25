from src.config import load_config, validate_config
from src.repository import get_dependencies


def print_config(config):
    """Выводит параметры конфигурации"""
    print("\nПараметры приложения:")

    for key, value in config.items():
        print(f"{key} = {value}")


def main():
    """Запускает приложение"""
    try:
        config = load_config()
        validate_config(config)
        print_config(config)

        if config["test_mode"].lower() == "false":
            dependencies = get_dependencies(
                config["repository_url"],
                config["package_name"]
            )

            print("\nПрямые зависимости:")

            for dependency in dependencies:
                print(dependency)

    except (ValueError, FileNotFoundError, OSError, ET.ParseError) as error:
        print(f"Ошибка: {error}")


if __name__ == "__main__":
    import xml.etree.ElementTree as ET
    main()