"""Global logic of the overall program.

"""


import solver
import interpreter
import watcher
from itertools import starmap


def new_game() -> dict:
    "Return a new dict, ready for a new game !"
    return {}

def with_solver_advices(interpretation:dict) -> dict:
    """Return the interpretation, with new fields like 'proposition'
    and 'other propositions', where one can find the best words
    to try, according to the different players.

    """

    interpretation = dict(interpretation)
    interpretation['other propositions'] = tuple(solver.best_candidates(interpretation['words'], interpretation['best remaining attempts'], silent=True))
    if interpretation['other propositions']:
        interpretation['proposition'] = interpretation['other propositions'][0]
    else:  # nothing was found by player…
        interpretation['proposition'] = None
    return interpretation


def on_new_screenshot(fname):
    global game_state
    interpretation = interpreter.interpret(fname)
    if interpretation['problems']:  # probably a non-game screenshot
        game_state = new_game()
        print("Well, i will wait for the next run. Have fun !")
        print()
        return
    # interpretation available
    interpretation = with_solver_advices(interpretation)

    if not game_state:  # no previous informations
        remaining = interpretation['remaining attempts']
        word_repr = lambda w, s: w + (f' [{s}]' if s is not None else '')
        print(f"I see the following words:", ', '.join(starmap(word_repr, interpretation['words'].items())))
        print(f"We got {' or '.join(map(str, remaining))} tr{'ies' if any(v>1 for v in remaining) else 'y'} left.")
        if interpretation['scored words']:
            print(f"Previous results: " + ', '.join(starmap(word_repr, interpretation['scored words'].items())))
        if interpretation['proposition'] is None:
            print("I do not have any proposition, Sir.")
        else:
            print(f"I would propose {interpretation['proposition']}, or any of"
                  f" {', '.join(interpretation['other propositions'])}.")

    # move in archive
    shutil.move(fname, 'archived-real-data/' + os.path.basename(fname))


if __name__ == '__main__':
    print("Hello Sir,")
    print("I am ready to play !")
    game_state = new_game()  # ready to play !
    watcher.run(on_new_screenshot)
    print("So it shall ends,")
    print("Good bye Sir !")
