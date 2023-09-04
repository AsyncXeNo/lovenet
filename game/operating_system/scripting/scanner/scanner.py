from game.operating_system.scripting.scanner.token import TT, Token
from game.operating_system.scripting.exceptions import ScriptError


class Scanner(object):
    def __init__(self, source: str) -> None:
        self.__source: str = source
        self.__start: int = 0
        self.__current: int = 0
        self.__line: int = 1

        self.__tokens: list[Token] = []

    """
    MAIN
    """

    def scan_tokens(self) -> list[Token]:
        self.__tokens = []

        while not self.__is_at_end():
            self.__scan_token(self.__advance())
            self.__start = self.__current

        self.__add_token(TT.EOF)
        return self.__tokens
    
    def __scan_token(self, c: str) -> None:
        # EMPTY CHARACTERS
        if c in ' \t\r':
            return
        if c == '\n':
            self.__line += 1
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
                while not self.__is_at_end() and self.__peek() != '\n': self.__advance()
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
                raise ScriptError(f'Invalid character \'{c}\' on line {self.__line}')

    def __string(self) -> None:
        while not self.__is_at_end() and self.__peek() != '"':
            if self.__peek() == '\n':
                self.__line += 1
            self.__advance()

        if self.__is_at_end():
            raise ScriptError(f'Unterminated string on line {self.__line}')
        
        self.__match('"')

        value: str = self.__source[self.__start + 1 : self.__current - 1]
        self.__add_token(TT.STRING, value)

    def __number(self) -> None:
        while not self.__is_at_end() and self.__peek().isdigit():
            self.__advance()

        if self.__match('.'):
            while not self.__is_at_end() and self.__peek().isdigit():
                self.__advance()

        value: float = float(self.__source[self.__start : self.__current])
        self.__add_token(TT.NUMBER, value)

    def __identifier(self) -> None:
        while not self.__is_at_end() and self.__peek().isalnum():
            self.__advance()

        src: str = self.__source[self.__start : self.__current]
        ttype: TT = TT.IDENTIFIER
        if Token.keywords.get(src):
            ttype = Token.keywords[src]
        self.__add_token(ttype)


    """
    HELPERS
    """

    def __is_at_end(self) -> bool:
        return self.__current >= len(self.__source)

    def __advance(self) -> str:
        self.__current += 1
        return self.__source[self.__current - 1]
    
    def __peek(self) -> str:
        if self.__is_at_end(): return '\0'
        return self.__source[self.__current]
    
    def __match(self, c: str) -> bool:
        if self.__is_at_end() or self.__peek() != c: return False
        self.__advance()
        return True
    
    def __add_token(self, type: TT, value: object | None = None) -> None:
        self.__tokens.append(Token(type, self.__source[self.__start : self.__current], value, self.__line))
