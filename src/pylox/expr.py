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
        return visitor.visit_binary_expression(self)


@dataclass(frozen=True, slots=True)
class Grouping(Expr):
    expression: Expr

    @override
    def accept(self, visitor: "Visitor[T]") -> T:
        return visitor.visit_grouping_expression(self)


@dataclass(frozen=True, slots=True)
class Literal(Expr):
    value: LiteralType | None

    @override
    def accept(self, visitor: "Visitor[T]") -> T:
        return visitor.visit_literal_expression(self)


@dataclass(frozen=True, slots=True)
class Unary(Expr):
    operator: Token
    right: Expr

    @override
    def accept(self, visitor: "Visitor[T]") -> T:
        return visitor.visit_unary_expression(self)


class Visitor[T](ABC):
    @abstractmethod
    def visit_binary_expression(self, expression: Binary) -> T:
        pass

    @abstractmethod
    def visit_grouping_expression(self, expression: Grouping) -> T:
        pass

    @abstractmethod
    def visit_literal_expression(self, expression: Literal) -> T:
        pass

    @abstractmethod
    def visit_unary_expression(self, expression: Unary) -> T:
        pass


class AstPrinter(Visitor[str]):
    def print(self, expression: Expr) -> str:
        return expression.accept(self)

    def parenthesize(self, name: str, *expressions: Expr) -> str:
        return f"({name} {" ".join(expression.accept(self) for expression in expressions)})"

    @override
    def visit_binary_expression(self, expression: Binary) -> str:
        return self.parenthesize(
            expression.operator.lexeme, expression.left, expression.right
        )

    @override
    def visit_grouping_expression(self, expression: Grouping) -> str:
        return self.parenthesize("group", expression.expression)

    @override
    def visit_literal_expression(self, expression: Literal) -> str:
        return "nil" if expression.value is None else str(expression.value)

    @override
    def visit_unary_expression(self, expression: Unary) -> str:
        return self.parenthesize(expression.operator.lexeme, expression.right)


class RichTreePrinter(Visitor[Tree]):
    def print(self, expression: Expr) -> Tree:
        return expression.accept(self)

    def treeify(self, name: str, *expressions: Expr) -> Tree:
        tree = Tree(name)
        for expression in expressions:
            _ = tree.add(expression.accept(self))
        return tree

    @override
    def visit_binary_expression(self, expression: Binary) -> Tree:
        return self.treeify(
            expression.operator.lexeme, expression.left, expression.right
        )

    @override
    def visit_grouping_expression(self, expression: Grouping) -> Tree:
        return self.treeify("group", expression.expression)

    @override
    def visit_literal_expression(self, expression: Literal) -> Tree:
        return Tree("nil" if expression.value is None else str(expression.value))

    @override
    def visit_unary_expression(self, expression: Unary) -> Tree:
        return self.treeify(expression.operator.lexeme, expression.right)


if __name__ == "__main__":
    from pylox.token import TokenType

    expression = Binary(
        left=Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)),
        operator=Token(TokenType.STAR, "*", None, 1),
        right=Grouping(Literal(45.87)),
    )
    result = AstPrinter().print(expression)
