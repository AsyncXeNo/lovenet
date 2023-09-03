import config as _

from engine.game import Game
from engine.game_object.game_object import TestGameObject


def main():
    game: Game = Game('LÖVENET')
    TestGameObject(game)
    game.run()


if __name__ == '__main__':
    main()
