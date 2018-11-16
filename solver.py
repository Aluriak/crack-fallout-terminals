"""Module that implement the solving routines for the Fallout terminal puzzle.

Puzzle is:
Words (at least 5, no more than 100) are given.
One of them is the 'key'.
Player win if it gives the key before the 5-th try (therefore, 4 words can be tested).

If player gives a word that is not the key,
he gain knowledge about how many letters are placed at the same place.
(see compute_score for exact definition)

"""


import random
from utils import choose, words_of_size
from collections import Counter


MAX_ATTEMPTS = 4


def simulate_game(player:callable, word_size:int=8, min_words:int=7, max_words:int=15):
    """Simulate a game with words of given size.

    Return the number of attempts made before finding it, or 0 if not found.

    """
    words = tuple(words_of_size(word_size))
    words = {w: None for w in choose(random.randint(min_words, max_words), words, len(words))}
    key = next(iter(choose(1, words.keys(), len(words))))
    def print_words():
        print('WORDS:')
        for word, score in words.items():
            print('\t' + word + (f' [{score}]' if score else ''))

    remaining_attempts = MAX_ATTEMPTS
    while remaining_attempts > 0:
        tested_word = next(player(words, remaining_attempts))
        print_words()
        print('Word tested >', tested_word)
        words[tested_word] = compute_score(tested_word, key)
        if tested_word == key:
            total_attempts = MAX_ATTEMPTS - remaining_attempts + 1
            print(f'Success in {total_attempts} attempts !')
            return total_attempts
        else:
            print('Access denied.')
            print(f'{words[tested_word]}/{len(key)} complete.')
            remaining_attempts -= 1
    assert tested_word != key
    print('Failure. The word to find was "' + key + '"')
    return 0




def compute_score(word:str, key:str) -> int:
    """Return the number of valid letters"""
    assert len(word) == len(key)
    return sum(1 for ca, cb in zip(word, key) if ca == cb)


def valid_candidates(words:{str: int}, remaining_attempts:int) -> [str]:
    """Yield the words that can be tested.
    If only one is returned, it is the key.
    If none is returned, it is a bug.

    words -- mapping from candidate word to its score, or None if not known.

    """
    scored_words = {w: s for w, s in words.items() if s is not None}
    if not scored_words:  # no enough data: every word is candidate
        yield from words
        return

    for word in words:
        if word in scored_words: continue
        if all(score == compute_score(word, scored_word)
               for scored_word, score in scored_words.items()):
            # There is exactly as much common letters as the score.
            #  May be good to try.
            yield word


def best_candidates(words:{str: int}, remaining_attempts:int) -> [str]:
    """Yield the words that can should tested (among the words than can be).
    If only one is returned, it is the key.
    If none is returned, it is a bug.

    words -- mapping from candidate word to its score, or None if not known.

    """
    candidates = tuple(valid_candidates(words, remaining_attempts))
    print('#candidates:', len(candidates))
    print(' candidates:', ', '.join(candidates))
    if len(candidates) <= 1:  # the last candidate is your best shot
        yield from candidates
        return
    # for each position, count the available letters
    position_distributions = map(Counter, zip(*candidates))
    print('DISTRIBUTIONS:', tuple(position_distributions))
    # TODO: ALT: get the word that would discard the most other words if found invalid.

    # while nothing is implemented…
    yield from candidates


if __name__ == '__main__':
    simulate_game(player=best_candidates)
