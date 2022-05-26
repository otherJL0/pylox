from pylox import scanner, tokens


def test_token_identification():
    source: str = ""
    expected_tokens: list[tokens.Token] = []
    for lexeme, token_type in tokens.TokenMapping.items():
        source += lexeme
        expected_tokens.append(tokens.Token(token_type, lexeme, None, 1))
    actual_tokens: tuple[tokens.Token, ...] = scanner.parse(source)
    assert tuple(expected_tokens) == actual_tokens
