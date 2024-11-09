from typing import override

from pylox.expr import Binary, Expr, Grouping, Literal, Unary, Visitor
from pylox.token import TokenType


class Interpreter(Visitor[object]):
    def evaluate(self, expr: Expr) -> object:
        return expr.accept(self)

    @override
    def visit_literal_expr(self, expr: Literal) -> object:
        return expr.value

    @override
    def visit_grouping_expr(self, expr: Grouping) -> object:
        return self.evaluate(expr.expr)

    @override
    def visit_unary_expr(self, expr: Unary) -> object:
        right = self.evaluate(expr.right)
        match (expr.operator.token_type, right):
            case (TokenType.MINUS, float() | int()):
                return -(float(right))
            case (TokenType.BANG, None):
                return True
            case (TokenType.BANG, bool()):
                return not right
            case (TokenType.BANG, _):
                return False
            case _:
                return None

    @override
    def visit_binary_expr(self, expr: Binary) -> object:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match (expr.operator.token_type, left, right):
            case (TokenType.MINUS, int() | float(), int() | float()):
                return float(left) - float(right)
            case (TokenType.SLASH, int() | float(), int() | float()):
                return float(left) / float(right)
            case (TokenType.STAR, int() | float(), int() | float()):
                return float(left) * float(right)
            case (TokenType.PLUS, int() | float(), int() | float()):
                return float(left) + float(right)
            case (TokenType.PLUS, str(), str()):
                return str(left) + str(right)
            case (TokenType.GREATER, int() | float(), int() | float()):
                return float(left) > float(right)
            case (TokenType.GREATER_EQUAL, int() | float(), int() | float()):
                return float(left) >= float(right)
            case (TokenType.LESS, int() | float(), int() | float()):
                return float(left) < float(right)
            case (TokenType.LESS_EQUAL, int() | float(), int() | float()):
                return float(left) <= float(right)
            case (TokenType.BANG_EQUAL, None, None):
                return False
            case (TokenType.BANG_EQUAL, _, _):
                return left != right
            case (TokenType.EQUAL_EQUAL, None, None):
                return True
            case (TokenType.EQUAL_EQUAL, _, _):
                return left == right
            case _:
                return None
