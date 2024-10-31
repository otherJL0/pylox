from dataclasses import dataclass
from enum import Enum, auto
from typing import override

import rich.repr


class TokenType(Enum):
    # Single-character tokens.
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()

    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()

    # One or two character tokens.
    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    # Literals.
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # Keywords.
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()

    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()
    EXIT = auto()

    EOF = auto()


@dataclass(frozen=True, slots=True)
class Token:
    token_type: TokenType
    lexeme: str
    literal: str | float | int | None
    line: int

    @override
    def __str__(self) -> str:
        return f"{self.token_type.name} {self.lexeme} {self.literal}"

    def __rich_repr__(self) -> rich.repr.Result:
        yield self.lexeme
        yield f"<{self.token_type.name}>"
        if self.literal is not None:
            yield f"({self.literal})"
