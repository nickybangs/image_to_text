######################################################################
#                              APP V1                                #
######################################################################

import fire
from pathlib import Path
from PIL import Image

ROOT_PATH = Path('/Users/nickybangs/gh/image_to_text')

def main(image):
    im = Image.open(ROOT_PATH/'app'/'src'/'lib'/'input'/image)
    im.convert('L')
    im.show()

if __name__ == '__main__':
    fire.Fire(main)
