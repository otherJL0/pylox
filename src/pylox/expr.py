from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, override

from rich.tree import Tree

from pylox.token import Token

type LiteralType = str | int | float
T = TypeVar("T")


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: "Visitor[T]") -> T:
        pass


@dataclass(frozen=True, slots=True)
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    @override
    def accept(self, visitor: "Visitor[T]") -> T:
        return visitor.visit_binary_expr(self)


@dataclass(frozen=True, slots=True)
class Grouping(Expr):
    expr: Expr

    @override
    def accept(self, visitor: "Visitor[T]") -> T:
        return visitor.visit_grouping_expr(self)


@dataclass(frozen=True, slots=True)
class Literal(Expr):
    value: LiteralType | None

    @override
    def accept(self, visitor: "Visitor[T]") -> T:
        return visitor.visit_literal_expr(self)


@dataclass(frozen=True, slots=True)
class Unary(Expr):
    operator: Token
    right: Expr

    @override
    def accept(self, visitor: "Visitor[T]") -> T:
        return visitor.visit_unary_expr(self)


class Visitor[T](ABC):
    @abstractmethod
    def visit_binary_expr(self, expr: Binary) -> T:
        pass

    @abstractmethod
    def visit_grouping_expr(self, expr: Grouping) -> T:
        pass

    @abstractmethod
    def visit_literal_expr(self, expr: Literal) -> T:
        pass

    @abstractmethod
    def visit_unary_expr(self, expr: Unary) -> T:
        pass


class AstPrinter(Visitor[str]):
    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    def parenthesize(self, name: str, *exprs: Expr) -> str:
        return f"({name} {" ".join(expr.accept(self) for expr in exprs)})"

    @override
    def visit_binary_expr(self, expr: Binary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    @override
    def visit_grouping_expr(self, expr: Grouping) -> str:
        return self.parenthesize("group", expr.expr)

    @override
    def visit_literal_expr(self, expr: Literal) -> str:
        return "nil" if expr.value is None else str(expr.value)

    @override
    def visit_unary_expr(self, expr: Unary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)


class RichTreePrinter(Visitor[Tree]):
    def print(self, expr: Expr) -> Tree:
        return expr.accept(self)

    @override
    def visit_binary_expr(self, expr: Binary) -> Tree:
        tree = Tree("BinaryExpr")
        operator = tree.add(expr.operator.token_type.name)
        _ = operator.add(expr.left.accept(self))
        _ = operator.add(expr.right.accept(self))
        return tree

    @override
    def visit_grouping_expr(self, expr: Grouping) -> Tree:
        tree = Tree("GroupingExpr")
        _ = tree.add(expr.expr.accept(self))
        return tree

    @override
    def visit_literal_expr(self, expr: Literal) -> Tree:
        tree = Tree("LiteralExpr")
        _ = tree.add("nil" if expr.value is None else str(expr.value))
        return tree

    @override
    def visit_unary_expr(self, expr: Unary) -> Tree:
        tree = Tree("UnaryExpr")
        operator = tree.add(expr.operator.token_type.name)
        _ = operator.add(expr.right.accept(self))
        return tree


if __name__ == "__main__":
    from pylox.token import TokenType

    expr = Binary(
        left=Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)),
        operator=Token(TokenType.STAR, "*", None, 1),
        right=Grouping(Literal(45.87)),
    )
    result = AstPrinter().print(expr)
