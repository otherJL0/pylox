import random
import pytest

from pylox.expr import Binary, Expr
from pylox.parser import Parser
from pylox.scanner import Scanner


def streamlined_parse(source: str) -> Expr | None:
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens)
    return parser.parse()


def generate_binary_expression_str() -> str:
    right = random.randint(0, 1000)
    left = random.randint(0, 1000)
    operator = random.choice(["+", "-", "/", "*"])
    return f"{left} {operator} {right}"


@pytest.mark.parametrize(
    "binary_expression",
    [generate_binary_expression_str() for _ in range(100)],
)
def test_parse_binary_expr(binary_expression: str):
    expr = streamlined_parse(binary_expression)
    assert isinstance(expr, Binary)
