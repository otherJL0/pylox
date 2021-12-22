import argparse
import readline
import sys
from pathlib import Path


def report(line: int, where: str, message: str) -> None:
    print(f"[line {line}] Error {where}: {message}", file=sys.stderr)


def error(line: int, message: str) -> None:
    report(line, "", message)


def repl() -> None:
    histfile = Path.home() / ".pylox_history"
    try:
        readline.read_history_file(histfile)
        # default history len is -1 (infinite), which may grow unruly
        readline.set_history_length(1000)
    except FileNotFoundError:
        readline.write_history_file(histfile)

    readline.set_auto_history(True)
    print("Pylox repl")
    try:
        while True:
            match input(">>> "):
                case "":
                    break
                case "exit":
                    print("Use exit() to exit")
                case "exit()":
                    break
                case _:
                    print("User input")
    except (EOFError, KeyboardInterrupt):
        print("\nShutting down...")


def run_script(pylox_script: str) -> None:
    try:
        with open(pylox_script, "rb") as pylox_file:
            bytes = pylox_file.read()
        print(bytes)
    except FileNotFoundError:
        print(f"No such file: {pylox_script}")


def main(cli_args: argparse.Namespace) -> None:
    match vars(cli_args):
        case {"script": None, "interactive": None}:
            repl()
        case {"script": _, "interactive": None}:
            run_script(cli_args.script)
        case {"script": None, "interactive": _}:
            print("TODO: Run script then activate repl")
            repl()
        case _:
            print("Usage: pylox [script]")


def entrypoint() -> None:
    parser = argparse.ArgumentParser("Pylox Interpreter")
    parser.add_argument("script", nargs="?", type=str)
    parser.add_argument("-i", "--interactive", type=str)
    main(parser.parse_args())