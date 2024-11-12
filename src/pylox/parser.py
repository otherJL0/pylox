from pylox.expr import Binary, Expr, Grouping, Literal, Unary
from pylox.stmt import Expression, Print, Stmt
from pylox.token import Token, TokenType


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens: list[Token] = tokens
        self.current: int = 0

    @property
    def peek(self) -> Token:
        return self.tokens[self.current]

    @property
    def is_at_end(self) -> bool:
        return self.peek.token_type == TokenType.EOF

    def advance(self) -> Token:
        if not self.is_at_end:
            self.current += 1
        return self.tokens[self.current - 1]

    def check(self, token_type: TokenType) -> bool:
        if self.is_at_end:
            return False
        return self.peek.token_type == token_type

    def consume(self, token_type: TokenType, message: str) -> Token:
        if self.check(token_type):
            return self.advance()
        raise RuntimeError(message)

    def expression(self) -> Expr:
        return self.equality()

    def statement(self) -> Stmt:
        token = self.tokens[self.current]
        match token.token_type:
            case TokenType.PRINT:
                _ = self.advance()
                return self.print_statement()
            case _:
                return self.expression_statement()

    def print_statement(self) -> Print:
        value = self.expression()
        _ = self.consume(TokenType.SEMICOLON, "Expect `;` after value")
        return Print(value)

    def expression_statement(self) -> Expression:
        expr = self.expression()
        _ = self.consume(TokenType.SEMICOLON, "Expect `;` after expression")
        return Expression(expr)

    def equality(self) -> Expr:
        expr = self.comparison()
        while True:
            token = self.tokens[self.current]
            match token.token_type:
                case TokenType.BANG_EQUAL | TokenType.EQUAL_EQUAL:
                    operator = token
                    _ = self.advance()
                    right = self.comparison()
                    expr = Binary(expr, operator, right)
                case _:
                    break
        return expr

    def comparison(self) -> Expr:
        expr = self.term()

        while True:
            token = self.tokens[self.current]
            match token.token_type:
                case (
                    TokenType.GREATER
                    | TokenType.GREATER_EQUAL
                    | TokenType.LESS
                    | TokenType.LESS_EQUAL
                ):
                    operator = token
                    _ = self.advance()
                    right = self.term()
                    expr = Binary(expr, operator, right)
                case _:
                    break
        return expr

    def term(self) -> Expr:
        expr = self.factor()

        while True:
            token = self.tokens[self.current]
            match token.token_type:
                case TokenType.MINUS | TokenType.PLUS:
                    operator = token
                    _ = self.advance()
                    right = self.factor()
                    expr = Binary(expr, operator, right)
                case _:
                    break
        return expr

    def factor(self) -> Expr:
        expr = self.unary()

        while True:
            token = self.tokens[self.current]
            match token.token_type:
                case TokenType.SLASH | TokenType.STAR:
                    operator = token
                    _ = self.advance()
                    right = self.unary()
                    expr = Binary(expr, operator, right)
                case _:
                    break
        return expr

    def unary(self) -> Expr:
        token = self.tokens[self.current]
        match token.token_type:
            case TokenType.BANG | TokenType.MINUS:
                operator = token
                _ = self.advance()
                right = self.unary()
                return Unary(operator, right)
            case _:
                return self.primary()

    def primary(self) -> Expr:
        token: Token = self.tokens[self.current]
        match token.token_type:
            case TokenType.FALSE:
                _ = self.advance()
                return Literal(False)
            case TokenType.TRUE:
                _ = self.advance()
                return Literal(True)
            case TokenType.NIL:
                _ = self.advance()
                return Literal(None)
            case TokenType.NUMBER | TokenType.STRING:
                literal_expr = Literal(token.literal)
                _ = self.advance()
                return literal_expr
            case TokenType.LEFT_PAREN:
                _ = self.advance()
                expr = self.expression()
                _ = self.consume(TokenType.RIGHT_PAREN, "Expected ')' after expression")
                return Grouping(expr)
            case _:
                raise RuntimeError("No token found")

    def synchronize(self):
        previous = self.tokens[self.current - 1]
        token = self.tokens[self.current]
        while not self.is_at_end:
            match [previous.token_type, token.token_type]:
                case [TokenType.SEMICOLON, _]:
                    return
                case [
                    _,
                    TokenType.CLASS
                    | TokenType.FUN
                    | TokenType.VAR
                    | TokenType.FOR
                    | TokenType.IF
                    | TokenType.WHILE
                    | TokenType.PRINT
                    | TokenType.RETURN,
                ]:
                    return
                case _:
                    _ = self.advance()

    def parse(self) -> Expr | None:
        statements: list[Stmt] = []
        while not self.is_at_end:
            statements.append(self.statement())
