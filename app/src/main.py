######################################################################
#                              APP V1                                #
######################################################################

from pathlib import Path

import fire
from PIL import Image
from torch import Tensor

ROOT_PATH = Path("/Users/nickybangs/gh/image_to_text")
DEFAULT_IM_PATH = ROOT_PATH / "app" / "src" / "lib" / "input"


# double check what preprocessing they do in fastai..
# this would be the entry point for making sure image looks correct
def preprocess_image(im: Image) -> Tensor:
    """
    Process the given Image to match expected characteristics of input.
    Return a Tensor of the image data
    """
    im.convert("L")
    image_tensor = Tensor(im.getdata())
    image_tensor.div_(255)
    return image_tensor


def main(image: str, image_path=Path(DEFAULT_IM_PATH)):
    im = Image.open(image_path / image)
    return preprocess_image(im)


if __name__ == "__main__":
    fire.Fire(main)
