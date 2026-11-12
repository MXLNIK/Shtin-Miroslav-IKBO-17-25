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
    """Обрабатывает команды."""
    if not args:
        return True

    command, *arguments = args

    handlers = {
        "exit": lambda: _handle_exit(arguments),
        "ls": lambda: _handle_vfs(arguments, vfs, "ls", "."),
        "cd": lambda: _handle_vfs(arguments, vfs, "cd", "/"),
        "pwd": lambda: _handle_pwd(arguments, vfs),
        "cat": lambda: _handle_cat(arguments, vfs),
        "conf-dump": lambda: _handle_conf_dump(arguments, config),
        "vfs-init": lambda: _handle_vfs_init(arguments, vfs),
    }

    handler = handlers.get(command)
    if handler is None:
        print(f"Ошибка: неизвестная команда '{command}'.")
        return True

    return handler()


def _handle_exit(args):
    if args:
        print("Ошибка: команда exit не принимает аргументы.")
        return True
    return False


def _handle_vfs(args, vfs, method, default_path):
    if len(args) > 1:
        print(f"Ошибка: {method} принимает не более одного аргумента.")
    elif vfs is None:
        print("Ошибка: VFS не инициализирована.")
    else:
        getattr(vfs, method)(args[0] if args else default_path)
    return True


def _handle_pwd(args, vfs):
    if args:
        print("Ошибка: pwd не принимает аргументы.")
    elif vfs:
        print(vfs.current_path)
    return True


def _handle_cat(args, vfs):
    if len(args) != 1:
        print("Ошибка: cat требует один путь к файлу.")
    elif vfs is not None:
        content = vfs.read_file(args[0])
        if content is not None:
            print(content.hex() if isinstance(content, bytes) else content)
    return True


def _handle_conf_dump(args, config):
    if args:
        print("Ошибка: команда conf-dump не принимает аргументы.")
    else:
        for key, value in (config or {}).items():
            print(f"{key}={value}")
    return True


def _handle_vfs_init(args, vfs):
    if args:
        print("Ошибка: vfs-init не принимает аргументы.")
    elif vfs is not None:
        vfs.init_default()
        print("VFS сброшена к состоянию по умолчанию.")
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
