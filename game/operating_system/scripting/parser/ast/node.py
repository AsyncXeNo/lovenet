from __future__ import annotations

from abc import abstractmethod

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.operating_system.scripting.parser.ast.visitor import Visitor, T

from game.operating_system.scripting.scanner.token import Token


class Expression(object):
    @abstractmethod
    def accept(self, visitor: Visitor[T]) -> T: pass


class Literal(Expression):
    def __init__(self, value: object) -> None:
        self.value: object = value

    def accept(self, visitor: Visitor[T]) -> T:
        return visitor.visit_literal(self)


class Grouping(Expression):
    def __init__(self, expression: Expression) -> None:
        self.expression: Expression = expression

    def accept(self, visitor: Visitor[T]) -> T:
        return visitor.visit_grouping(self)


class Unary(Expression):
    def __init__(self, operator: Token, right: Expression) -> None:
        self.operator: Token = operator
        self.right: Expression = right

    def accept(self, visitor: Visitor[T]) -> T:
        return visitor.visit_unary(self)


class Binary(Expression):
    def __init__(self, left: Expression, operator: Token, right: Expression) -> None:
        self.left: Expression = left
        self.operator: Token = operator
        self.right: Expression = right

    def accept(self, visitor: Visitor[T]) -> T:
        return visitor.visit_binary(self)
