import sys
from typing import List

from pylox.tokens import Token, TokenType

RESERVED = {
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

class Scanner:
    @staticmethod
    def report(line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error {where}: {message}", file=sys.stderr)


    @staticmethod
    def error(line: int, message: str) -> None:
        Scanner.report(line, "", message)



    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens: List[Token] = []
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1

    def scan_tokens(self) -> List[Token]:
        while not self._is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self) -> None:
        c: str = self._advance()
        match c:
            # Simple single character matches
            case "(":
                self._add_token(TokenType.LEFT_PAREN)
            case ")":
                self._add_token(TokenType.RIGHT_PAREN)
            case "{":
                self._add_token(TokenType.LEFT_BRACE)
            case "}":
                self._add_token(TokenType.RIGHT_BRACE)
            case ",":
                self._add_token(TokenType.COMMA)
            case ".":
                self._add_token(TokenType.DOT)
            case "-":
                self._add_token(TokenType.MINUS)
            case "+":
                self._add_token(TokenType.PLUS)
            case ";":
                self._add_token(TokenType.SEMICOLON)
            case "*":
                self._add_token(TokenType.STAR)

            # Match the current character and the next character to determine token
            case "!":
                self._add_token(
                    TokenType.BANG_EQUAL if self._match("=") else TokenType.BANG
                )
            case "=":
                self._add_token(
                    TokenType.EQUAL_EQUAL if self._match("=") else TokenType.EQUAL
                )
            case "<":
                self._add_token(
                    TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS
                )
            case ">":
                self._add_token(
                    TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER
                )

            # Slash character can either be a slash or a comment
            case "/":
                if self._match("/"):
                    # Advance through comment without adding token
                    while self._peek() != "\n" and not self._is_at_end():
                        self._advance()
                else:
                    self._add_token(TokenType.SLASH)

            # Ignore whitespace
            case " " | "\r" | "\t":
                pass

            # Increment line count
            case "\n":
                self.line += 1

            # Handle string literals
            case '"':
                self._consume_string()

            # Default case handles numeric literals, reserved words, and errors
            case _:
                if c.isdigit():
                    self._consume_number()
                elif c.isalpha():
                    self._consume_reserved()
                else:
                    Scanner.error(self.line, "Unexpected character")

    def _is_at_end(self) -> bool:
        """Check if all characters in `self.source` have been consumed"""
        return self.current >= len(self.source)

    def _advance(self) -> str:
        """Proceed and consume next character"""
        next_char = self.source[self.current]
        self.current += 1
        return next_char

    def _add_token(self, type: TokenType, literal: object = None) -> None:
        """Helper function to append token to self.tokens

        :type: TokenType
        :literal: object
        """
        text = self.source[self.start : self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def _match(self, expected: str) -> bool:
        """Check if next character in self.source is an expected character"""
        if self._is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def _peek(self) -> str:
        """Look at next character without consuming the character"""
        if self._is_at_end():
            return "\0"
        return self.source[self.current]

    def _consume_string(self) -> None:
        while self._peek() != '"' and not self._is_at_end():
            if self._peek() == "\n":
                self.line += 1
            self._advance()

        if self._is_at_end():
            # String is missing terminal '"'
            Scanner.error(self.line, "Unterminated string")
            return

        # Otherwise, next character is '"'
        self._advance()

        # Trim the surrounding '"' characters around string literal
        value: str = self.source[self.start + 1 : self.current - 1]
        self._add_token(TokenType.STRING, value)

    def _peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def _consume_number(self) -> None:
        while self._peek().isdigit():
            self._advance()

        if self._peek() == "." and self._peek_next().isdigit():
            # Consume the "."
            self._advance()
            # Consume all digits after the "."
            while self._peek().isdigit():
                self._advance()

        self._add_token(TokenType.NUMBER, float(self.source[self.start : self.current]))

    def _consume_reserved(self) -> None:
        while self._peek().isalnum():
            self._advance()

        text: str = self.source[self.start:self.current]
        try:
            self._add_token(RESERVED[text])
        except KeyError:
            self._add_token(TokenType.IDENTIFIER)
