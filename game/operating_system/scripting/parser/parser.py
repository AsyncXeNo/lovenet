from game.operating_system.scripting.scanner.token import Token, TT
from game.operating_system.scripting.parser.ast.node import Expression, Binary, Unary, Literal, Grouping
from game.operating_system.scripting.exceptions import ScriptError


class Parser(object):
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens: list[Token] = tokens
        self.current: int = 0

    """
    MAIN
    """

    def parse(self) -> Expression:
        return self.__expression()

    def __expression(self) -> Expression:
        return self.__equality()
    
    def __equality(self) -> Expression:
        expression: Expression = self.__comparison()

        while (self.__match(TT.NOT_EQUALS, TT.EQUALS_EQUALS)):
            operator: Token = self.__previous()
            right: Expression = self.__comparison()
            expression = Binary(expression, operator, right)

        return expression
    
    def __comparison(self) -> Expression:
        expression: Expression = self.__term()

        while (self.__match(TT.GREATER, TT.GREATER_EQUALS, TT.LESS, TT.LESS_EQUALS)):
            operator: Token = self.__previous()
            right: Expression = self.__term()
            expression = Binary(expression, operator, right) 

        return expression
    
    def __term(self) -> Expression:
        expression: Expression = self.__factor()

        while (self.__match(TT.PLUS, TT.MINUS)):
            operator: Token = self.__previous()
            right: Expression = self.__factor()
            expression = Binary(expression, operator, right)

        return expression
    
    def __factor(self) -> Expression:
        expression: Expression = self.__unary()

        while (self.__match(TT.SLASH, TT.STAR)):
            operator: Token = self.__previous()
            right: Expression = self.__unary()
            expression = Binary(expression, operator, right)

        return expression

    def __unary(self) -> Expression:
        if (self.__match(TT.NOT, TT.MINUS)):
            operator: Token = self.__previous()
            right: Expression = self.__unary()
            return Unary(operator, right)
        
        return self.__primary()
    
    def __primary(self) -> Expression:
        if (self.__match(TT.FALSE)): return Literal(False)
        if (self.__match(TT.TRUE)): return Literal(True)
        if (self.__match(TT.NIL)): return Literal(None)

        if (self.__match(TT.NUMBER, TT.STRING)):
            return Literal(self.__previous().value)
        
        if (self.__match(TT.LPAREN)):
            expression: Expression = self.__expression()
            self.__consume(TT.RPAREN, 'Exprected \')\' after expression')
            return Grouping(expression)
        
        raise ScriptError(f'Line {self.__previous().line}: Expected expression')
    
    """
    HELPERS
    """

    def __is_at_end(self) -> bool:
        return self.__peek().type == TT.EOF

    def __advance(self) -> Token:
        if not self.__is_at_end():
            self.current += 1
        return self.__previous()

    def __peek(self) -> Token:
        return self.tokens[self.current]

    def __previous(self) -> Token:
        return self.tokens[self.current - 1]
    
    def __check(self, ttype: TT) -> bool:
        if self.__is_at_end():
            return False
        return self.__peek().type == ttype
    
    def __consume(self, ttype: TT, error_message: str) -> None:
        if self.__check(ttype):
            self.__advance()
            return

        raise ScriptError(f'Line {self.__previous().line}: {error_message}')

    def __match(self, *ttypes: TT) -> bool:
        for tt in ttypes:
            if (self.__check(tt)):
                self.__advance()
                return True
        return False
