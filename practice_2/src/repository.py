import urllib.request
import xml.etree.ElementTree as ET


MAVEN_NAMESPACE = {"m": "http://maven.apache.org/POM/4.0.0"}


def build_pom_url(repository_url, package_name):
    """Формирует URL POM-файла Maven"""
    group, artifact, version = package_name.split(":")
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
        headers={"User-Agent": "DependencyVisualizer/1.0"}
    )

    with urllib.request.urlopen(request, timeout=15) as response:
        return response.read()


def parse_dependencies(xml_content):
    """Извлекает прямые зависимости из POM"""
    root = ET.fromstring(xml_content)
    dependencies = root.find("m:dependencies", MAVEN_NAMESPACE)
    result = []

    if dependencies is None:
        return result

    for dependency in dependencies.findall("m:dependency", MAVEN_NAMESPACE):
        group = dependency.findtext("m:groupId", default="", namespaces=MAVEN_NAMESPACE)
        artifact = dependency.findtext("m:artifactId", default="", namespaces=MAVEN_NAMESPACE)
        version = dependency.findtext("m:version", default="", namespaces=MAVEN_NAMESPACE)
        scope = dependency.findtext("m:scope", default="compile", namespaces=MAVEN_NAMESPACE)

        if group and artifact and version:
            if scope not in ("test", "provided"):
                result.append(f"{group}:{artifact}:{version}")

    return result


def get_dependencies(repository_url, package_name):
    """Получает зависимости пакета из Maven-репозитория"""
    url = build_pom_url(repository_url, package_name)
    content = download_pom(url)
    return parse_dependencies(content)