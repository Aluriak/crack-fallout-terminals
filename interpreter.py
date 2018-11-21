"""Routines that call OCR and perform
some computations to get an idea of the game state.

"""

import re
import glob
from PIL import Image
import pytesseract


def crop_standard_image(img:Image) -> dict:
    """Return the 4 important blocks of texts in image format:

    The line defining the remaining attempts.
    The first and second blocks of words.
    The game state information.

    """
    def make_crop(left, upper, right, lower, img=img) -> Image:
        # arguments: left, top, right, upper
        #  (ALL ARE DISTANCE TO THE TOP/LEFT EDGE OF THE BASE IMAGE)
        width = right - left
        height = lower - upper
        return img.copy().crop((left, upper, left+width, upper+height))
    LEFT, RIGHT = 444, 1466
    UPPER, LOWER = 236, 831
    ATTEMPTS_LOWER, ATTEMPTS_RIGHT = 284, 1100
    BLOCK_UPPER = 302
    BLOCK1_LEFT, BLOCK1_RIGHT = 569, 818
    BLOCK2_LEFT, BLOCK2_RIGHT = 957, 1201
    img_attempts = make_crop(LEFT, UPPER, ATTEMPTS_RIGHT, ATTEMPTS_LOWER)
    img_block_1 = make_crop(BLOCK1_LEFT, BLOCK_UPPER, BLOCK1_RIGHT, LOWER)
    img_block_2 = make_crop(BLOCK2_LEFT, BLOCK_UPPER, BLOCK2_RIGHT, LOWER)
    img_state = make_crop(BLOCK2_RIGHT, UPPER, RIGHT, LOWER)
    return {'remaining-attempts': img_attempts, 'block1': img_block_1, 'block2': img_block_2, 'state': img_state}


def interpret_images(images:dict) -> [str, str]:
    """Return {name: interpretation}"""
    texts = {
        name: pytesseract.image_to_string(image, lang='Fixedsys')
        for name, image in images.items()
    }
    texts['words'] = texts['block1'] + texts['block2']
    del texts['block1']
    del texts['block2']
    for name, text in texts.items():
        yield name, globals()['interpret_' + name.replace('-', '_')](text)


def interpret_words(raw_text:str) -> [str]:
    "Return the words in block1"
    print('WORDS:', '\n' + raw_text)
    accepted_letters = range(ord('A'), ord('Z')+1)
    def normalized_char(c:str) -> str:
        if ord(c.upper()) in accepted_letters:
            return '*' if c.islower() else c
        return ' '
    possibles = ''.join(map(normalized_char, raw_text.replace('\n', ''))).split()
    return tuple(w for w in possibles if len(w) > 3)


def interpret_state(raw_text:str) -> dict:
    "Return the words in block1"
    ret = {}  # word: score
    last_word = None
    for line in raw_text.splitlines():
        if not line:  continue
        line = line if line.strip()[0].isalpha() else line[1:]
        REGEX_SCORE = re.compile(r"([0-9]+)\/([0-9]+)")
        match = REGEX_SCORE.match(line)
        if match:
            score, key_size = map(int, match.groups())
            if last_word and len(last_word) != key_size:
                print(f"WARNING: word {last_word} is of size {len(last_word)}, but score is given on size {key_size}. I will ignore this.")
            ret[last_word] = score
        elif 'Entry denied' in line:
            pass  # we do not care about this one
        elif sum(1 if c.isupper() else 0 for c in line) > 4:  # at least 4 letters in uppercase
            last_word = line
    return ret

def interpret_remaining_attempts(raw_text:str) -> [int]:
    "Return the possible numbers of remaining guesses"
    if not raw_text:
        return ()
    if raw_text[0].isnumeric():
        first_guess = int(raw_text[0])
    else:
        first_guess = None
    secnd_guess = raw_text.count('■')
    if not first_guess:
        return secnd_guess,
    if secnd_guess > 0 and secnd_guess != first_guess:
        return first_guess, secnd_guess
    return first_guess,  # both agree, or secnd_guess is lost


def interpret(fname:str) -> dict:
    "Interpret image of given filename, return a dictionnary ready to be used."
    img = Image.open(fname)
    first_interpretation = dict(interpret_images(crop_standard_image(img)))
    interpretation = first_interpretation
    interpretation['problems'] = set()
    # decide if the screenshot was taken during a game
    if all(estimation not in range(1, 5) for estimation in first_interpretation['remaining-attempts']):
        interpretation['problems'].add('bad attempts estimation')
    if len(first_interpretation['words']) < 4:
        interpretation['problems'].add('too few words')
    # decide some values
    interpretation['remaining attempts'] = interpretation['remaining-attempts']
    interpretation['best remaining attempts'] = max(1, min(interpretation['remaining-attempts']))
    interpretation['words'] = {
        word: interpretation['state'].get(word, None)
        for word in interpretation['words']
    }
    interpretation['scored words'] = interpretation['state']
    return interpretation


if __name__ == '__main__':
    imagefile = next(iter(glob.glob('real-data/*.png')))
    image = Image.open(imagefile)
    print('IMAGE:', imagefile)
    images = crop_standard_image(image)

    for name, img in images.items():
        print('\n\n' + '#' * 120)
        print('IMAGE:', name)
        img.save(f'real-data/temp/{name}.png')
        print(pytesseract.image_to_string(img, lang='Fixedsys'))

    for name, interpretation in interpret_images(images):
        print(name + ':', interpretation)
