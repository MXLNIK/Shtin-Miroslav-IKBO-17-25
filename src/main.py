
import os
import shlex
import getpass
import socket
import argparse


def build_prompt():
    """Формирует приглашение"""
    username = getpass.getuser()
    hostname = socket.gethostname()

    home = os.path.expanduser("~")
    current = os.getcwd()

    if current == home:
        path = "~"
    elif current.startswith(home + os.sep):
        path = "~" + current[len(home):]
    else:
        path = current

    return f"{username}@{hostname}:{path}$ "


def parse_command(command):
    """Разбирает переменные окружения, команды и аргументы"""
    command = os.path.expandvars(command)
    return shlex.split(command)


def execute_command(args, config=None):
    """Обрабатывает команды"""
    if not args:
        return True

    command = args[0]
    arguments = args[1:]

    if command == "exit":
        if arguments:
            print("Ошибка: команда exit не принимает аргументы.")
            return True

        return False

    elif command == "ls":
        print(f"Команда: ls, аргументы: {arguments}")

    elif command == "cd":
        if len(arguments) > 1:
            print("Ошибка: команда cd принимает не более одного аргумента.")
        else:
            print(f"Команда: cd, аргументы: {arguments}")

    elif command == "conf-dump":
        if arguments:
            print("Ошибка: команда conf-dump не принимает аргументы.")
        else:
            if config is None:
                config = {}

            for key, value in config.items():
                print(f"{key}={value}")

    else:
        print(f"Ошибка: неизвестная команда '{command}'.")

    return True


def run_script(script_path, config):
    """Выполняет команды из текстового скрипта"""
    try:
        with open(script_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                print(build_prompt() + line)

                try:
                    args = parse_command(line)
                    if not execute_command(args, config):
                        break
                except ValueError as error:
                    print(f"Ошибка разбора команды: {error}")

    except OSError as error:
        print(f"Ошибка открытия скрипта: {error}")


def run_repl(config):
    """Запускает цикл REPL"""
    print("Эмулятор командной оболочки. Введите exit для выхода.")

    while True:
        try:
            command = input(build_prompt())
            args = parse_command(command)

            if not execute_command(args, config):
                break

        except ValueError as error:
            print(f"Ошибка разбора команды: {error}")

        except EOFError:
            print()
            break

        except KeyboardInterrupt:
            print()
            continue


def main():
    parser = argparse.ArgumentParser(
        description="Эмулятор командной оболочки"
    )

    parser.add_argument(
        "--vfs",
        default=None,
        help="Путь к физическому расположению VFS"
    )

    parser.add_argument(
        "--script",
        default=None,
        help="Путь к стартовому скрипту"
    )

    args = parser.parse_args()

    config = {
        "vfs": args.vfs,
        "script": args.script
    }

    print("Параметры запуска:")
    for key, value in config.items():
        print(f"{key}={value}")

    if args.script:
        run_script(args.script, config)
    else:
        run_repl(config)


if __name__ == "__main__":
    main()
