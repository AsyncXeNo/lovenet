from abc import abstractmethod
from typing import TypeVar, Generic

from game.operating_system.scripting.parser.ast.node import Literal, Grouping, Binary, Unary, Expression

T = TypeVar('T')


class Visitor(Generic[T]):
    @abstractmethod
    def visit_literal(self, literal: Literal) -> T: pass

    @abstractmethod
    def visit_grouping(self, grouping: Grouping) -> T: pass

    @abstractmethod
    def visit_binary(self, binary: Binary) -> T: pass

    @abstractmethod
    def visit_unary(self, unary: Unary) -> T: pass


class AstPrinter(Visitor[str]):
    def visit_literal(self, literal: Literal) -> str:
        if literal.value is None:
            return 'nil'
        return str(literal.value)
    
    def visit_grouping(self, grouping: Grouping) -> str:
        return self.__parenthesize('group', grouping.expression)
    
    def visit_binary(self, binary: Binary) -> str:
        return self.__parenthesize(binary.operator.src, binary.left, binary.right)
    
    def visit_unary(self, unary: Unary) -> str:
        return self.__parenthesize(unary.operator.src, unary.right)
    
    def print(self, expression: Expression) -> None:
        print(expression.accept(self))
    
    def __parenthesize(self, name: str, *expressions: Expression) -> str:
        string: str = ''

        string += f'({name}'
        for expression in expressions:
            string += ' '
            string += expression.accept(self)
        string += ')'

        return string
