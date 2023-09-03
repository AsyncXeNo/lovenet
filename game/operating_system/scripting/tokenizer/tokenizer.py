from game.operating_system.scripting.tokenizer.token import TT, Token
from game.operating_system.scripting.exceptions import ScriptError


class Tokenizer(object):
    def __init__(self, source: str) -> None:
        self.source: str = source
        self.start: int = 0
        self.current: int = 0
        self.line: int = 0

        self.tokens: list[Token] = []

    """
    MAIN
    """

    def scan_tokens(self) -> list[Token]:
        self.tokens = []

        while not self.__is_at_end():
            self.start = self.current
            self.__scan_token(self.__advance())

        self.__add_token(TT.EOF)
        return self.tokens
    
    def __scan_token(self, c: str) -> None:
        # EMPTY CHARACTERS
        if c in ' \t\r':
            return
        if c == '\n':
            self.line += 1
            return
        # SINGLE CHARACTERS
        if c == ';':
            self.__add_token(TT.SEMICOLON)
        elif c == '(':
            self.__add_token(TT.LPAREN)
        elif c == ')':
            self.__add_token(TT.RPAREN)
        elif c == '{':
            self.__add_token(TT.LBRACE)
        elif c == '}':
            self.__add_token(TT.RBRACE)
        elif c == '+':
            self.__add_token(TT.PLUS)
        elif c == '-':
            self.__add_token(TT.MINUS)
        elif c == '*':
            self.__add_token(TT.PLUS)
        # DOUBLE CHARACTERS
        elif c == '/':
            if self.__match('/'): 
                while self.__peek() != '\n': self.__advance()
            else: self.__add_token(TT.SLASH)
        elif c == '=':
            if self.__match('='): self.__add_token(TT.EQUALS_EQUALS)
            else: self.__add_token(TT.EQUALS)
        elif c == '!':
            if self.__match('='): self.__add_token(TT.NOT_EQUALS)
            else: self.__add_token(TT.NOT)
        elif c == '<':
            if self.__match('='): self.__add_token(TT.LESS_EQUALS)
            else: self.__add_token(TT.LESS)
        elif c == '>':
            if self.__match('='): self.__add_token(TT.GREATER_EQUALS)
            else: self.__add_token(TT.GREATER)
        # COMPLEX
        elif c == '"':
            self.__string()
        else:
            if c.isdigit():
                self.__number()
            elif c.isalpha():
                self.__identifier()
            else:
                raise ScriptError(f'Invalid character \'{c}\' on line {self.line}')

    def __string(self) -> None:
        while not self.__is_at_end() and self.__peek() != '"':
            if self.__peek() == '\n':
                self.line += 1
            self.__advance()

        if self.__is_at_end():
            raise ScriptError(f'Unterminated string on line {self.line}')
        
        self.__match('"')

        value: str = self.source[self.start + 1 : self.current - 1]
        self.__add_token(TT.STRING, value)

    def __number(self) -> None:
        while not self.__is_at_end() and self.__peek().isdigit():
            self.__advance()

        if self.__match('.'):
            while not self.__is_at_end() and self.__peek().isdigit():
                self.__advance()

        value: float = float(self.source[self.start : self.current])
        self.__add_token(TT.NUMBER, value)

    def __identifier(self) -> None:
        while not self.__is_at_end() and self.__peek().isalnum():
            self.__advance()

        src: str = self.source[self.start : self.current]
        ttype: TT = TT.IDENTIFIER
        if Token.keywords.get(src):
            ttype = Token.keywords[src]
        self.__add_token(ttype)


    """
    HELPERS
    """

    def __is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def __advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]
    
    def __peek(self) -> str:
        if self.__is_at_end(): return '\0'
        return self.source[self.current]
    
    def __match(self, c: str) -> bool:
        if self.__is_at_end() or self.__peek() != c: return False
        self.__advance()
        return True
    
    def __add_token(self, type: TT, value: object | None = None) -> None:
        self.tokens.append(Token(type, self.source[self.start : self.current], value, self.line))
