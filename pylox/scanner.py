from pylox.tokens import Token, TokenMapping, TokenType


def parse(source: str) -> tuple[Token, ...]:
    start: int = 0
    line: int = 1

    tokens: list[Token] = []
    lexeme: str = ""
    for current, char in enumerate(source):
        start = current
        lexeme += char
        if token_type := identify_token(lexeme):
            tokens.append(Token(token_type, lexeme, None, line))
            lexeme = ""

    return tuple(tokens)


def identify_token(lexeme: str) -> TokenType | None:
    try:
        return TokenMapping[lexeme]
    except KeyError:
        return None
