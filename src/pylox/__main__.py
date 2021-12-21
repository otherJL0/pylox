import sys
from typing import Sequence


def repl() -> None:
    print("Pylox repl")
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


def run_script(pylox_script: str) -> None:
    try:
        with open(pylox_script, "rb") as pylox_file:
            bytes = pylox_file.read()
        print(bytes)
    except FileNotFoundError:
        print(f"No such file: {pylox_script}")


def main(cli_args: Sequence[str]) -> None:
    match len(cli_args):
        case 0:
            repl()
        case 1:
            run_script(cli_args[0])
        case _:
            print("Usage: pylox [script]")


def entrypoint() -> None:
    main(sys.argv[1:])


if __name__ == "__main__":  # pragma: no cover
    main(sys.argv[1:])
