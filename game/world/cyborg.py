import pygame

from engine.utils.math.vector import Vector2
from engine.game import Game
from engine.game_object.game_object import GameObject
from engine.graphics import Surface, Graphics, Position


class Cyborg(GameObject):
    def __init__(self, game: Game, tags: list[str] = []) -> None:
        super().__init__(game, tags)

        self.__pos: Position = Position(100, 100)
        
        self.__surface: Surface = Surface(self.__pos, (40, 100))
        self.__surface_id: str = Graphics.subscribe(self.__surface)

    def update(self, delta: float) -> None:
        move = Vector2(0, 0)
        
        if self._game.input_handler.any_pressed(pygame.K_UP, pygame.K_w):
            move.y = -1
        if self._game.input_handler.any_pressed(pygame.K_DOWN, pygame.K_s):
            move.y = 1
        if self._game.input_handler.any_pressed(pygame.K_LEFT, pygame.K_a):
            move.x = -1
        if self._game.input_handler.any_pressed(pygame.K_RIGHT, pygame.K_d):
            move.x = 1

        move = move.normalize()
        move = move.scale(500 * delta)
        move = move.round()

        self.__pos.move(int(move.x), int(move.y))
            
    
    def render(self) -> None:
        self.__surface.fill(pygame.Color('gold'))
