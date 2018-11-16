from PIL import Image
import pytesseract

IMAGE = 'data/eng.Fixedsys.exp2.png'
IMAGE = 'data/base_image_3.png'

# Simple image to string
print(pytesseract.image_to_string(IMAGE, lang='Fixedsys'))

# Get bounding box estimates
# print(pytesseract.image_to_boxes(IMAGE, lang='Fixedsys'))

# Get verbose data including boxes, confidences, line and page numbers
# print(pytesseract.image_to_data(IMAGE))

# Get information about orientation and script detection
# print(pytesseract.image_to_osd(IMAGE))
