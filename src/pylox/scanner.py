from typing import List

from pylox.main import error
from pylox.tokens import Token, TokenType


class Scanner:
    keywords = {
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
    }

    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens: List[Token] = []
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1

    def scan_tokens(self) -> List[Token]:
        while self.current < len(self.source):
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self) -> None:
        c: str = self.source[self.current]
        self.current += 1
        match c:
            case "(":
                self.tokens.append(
                    Token(
                        TokenType.LEFT_PAREN,
                        self.source[self.start : self.current],
                        None,
                        self.line,
                    )
                )
            case ")":
                self.tokens.append(
                    Token(
                        TokenType.RIGHT_PAREN,
                        self.source[self.start : self.current],
                        None,
                        self.line,
                    )
                )
            case "{":
                self.tokens.append(
                    Token(
                        TokenType.LEFT_BRACE,
                        self.source[self.start : self.current],
                        None,
                        self.line,
                    )
                )
            case "}":
                self.tokens.append(
                    Token(
                        TokenType.RIGHT_BRACE,
                        self.source[self.start : self.current],
                        None,
                        self.line,
                    )
                )
            case ",":
                self.tokens.append(
                    Token(
                        TokenType.COMMA,
                        self.source[self.start : self.current],
                        None,
                        self.line,
                    )
                )
            case ".":
                self.tokens.append(
                    Token(
                        TokenType.DOT,
                        self.source[self.start : self.current],
                        None,
                        self.line,
                    )
                )
            case "-":
                self.tokens.append(
                    Token(
                        TokenType.MINUS,
                        self.source[self.start : self.current],
                        None,
                        self.line,
                    )
                )
            case "+":
                self.tokens.append(
                    Token(
                        TokenType.PLUS,
                        self.source[self.start : self.current],
                        None,
                        self.line,
                    )
                )
            case ";":
                self.tokens.append(
                    Token(
                        TokenType.SEMICOLON,
                        self.source[self.start : self.current],
                        None,
                        self.line,
                    )
                )
            case "*":
                self.tokens.append(
                    Token(
                        TokenType.STAR,
                        self.source[self.start : self.current],
                        None,
                        self.line,
                    )
                )
            case _:
                error(self.line, "Unexpected character")
