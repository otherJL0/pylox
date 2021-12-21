import sys
from typing import Sequence


def repl() -> None:
    print("TODO: Pylox repl")


def run_script(pylox_script: str) -> None:
    print("TODO: Pylox run script")
    print(f"Running {pylox_script}")


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
