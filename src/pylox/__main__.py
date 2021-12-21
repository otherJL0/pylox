import argparse


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


if __name__ == "__main__":  # pragma: no cover
    entrypoint()
