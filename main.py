import config as _

from engine.game import Game
from game.world.cyborg import Cyborg


def main():
    game: Game = Game('LÖVENET')
    Cyborg(game=game)
    game.run()


if __name__ == '__main__':
    main()
