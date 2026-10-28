
import os
import shlex
import getpass
import socket


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


def execute_command(args):
    """Обрабатывает ls, cd, exit и неизвестные команды"""
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

    else:
        print(f"Ошибка: неизвестная команда '{command}'.")

    return True


def run_repl():
    """Запускает цикл REPL"""
    print("Эмулятор командной оболочки. Введите exit для выхода.")

    while True:
        try:
            command = input(build_prompt())
            args = parse_command(command)

            if not execute_command(args):
                break

        except ValueError as error:
            print(f"Ошибка разбора команды: {error}")

        except EOFError:
            print()
            break

        except KeyboardInterrupt:
            print()
            continue


if __name__ == "__main__":
    run_repl()
