from __future__ import annotations

import pygame


class Input(object):
    _instance = None

    def __new__(cls) -> Input:
        if cls._instance is None:
            cls._instance = super(Input, cls).__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        self.key_state: dict[int, bool] = {}
        self.mouse_button_state: dict[int, bool] = {}
        self.mouse_position: tuple[int, int] = (0, 0)

        self.pressed_this_frame: list[int] = []  # Keys which have been just pressed this frame
        self.up_this_frame: list[int] = []  # Keys which have been unpressed this frame

        self.modifiers: dict[str, bool] = {
            'ctrl': False,
            'alt': False,
            'shift': False
        }

    def any_pressed(self, *keys: int) -> bool:
        for key in keys:
            if self.key_state.get(key):
                return True
        return False

    def pressed(self, *keys: int) -> bool:
        for key in keys:
            if not self.key_state.get(key):
                return False
        return True

    def update(self, events: list[pygame.event.Event]) -> None:
        """Update input state based on a list of pygame events."""

        self.pressed_this_frame.clear()
        self.up_this_frame.clear()

        for event in events:

            # KEYDOWN
            if event.type == pygame.KEYDOWN:
                self.key_state[event.key] = True
                self.pressed_this_frame.append(event.key)\

                if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    self.modifiers['ctrl'] = True
                elif event.key == pygame.K_LALT or event.key == pygame.K_RALT:
                    self.modifiers['alt'] = True
                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.modifiers['shift'] = True
                
            # KEYUP
            elif event.type == pygame.KEYUP:
                self.key_state[event.key] = False
                self.up_this_frame.append(event.key)

                if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    self.modifiers['ctrl'] = False
                elif event.key == pygame.K_LALT or event.key == pygame.K_RALT:
                    self.modifiers['alt'] = False
                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.modifiers['shift'] = False
            
            # MOUSEMOTION
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_position = event.pos

            # MOUSEBUTTONDOWN
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_button_state[event.button] = True
                self.pressed_this_frame.append(event.button)

            # MOUSEBUTTONUP
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_button_state[event.button] = False
                self.up_this_frame.append(event.button)


# Usage:
# input_instance = Input()
# input_instance.update(pygame.event.get())
