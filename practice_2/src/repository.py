import re
import urllib.request
import xml.etree.ElementTree as element_tree


MAVEN_NAMESPACE = "http://maven.apache.org/POM/4.0.0"
USER_AGENT = "DependencyVisualizer/1.0"
TIMEOUT = 15
EXCLUDED_SCOPES = ("test", "provided")
PROPERTY_PATTERN = re.compile(r"\$\{([^}]+)\}")


def build_pom_url(repository_url, package_name):
    """Формирует URL POM-файла Maven"""
    expected_parts_count = 3
    parts = package_name.split(":")

    if len(parts) != expected_parts_count:
        raise ValueError("Ожидается формат group:artifact:version")

    group, artifact, version = parts
    group_path = group.replace(".", "/")
    filename = f"{artifact}-{version}.pom"

    return (
        f"{repository_url.rstrip('/')}/"
        f"{group_path}/{artifact}/{version}/{filename}"
    )


def download_pom(url):
    """Загружает содержимое POM-файла"""
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT}
    )

    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        return response.read()


def find_element(parent, name):
    """Ищет XML-элемент с учетом пространства имен"""
    element = parent.find(f"{{{MAVEN_NAMESPACE}}}{name}")

    if element is None:
        element = parent.find(name)

    return element


def get_text(parent, name, default=""):
    """Получает текст XML-элемента"""
    element = find_element(parent, name)

    if element is None or element.text is None:
        return default

    return element.text.strip()


def resolve_properties(value, properties):
    """Подставляет значения Maven properties"""
    for _ in range(len(properties) + 1):
        matches = PROPERTY_PATTERN.findall(value)

        if not matches:
            break

        for name in matches:
            replacement = properties.get(name)

            if replacement is None:
                return ""

            value = value.replace(f"${{{name}}}", replacement)

    return value


def get_properties(root, inherited):
    """Получает свойства POM с учетом наследования"""
    properties = inherited.copy()
    element = find_element(root, "properties")

    if element is not None:
        for item in list(element):
            name = item.tag.split("}")[-1]
            properties[name] = (item.text or "").strip()

    return properties


def get_managed_versions(root, properties, inherited):
    """Получает версии зависимостей из dependencyManagement"""
    result = inherited.copy()
    management = find_element(root, "dependencyManagement")

    if management is None:
        return result

    dependencies = find_element(management, "dependencies")

    if dependencies is None:
        return result

    for dependency in list(dependencies):
        group = resolve_properties(
            get_text(dependency, "groupId"), properties
        )
        artifact = resolve_properties(
            get_text(dependency, "artifactId"), properties
        )
        version = resolve_properties(
            get_text(dependency, "version"), properties
        )

        if group and artifact and version:
            result[f"{group}:{artifact}"] = version

    return result


def load_pom_context(repository_url, package_name, visited=None):
    """Загружает POM и наследуемые настройки родительских POM"""
    if visited is None:
        visited = set()

    if package_name in visited:
        return {}, {}

    visited.add(package_name)
    url = build_pom_url(repository_url, package_name)
    root = element_tree.fromstring(download_pom(url))

    properties = {}
    managed = {}
    parent = find_element(root, "parent")

    if parent is not None:
        group = get_text(parent, "groupId")
        artifact = get_text(parent, "artifactId")
        version = get_text(parent, "version")

        if group and artifact and version:
            parent_package = f"{group}:{artifact}:{version}"
            properties, managed = load_pom_context(
                repository_url, parent_package, visited
            )

    properties = get_properties(root, properties)
    managed = get_managed_versions(root, properties, managed)

    return properties, managed


def parse_dependencies(xml_content):
    """Извлекает зависимости с явно указанными версиями"""
    root = element_tree.fromstring(xml_content)
    dependencies = find_element(root, "dependencies")
    result = []

    if dependencies is None:
        return result

    for dependency in list(dependencies):
        group = get_text(dependency, "groupId")
        artifact = get_text(dependency, "artifactId")
        version = get_text(dependency, "version")
        scope = get_text(dependency, "scope", "compile")

        if group and artifact and version:
            if scope not in EXCLUDED_SCOPES:
                result.append(f"{group}:{artifact}:{version}")

    return result


def extract_dependencies(root, properties, managed):
    """Извлекает зависимости с учетом свойств и управления версиями"""
    dependencies = find_element(root, "dependencies")
    result = []

    if dependencies is None:
        return result

    for dependency in list(dependencies):
        group = resolve_properties(get_text(dependency, "groupId"), properties)
        artifact = resolve_properties(
            get_text(dependency, "artifactId"), properties
        )
        version = resolve_properties(
            get_text(dependency, "version"), properties
        )
        scope = resolve_properties(
            get_text(dependency, "scope", "compile"), properties
        )

        if not version:
            version = managed.get(f"{group}:{artifact}", "")

        if group and artifact and version:
            if scope not in EXCLUDED_SCOPES:
                result.append(f"{group}:{artifact}:{version}")

    return result


def get_dependencies(repository_url, package_name):
    """Получает зависимости пакета из Maven-репозитория"""
    url = build_pom_url(repository_url, package_name)
    root = element_tree.fromstring(download_pom(url))
    properties, managed = load_pom_context(
        repository_url, package_name
    )

    return extract_dependencies(root, properties, managed)


def validate_depth(max_depth):
    """Проверяет корректность максимальной глубины"""
    if max_depth < 0:
        raise ValueError("Глубина не может быть отрицательной")


def filter_dependencies(dependencies, filter_substring):
    """Фильтрует зависимости по подстроке"""
    if not filter_substring:
        return dependencies

    return [
        item for item in dependencies
        if filter_substring not in item
    ]


def get_package_dependencies(repository_url, package_name, filter_substring):
    """Получает и фильтрует зависимости пакета"""
    dependencies = get_dependencies(repository_url, package_name)

    return filter_dependencies(dependencies, filter_substring)


def process_package(repository_url, current, depth, context):
    """Обрабатывает пакет и добавляет его зависимости в очередь"""
    dependencies = get_package_dependencies(
        repository_url,
        current,
        context["filter_substring"]
    )

    if depth < context["max_depth"]:
        context["graph"][current] = dependencies

        for dependency in dependencies:
            if dependency not in context["visited"]:
                context["queue"].append((dependency, depth + 1))
    else:
        context["graph"][current] = []


def get_maven_graph(repository_url, package_name, max_depth, filter_substring):
    """Строит граф Maven-зависимостей"""
    validate_depth(max_depth)

    context = {
        "max_depth": max_depth,
        "filter_substring": filter_substring,
        "graph": {},
        "visited": set(),
        "queue": [(package_name, 0)]
    }

    while context["queue"]:
        current, depth = context["queue"].pop(0)

        if current in context["visited"]:
            continue

        context["visited"].add(current)

        process_package(
            repository_url,
            current,
            depth,
            context
        )

    return context["graph"]
