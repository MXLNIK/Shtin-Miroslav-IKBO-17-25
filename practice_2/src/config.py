import configparser
from pathlib import Path


DEFAULT_CONFIG = "config.ini"


def load_config(filename=DEFAULT_CONFIG):
    """Загружает параметры из INI-файла"""
    parser = configparser.ConfigParser()

    if not Path(filename).is_file():
        raise FileNotFoundError(f"Файл {filename} не найден")

    parser.read(filename, encoding="utf-8")

    if not parser.has_section("settings"):
        raise ValueError("Отсутствует секция [settings]")

    return dict(parser.items("settings"))


def validate_required_params(config):
    """Проверяет наличие и заполненность обязательных параметров"""
    required = [
        "package_name",
        "repository_url",
        "test_repository",
        "test_mode",
        "output_file",
        "max_depth",
        "filter_substring"
    ]

    for key in required:
        if not config.get(key, "").strip():
            raise ValueError(f"Параметр {key} не может быть пустым")


def validate_test_mode(config):
    """Проверяет режим тестирования"""
    if config["test_mode"].lower() not in ("true", "false"):
        raise ValueError("test_mode должен быть true или false")


def validate_max_depth(config):
    """Проверяет максимальную глубину"""
    try:
        depth = int(config["max_depth"])
        if depth < 0:
            raise ValueError
    except ValueError:
        raise ValueError("max_depth должен быть целым числом >= 0")


def validate_package_name(config):
    """Проверяет формат имени пакета"""
    if ":" not in config["package_name"]:
        raise ValueError(
            "Формат имени пакета: group:artifact:version"
        )


def validate_output_file(config):
    """Проверяет формат выходного файла"""
    if not config["output_file"].endswith(".svg"):
        raise ValueError("Файл результата должен иметь формат SVG")


def validate_repository(config):
    """Проверяет URL основного репозитория"""
    if config["test_mode"].lower() == "false":
        if not config["repository_url"].startswith(("http://", "https://")):
            raise ValueError("Некорректный URL репозитория")


def validate_test_repository(config):
    """Проверяет наличие тестового репозитория"""
    if config["test_mode"].lower() == "true":
        if not Path(config["test_repository"]).is_file():
            raise FileNotFoundError("Файл тестового репозитория не найден")


def validate_config(config):
    """Проверяет корректность параметров конфигурации"""
    validate_required_params(config)
    validate_test_mode(config)
    validate_max_depth(config)
    validate_package_name(config)
    validate_output_file(config)
    validate_repository(config)
    validate_test_repository(config)

    return True
