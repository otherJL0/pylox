import argparse
from typing import TextIO, cast, override

from rich.console import Console
from rich.panel import Panel
from rich.prompt import PromptBase
from rich.tree import Tree

from pylox.expr import RichTreePrinter
from pylox.interpreter import Interpreter
from pylox.parser import Parser
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
            parser = Parser(tokens)
            if statements := parser.parse():
                # expr_tree = RichTreePrinter().print(expr)
                # console.print(
                #     Panel(
                #         expr_tree,
                #         title="Expression Tree",
                #         style="cyan",
                #         subtitle=f"`{line.source}`",
                #     )
                # )
                interpreter = Interpreter()
                result = interpreter.interpret(statements)
                console.print(
                    Panel(
                        str(result),
                        title="Result",
                        style="green",
                        subtitle=f"`{line.source}`",
                    )
                )
            else:
                tree = Tree("Detected Tokens:")
                for token in tokens:
                    suffix = (
                        f": {token.lexeme}"
                        if token.token_type == TokenType.IDENTIFIER
                        else ""
                    )
                    _ = tree.add(f"{token.token_type.name}{suffix}")
                console.print(
                    Panel(
                        tree,
                        title="Parsing Error",
                        style="red",
                        subtitle=f"`{line.source}`",
                    )
                )
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
