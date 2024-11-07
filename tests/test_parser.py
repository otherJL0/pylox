from enum import Enum, auto
import random
import pytest

from pylox.expr import Binary, Expr
from pylox.parser import Parser
from pylox.scanner import Scanner

GENERATED_TEST_CASE_COUNT: int = 100


class ExpressionType(Enum):
    BINARY = auto()
    GROUPING = auto()
    LITERAL = auto()
    UNARY = auto()


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


def generate_expressions(expression_type: ExpressionType) -> list[str]:
    match expression_type:
        case ExpressionType.BINARY:
            return [
                generate_binary_expression_str()
                for _ in range(GENERATED_TEST_CASE_COUNT)
            ]
        case _:
            raise RuntimeError("Not implemented for expression type")


@pytest.mark.parametrize(
    "binary_expression",
    generate_expressions(ExpressionType.BINARY),
)
def test_parse_binary_expr(binary_expression: str):
    expr = streamlined_parse(binary_expression)
    assert isinstance(expr, Binary)
