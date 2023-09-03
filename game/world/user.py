from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.world.cyborg import Cyborg


class User(object):
    def __init__(self, name: str, password: str, cyborg: Cyborg) -> None:
        self.name: str = name
        self.password: str = password
        self.cyborg: Cyborg = cyborg
