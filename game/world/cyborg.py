from game.world.user import User


class Cyborg(object):
    def __init__(self) -> None:
        """TODO: Implement"""
        pass

    def create_user(self, username: str, password: str) -> None:
        User(username, password, self)
