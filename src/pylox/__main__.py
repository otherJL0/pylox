import argparse
from typing import TextIO, cast, override

from rich.console import Console
from rich.prompt import PromptBase
from rich.tree import Tree
from pylox.scanner import Scanner
from pylox.token import TokenType


class LoxPrompt(PromptBase[Scanner]):
    prompt_suffix: str = ">> "

    @override
    def process_response(self, value: str) -> Scanner:
        return Scanner(value)


def run_prompt() -> None:
    console = Console()
    while True:
        try:
            line = LoxPrompt.ask()
            tokens = line.scan_tokens()
            if tokens[0].token_type == TokenType.EXIT:
                return
            tree = Tree(line.source)
            for token in tokens:
                _ = tree.add(str(token))
            console.print(tree)
        except (EOFError, KeyboardInterrupt):
            return


def run_file(filename: TextIO) -> None:
    source = "".join(filename.readlines())
    filename.close()
    print(source)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="pylox",
        description="A Lox interpreter written in Python",
        epilog="Python 3.13",
    )
    _ = parser.add_argument("filename", nargs="?", type=argparse.FileType("r"))
    args = parser.parse_args()
    args.filename = cast(TextIO | None, args.filename)
    if args.filename is None:
        run_prompt()
    else:
        run_file(args.filename)


if __name__ == "__main__":
    main()
