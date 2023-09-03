from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from engine.game import Game

import pygame
from loguru import logger

from engine.graphics import Surface, Graphics


class GameObject(object):
    def __init__(self, game: Game, tags: list[str]=[]) -> None:
        self.tags: list[str] = tags
        game.game_objects.append(self)

    @abstractmethod
    def update(self, delta: float) -> None:
        pass

    @abstractmethod
    def render(self) -> None:
        pass


class TestGameObject(GameObject):
    def __init__(self, game: Game, tags: list[str]=[]) -> None:
        super().__init__(game, tags)

        self.surface: Surface = Surface((100, 100), (100, 100))
        Graphics.subscribe(self.surface)

    def update(self, delta: float) -> None:
        logger.debug('update')

    def render(self) -> None:
        self.surface.fill(pygame.Color('red'))
