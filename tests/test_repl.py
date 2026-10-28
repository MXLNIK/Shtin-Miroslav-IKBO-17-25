import unittest
import os
from io import StringIO
from contextlib import redirect_stdout

from src.main import parse_command, execute_command, run_script
from src.vfs import VFS


class TestREPL(unittest.TestCase):

    def test_parse_command(self):
        result = parse_command("ls folder")
        self.assertEqual(result, ["ls", "folder"])

    def test_environment_variable(self):
        os.environ["TEST_FOLDER"] = "my_folder"

        result = parse_command("ls $TEST_FOLDER")

        self.assertEqual(result, ["ls", "my_folder"])

    def test_ls(self):
        output = StringIO()

        with redirect_stdout(output):
            execute_command(["ls", "folder"], vfs=VFS())

        self.assertIn("ls", output.getvalue())
        self.assertIn("folder", output.getvalue())

    def test_unknown_command(self):
        output = StringIO()

        with redirect_stdout(output):
            execute_command(["unknown"])

        self.assertIn("неизвестная команда", output.getvalue())

    def test_exit(self):
        self.assertFalse(execute_command(["exit"]))

    def test_exit_with_arguments(self):
        output = StringIO()

        with redirect_stdout(output):
            result = execute_command(["exit", "123"])

        self.assertTrue(result)
        self.assertIn("не принимает аргументы", output.getvalue())

    def test_cd_with_too_many_arguments(self):
        output = StringIO()

        with redirect_stdout(output):
            execute_command(["cd", "one", "two"])

        self.assertIn("не более одного аргумента", output.getvalue())
    
    def test_conf_dump(self):
        output = StringIO()
        config = {"vfs": "test.json", "script": "startup.txt"}

        with redirect_stdout(output):
            execute_command(["conf-dump"], config)

        self.assertIn("vfs=test.json", output.getvalue())
        self.assertIn("script=startup.txt", output.getvalue())

    def test_conf_dump_with_arguments(self):
        output = StringIO()

        with redirect_stdout(output):
            execute_command(["conf-dump", "extra"], {})

        self.assertIn("не принимает аргументы", output.getvalue())

    def test_script_continues_after_error(self):
        import tempfile

        config = {"vfs": None, "script": None}

        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            suffix=".txt",
            delete=False
        ) as file:
            file.write("unknown_command\n")
            file.write("ls final_folder\n")
            script_path = file.name

        try:
            output = StringIO()

            with redirect_stdout(output):
                run_script(script_path, config, VFS())

            result = output.getvalue()

            self.assertIn("неизвестная команда", result)
            self.assertIn("final_folder", result)
        finally:
            os.remove(script_path)

    def test_vfs_default(self):
        vfs = VFS()

        self.assertEqual(vfs.current_path, "/")
        self.assertIsNotNone(vfs.get_node("hello.txt"))

    def test_vfs_load_json(self):
        vfs = VFS("vfs/files.json")

        self.assertIsNotNone(vfs.get_node("hello.txt"))
        self.assertIsNotNone(vfs.get_node("docs/readme.txt"))

    def test_vfs_cd(self):
        vfs = VFS("vfs/nested.json")

        vfs.cd("/home/student/projects/demo")

        self.assertEqual(vfs.current_path, "/home/student/projects/demo")
        self.assertIsNotNone(vfs.get_node("main.py"))

    def test_vfs_parent_directory(self):
        vfs = VFS("vfs/nested.json")

        vfs.cd("/home/student")
        vfs.cd("..")

        self.assertEqual(vfs.current_path, "/home")

    def test_vfs_init(self):
        vfs = VFS("vfs/files.json")

        vfs.cd("/docs")
        vfs.init_default()

        self.assertEqual(vfs.current_path, "/")
        self.assertIsNotNone(vfs.get_node("hello.txt"))
        self.assertIsNone(vfs.get_node("docs"))

    def test_vfs_binary_file(self):
        import tempfile
        import json

        data = {
            "type": "dir",
            "children": {
                "binary.bin": {
                    "type": "file",
                    "content": "AAEC/w==",
                    "encoding": "base64"
                }
            }
        }

        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            suffix=".json",
            delete=False
        ) as file:
            json.dump(data, file)
            path = file.name

        try:
            vfs = VFS(path)
            self.assertEqual(
                vfs.read_file("binary.bin"),
                bytes([0, 1, 2, 255])
            )
        finally:
            os.remove(path)



if __name__ == "__main__":
    unittest.main()
