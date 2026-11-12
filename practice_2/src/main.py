from config import load_config, validate_config


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
        print("\nКонфигурация успешно загружена")

    except (ValueError, FileNotFoundError) as error:
        print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()