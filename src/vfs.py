import json
import base64
import os


def default_vfs():
    return {
        "type": "dir",
        "children": {
            "home": {
                "type": "dir",
                "children": {}
            },
            "hello.txt": {
                "type": "file",
                "content": "Hello from default VFS",
                "encoding": "utf-8"
            }
        }
    }


class VFS:
    def __init__(self, json_path=None):
        self.json_path = json_path
        self.root = default_vfs()
        self.current_path = "/"

        if json_path:
            self.load(json_path)

    def load(self, path):
        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not self.valid_directory(data):
                raise ValueError("Корень VFS должен быть каталогом.")

            self.root = data
            self.current_path = "/"
            self.json_path = path

        except (OSError, json.JSONDecodeError, ValueError) as error:
            print(f"Ошибка загрузки VFS: {error}")
            self.root = default_vfs()
            self.current_path = "/"

    def valid_directory(self, node):
        if not isinstance(node, dict):
            return False

        if node.get("type") != "dir":
            return False

        children = node.get("children")

        if not isinstance(children, dict):
            return False

        for name, child in children.items():
            if not isinstance(name, str) or name in ("", ".", ".."):
                return False

            if "/" in name or "\\" in name:
                return False

            if not isinstance(child, dict):
                return False

            if child.get("type") == "dir":
                if not self.valid_directory(child):
                    return False
            elif child.get("type") == "file":
                if not isinstance(child.get("content", ""), str):
                    return False

                if child.get("encoding", "utf-8") not in ("utf-8", "base64"):
                    return False
            else:
                return False

        return True

    def get_node(self, path):
        if path.startswith("/"):
            full_path = path
        elif self.current_path == "/":
            full_path = "/" + path
        else:
            full_path = self.current_path + "/" + path

        parts = []

        for part in full_path.split("/"):
            if part in ("", "."):
                continue
            elif part == "..":
                if parts:
                    parts.pop()
            else:
                parts.append(part)

        node = self.root

        for part in parts:
            if node.get("type") != "dir":
                return None

            node = node.get("children", {}).get(part)

            if node is None:
                return None

        return node

    def ls(self, path="."):
        node = self.get_node(path)

        if node is None:
            print(f"Ошибка ls: путь '{path}' не найден.")
        elif node.get("type") == "file":
            print(path)
        else:
            for name in node["children"]:
                print(name)

    def cd(self, path="."):
        node = self.get_node(path)

        if node is None:
            print(f"Ошибка: каталог '{path}' не найден.")
        elif node.get("type") != "dir":
            print(f"Ошибка: '{path}' не является каталогом.")
        else:
            if path.startswith("/"):
                new_path = path
            elif self.current_path == "/":
                new_path = "/" + path
            else:
                new_path = self.current_path + "/" + path

            parts = []

            for part in new_path.split("/"):
                if part in ("", "."):
                    continue
                elif part == "..":
                    if parts:
                        parts.pop()
                else:
                    parts.append(part)

            self.current_path = "/" + "/".join(parts)
            if self.current_path == "":
                self.current_path = "/"

    def read_file(self, path):
        node = self.get_node(path)

        if node is None or node.get("type") != "file":
            print(f"Ошибка: файл '{path}' не найден.")
            return None

        content = node.get("content", "")

        if node.get("encoding") == "base64":
            try:
                return base64.b64decode(content, validate=True)
            except ValueError:
                print("Ошибка: неверные данные Base64.")
                return None

        return content

    def init_default(self):
        self.root = default_vfs()
        self.current_path = "/"

        if self.json_path and os.path.isdir(self.json_path):
            for name in os.listdir(self.json_path):
                path = os.path.join(self.json_path, name)

                if os.path.isfile(path):
                    os.remove(path)
