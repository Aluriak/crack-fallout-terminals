"""Compare the different players accross millions of games.

"""

import random
from utils import choose, words_of_size
from solver import simulate_game_silently, PLAYERS, create_game_data

BAR_SIZE = 60
NB_GAMES = 10


def simulate_benchmarkable_game(players:[callable]=PLAYERS, nb_games:int=NB_GAMES, **kwargs):
    """Simulate a game with words of given size.

    """

    for nb_game in range(nb_games):
        ratio = int(round(BAR_SIZE * (nb_game / nb_games), 0))
        print('\r[' + (ratio * '#').ljust(BAR_SIZE) + ']', end='', flush=False)
        words, key = create_game_data(**kwargs)
        yield tuple(
            simulate_game_silently(player, dict(words), key)
            for player in players
        )
    print()


def make_data(players:[callable]=PLAYERS, **kwargs):
    players = tuple(players)
    players_idx = range(len(players))
    total_games = {p.__name__: [] for p in players}  # player: [score]
    for scores in simulate_benchmarkable_game(players, **kwargs):
        for score, player in zip(scores, players):
            total_games[player.__name__].append(score)

    print(total_games)



if __name__ == '__main__':
    make_data()
