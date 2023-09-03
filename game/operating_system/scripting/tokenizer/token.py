from enum import Enum


class TT(Enum):

    SEMICOLOR = 0
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

    VAR = 23
    PRINT = 24

    STRING = 25
    NUMBER = 26
    IDENTIFIER = 27

    EOF = 28


class Token(object):
    def __init__(self, type: TT, src: str, value: object, line: int) -> None:
        self.type: TT = type
        self.src: str = src
        self.value: object = value
        self.line: int = line

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f'[line {self.line}: {self.type} (s:{self.src},v:{self.value})]'
