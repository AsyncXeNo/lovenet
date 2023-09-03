import pygame

from engine.constants import PYGAMECONSTANTS, SETTINGS
from engine.graphics import Graphics
from engine.game_object.game_object import GameObject


class Game(object):
    def __init__(self, name: str) -> None:
        pygame.init()

        self.game_objects: list[GameObject] = []

        self.settings: dict[str, object] = SETTINGS.DEFAULT

        if self.settings.get('fullscreen', False):
            self.__screen: pygame.Surface = pygame.display.set_mode((0, 0), flags=pygame.FULLSCREEN)
        else:
            self.__screen: pygame.Surface = pygame.display.set_mode((PYGAMECONSTANTS.WINDOW.WIDTH, PYGAMECONSTANTS.WINDOW.HEIGHT))

        pygame.display.set_caption(name)

        self.__clock: pygame.time.Clock = pygame.time.Clock()
        self.__fps: int = PYGAMECONSTANTS.WINDOW.FPS
        self.__curent_frame_fps: int
        
        self.__last_frame_time: int = pygame.time.get_ticks()
        
        self.__running: bool = True

    """
    MAIN
    """

    def run(self) -> None:
        while self.__running:            
            self.__handle_events()
            if not self.__running: break
            
            self.__update()

            self.__render()

        pygame.quit()

    def change_settings(self, key: str, value: object) -> None:
        """TODO: Implement"""
        pass

    """
    Events
    """
    
    def __handle_events(self) -> None:
        for event in pygame.event.get():
            self.__handle_event(event)

    def __handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            self.__running = False

    """
    Update
    """

    def __update(self) -> None:
        delta: float = self.__get_delta()
        self.__curent_frame_fps = round(1 / delta) if delta > 0 else self.__fps
        
        for game_object in self.game_objects:
            game_object.update(delta)

    """
    Render
    """

    def __render(self) -> None:
        self.__display_fps()

        for game_object in self.game_objects:
            game_object.render()

        Graphics.render_surfaces(self.__screen)
        
        pygame.display.flip()
        self.__screen.fill(pygame.Color('black'))
        self.__clock.tick(self.__fps)

    def __display_fps(self) -> None:
        Graphics.print(
            text=f'FPS: {self.__curent_frame_fps}',
            font_name="Fira Code",
            font_size=15, 
            color=(0, 255, 0, 255), 
            pos=(10, 10), 
            surface=self.__screen)

    """
    HELPERS
    """

    def is_running(self) -> bool:
        return self.__running
     
    def __get_delta(self) -> float:
        current_time: int = pygame.time.get_ticks()
        delta_time: float = (current_time - self.__last_frame_time) / 1000  # (Current ticks - Last recorded ticks) / 1000
        self.__last_frame_time = current_time

        return delta_time
