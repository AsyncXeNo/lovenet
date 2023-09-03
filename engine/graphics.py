from __future__ import annotations

import uuid
import os
from collections import OrderedDict

import pygame
from loguru import logger

from engine.constants import PATH


class Surface(pygame.Surface):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], flags: int = 0) -> None:
        self.pos: tuple[int, int] = pos
        super().__init__(size, flags)


class Graphics(object):

    fonts: dict[str, dict[int, pygame.font.Font]] = {}
    render_queue: OrderedDict[str, Surface] = OrderedDict()

    @staticmethod
    def render_surfaces(main: pygame.Surface) -> None:
        for surface in Graphics.render_queue.values():
            main.blit(surface, surface.pos)

    @staticmethod
    def subscribe(surface: Surface):
        id_: str = str(uuid.uuid4())
        Graphics.render_queue[id_] = surface
        return id_
        
    @staticmethod
    def print(
            text: str, 
            font_name: str,
            font_size: int, 
            color: tuple[int, int, int, int], 
            pos: tuple[int, int], 
            surface: pygame.Surface,
            antialias: bool = False
        ) -> pygame.Rect:

        font_name = f'{font_name}'
        
        font: pygame.font.Font

        if Graphics.fonts.get(font_name) and Graphics.fonts[font_name].get(font_size):
            font = Graphics.fonts[font_name][font_size]
        else:
            font_path = pygame.font.match_font(font_name) or f'{PATH.FONTS.BASE}{font_name}'
            
            if not os.path.isfile(font_path):
                font_path = pygame.font.match_font(PATH.FONTS.DEFAULT) 
                logger.warning(f'Font "{font_name}" does not exist. Using default font at {font_path}.')

            font = pygame.font.Font(font_path, font_size)
            Graphics.fonts[font_name] = { font_size : font }
        
        text_surface: pygame.Surface = font.render(text, antialias, color)
        text_rect: pygame.Rect = text_surface.get_rect()
        text_rect.topleft = pos
        
        return surface.blit(text_surface, text_rect)
    
    @staticmethod
    def draw_rect():
        """TODO: Implement"""
        pass
