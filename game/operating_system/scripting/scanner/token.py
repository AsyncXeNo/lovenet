from enum import Enum


class TT(Enum):

    COMMA = -1
    SEMICOLON = 0
    LBRACE = 1
    RBRACE = 2
    LPAREN = 3
    RPAREN = 4

    PLUS = 5
    MINUS = 6
    STAR = 7
    SLASH = 8

    EQUALS = 9
    EQUALS_EQUALS = 10
    NOT = 11
    NOT_EQUALS = 12
    LESS = 13
    LESS_EQUALS = 14
    GREATER = 15
    GREATER_EQUALS = 16

    IF = 17
    ELSE = 18
    WHILE = 19
    FOR = 20
    CONTINUE = 21
    BREAK = 22
    AND = 23
    OR = 24
    TRUE = 25
    FALSE = 26

    VAR = 27
    PRINT = 28

    STRING = 29
    NUMBER = 30
    IDENTIFIER = 31
    NIL = 32

    EOF = 33


class Token(object):

    keywords = {
        "if": TT.IF,
        "else": TT.ELSE,
        "while": TT.WHILE,
        "for": TT.FOR,
        "continue": TT.CONTINUE,
        "break": TT.BREAK,
        "var": TT.VAR,
        "print": TT.PRINT,
        "nil": TT.NIL,
        "and": TT.AND,
        "or": TT.OR,
        "true": TT.TRUE,
        "false": TT.FALSE,
    }
    
    def __init__(self, type: TT, src: str, value: object, line: int) -> None:
        self.type: TT = type
        self.src: str = src
        self.value: object = value
        self.line: int = line

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f'[line {self.line}: {self.type} (s:{self.src},v:{self.value})]'
