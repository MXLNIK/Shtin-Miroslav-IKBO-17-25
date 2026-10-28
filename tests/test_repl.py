
import unittest
import os
from io import StringIO
from contextlib import redirect_stdout

from src.main import parse_command, execute_command


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
            execute_command(["ls", "folder"])

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


if __name__ == "__main__":
    unittest.main()
