import glob
from PIL import Image
import pytesseract

IMAGE = 'data/base_image_3.png'
IMAGE = 'data/eng.Fixedsys.exp2.png'

# Simple image to string
# print(pytesseract.image_to_string(IMAGE, lang='Fixedsys'))

# Get bounding box estimates
# print(pytesseract.image_to_boxes(IMAGE, lang='Fixedsys'))

# Get verbose data including boxes, confidences, line and page numbers
# print(pytesseract.image_to_data(IMAGE))

# Get information about orientation and script detection
# print(pytesseract.image_to_osd(IMAGE))



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
    texts['blocks'] = texts['block1'] + texts['block2']
    del texts['block1']
    del texts['block2']
    for name, text in texts.items():
        yield name, globals()['interpret_' + name.replace('-', '_')](text)


def interpret_blocks(raw_text:str) -> [int]:
    "Return the words in block1"
    accepted_letters = range(ord('A'), ord('Z')+1)
    return ''.join(
        c if ord(c.upper()) in accepted_letters else ' '
        for c in raw_text.replace('\n', '')
    ).split()

def interpret_state(raw_text:str) -> [int]:
    "Return the words in block1"
    return raw_text

def interpret_remaining_attempts(raw_text:str) -> [int]:
    "Return the possible numbers of remaining guesses"
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


def debug_print_images(images:dict):
    for name, img in images.items():
        print('\n\n' + '#' * 120)
        print('IMAGE:', name)
        img.save(f'real-data/{name}.png')
        print(pytesseract.image_to_string(img, lang='Fixedsys'))


if __name__ == '__main__':
    imagefile = next(iter(glob.glob('real-data/*.png')))
    image = Image.open(imagefile)
    print('IMAGE:', imagefile)
    images = crop_standard_image(image)
    for name, interpretation in interpret_images(images):
        print(name + ':', interpretation)
