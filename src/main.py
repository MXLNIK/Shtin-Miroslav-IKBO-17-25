import os
import shlex
import getpass
import socket
import argparse
try:
    from .vfs import VFS
except ImportError:
    from vfs import VFS


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


def execute_command(args, config=None, vfs=None):
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
        if len(arguments) > 1:
            print("Ошибка: ls принимает не более одного аргумента.")
        elif vfs:
            path = arguments[0] if arguments else "."
            vfs.ls(path)
        else:
            print("Ошибка: VFS не инициализирована.")

    elif command == "cd":
        if len(arguments) > 1:
            print("Ошибка: cd принимает не более одного аргумента.")
        elif vfs:
            path = arguments[0] if arguments else "/"
            vfs.cd(path)
        else:
            print("Ошибка: VFS не инициализирована.")

    elif command == "pwd":
        if arguments:
            print("Ошибка: pwd не принимает аргументы.")
        elif vfs:
            print(vfs.current_path)

    elif command == "cat":
        if len(arguments) != 1:
            print("Ошибка: cat требует один путь к файлу.")
        elif vfs:
            content = vfs.read_file(arguments[0])
            if content is not None:
                if isinstance(content, bytes):
                    print(content.hex())
                else:
                    print(content)

    elif command == "conf-dump":
        if arguments:
            print("Ошибка: команда conf-dump не принимает аргументы.")
        else:
            for key, value in (config or {}).items():
                print(f"{key}={value}")

    elif command == "vfs-init":
        if arguments:
            print("Ошибка: vfs-init не принимает аргументы.")
        elif vfs:
            vfs.init_default()
            print("VFS сброшена к состоянию по умолчанию.")

    else:
        print(f"Ошибка: неизвестная команда '{command}'.")

    return True


def run_script(script_path, config, vfs):
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
                    if not execute_command(args, config, vfs):
                        break
                except ValueError as error:
                    print(f"Ошибка разбора команды: {error}")

    except OSError as error:
        print(f"Ошибка открытия скрипта: {error}")


def run_repl(config, vfs):
    """Запускает цикл REPL"""
    print("Эмулятор командной оболочки. Введите exit для выхода.")

    while True:
        try:
            command = input(build_prompt())
            args = parse_command(command)

            if not execute_command(args, config, vfs):
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
        help="Путь к JSON-файлу виртуальной файловой системы"
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

    vfs = VFS(args.vfs)

    if args.script:
        run_script(args.script, config, vfs)
    else:
        run_repl(config, vfs)


if __name__ == "__main__":
    main()
