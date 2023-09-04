from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from engine.game import Game
    

class GameObject(object):
    def __init__(self, game: Game, tags: list[str]=[]) -> None:
        self.tags: list[str] = tags
        self._game: Game = game
        self._game.game_objects.append(self)

    @abstractmethod
    def update(self, delta: float) -> None:
        pass

    @abstractmethod
    def render(self) -> None:
        pass
