from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, override

from pylox.expr import Expr


class Stmt(ABC):
    @abstractmethod
    def accept[T](self, visitor: "Visitor[T]") -> T:
        pass


@dataclass(frozen=True, slots=True)
class Print(Stmt):
    expr: Expr

    @override
    def accept[T](self, visitor: "Visitor[T]") -> T:
        return visitor.visit_print_stmt(self)


@dataclass(frozen=True, slots=True)
class Expression(Stmt):
    expr: Expr

    @override
    def accept[T](self, visitor: "Visitor[T]") -> T:
        return visitor.visit_expression_stmt(self)


class Visitor[T](ABC):
    @abstractmethod
    def visit_expression_stmt(self, stmt: Expression) -> T:
        pass

    @abstractmethod
    def visit_print_stmt(self, stmt: Print) -> T:
        pass
