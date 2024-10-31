from configparser import ParsingError
from typing import Any
from pylox.token import Token, TokenType

KEYWORDS: dict[str, TokenType] = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
    "exit": TokenType.EXIT,
}


class Scanner:
    def __init__(self, source: str) -> None:
        self.source: str = source
        self.tokens: list[Token] = []
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1

    def __next__(self) -> str:
        character: str = self.source[self.current]
        self.current += 1
        return character

    @property
    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def add_token(self, token_type: TokenType, literal: Any | None = None) -> None:
        text: str = self.source[self.start : self.current]
        self.tokens.append(
            Token(token_type=token_type, lexeme=text, literal=literal, line=self.line)
        )

    def next_is(self, expected: str) -> bool:
        if self.is_at_end:
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    @property
    def next(self) -> str:
        if self.is_at_end:
            return "\0"
        return self.source[self.current]

    @property
    def next_next(self) -> str:
        if self.current + 1 > len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def string(self) -> None:
        while self.next != '"' and not self.is_at_end:
            if self.next_is("\n"):
                self.line += 1
            _ = next(self)
        if self.is_at_end:
            raise ParsingError("Unterminated string")
        _ = next(self)
        literal = self.source[self.start + 1 : self.current - 1]
        self.add_token(token_type=TokenType.STRING, literal=literal)

    def number(self) -> None:
        while self.next.isnumeric():
            _ = next(self)
        if self.next == "." and self.next_next.isnumeric():
            _ = next(self)
        while self.next.isnumeric():
            _ = next(self)
        literal = float(self.source[self.start : self.current])
        self.add_token(token_type=TokenType.NUMBER, literal=literal)

    def identifier(self) -> None:
        while self.next.isidentifier():
            _ = next(self)
        text = self.source[self.start : self.current]
        token_type = KEYWORDS.get(text, TokenType.IDENTIFIER)
        self.add_token(token_type=token_type)

    def scan_token(self) -> None:
        character = next(self)
        match character:
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.add_token(TokenType.LEFT_BRACE)
            case "}":
                self.add_token(TokenType.RIGHT_BRACE)
            case ",":
                self.add_token(TokenType.COMMA)
            case ".":
                self.add_token(TokenType.DOT)
            case "-":
                self.add_token(TokenType.MINUS)
            case "+":
                self.add_token(TokenType.PLUS)
            case ";":
                self.add_token(TokenType.SEMICOLON)
            case "*":
                self.add_token(TokenType.STAR)
            case "!":
                self.add_token(
                    TokenType.BANG_EQUAL if self.next_is("=") else TokenType.BANG
                )
            case "=":
                self.add_token(
                    TokenType.EQUAL_EQUAL if self.next_is("=") else TokenType.EQUAL
                )
            case "<":
                self.add_token(
                    TokenType.LESS_EQUAL if self.next_is("=") else TokenType.LESS
                )
            case ">":
                self.add_token(
                    TokenType.GREATER_EQUAL if self.next_is("=") else TokenType.GREATER
                )
            case "/":
                if self.next_is("/"):
                    while self.next != "\n" and not self.is_at_end:
                        _ = next(self)
                else:
                    self.add_token(TokenType.SLASH)
            case " " | "\r" | "\t":
                pass
            case "\n":
                self.line += 1
            case '"':
                self.string()
            case _:
                if character.isnumeric():
                    return self.number()
                if character.isidentifier():
                    return self.identifier()
                raise ParsingError(f"Unexpected character: {character}")

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end:
            self.start = self.current
            self.scan_token()
        self.tokens.append(
            Token(token_type=TokenType.EOF, lexeme="", literal=None, line=self.line)
        )
        return self.tokens
