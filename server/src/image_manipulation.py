import random
from PIL import Image
from os import listdir, rename
from os.path import abspath
from config import Config

path = abspath(Config.CHARACTER_IMAGES_DIRECTORY_PATH) + "/"
images = [f for f in listdir(path)]
with open("./mock_names.csv", "r") as f:
    image_names = ["_".join(image_name.split(",")) for image_name in f.readlines()]

def resize_images(size: tuple[int, int] = (256, 256)) -> None:
    for i in images:
        print(i, " resized.")
        img = Image.open(path + i)
        img = img.resize(size)
        img.save(path + i)

def rename_images() -> None:
    """Rename all images in directory to consecutive numbers. 1.png, 2.png,...3.png"""
    for nr, i in enumerate(images):
        rename(path + i, path + str(nr) + ".png")

def get_random_image_names() -> list[tuple[str, str]]:
    _names = [image_names[random.randint(0, len(image_names)-1)] for _ in range(24)]
    _images = [images[random.randint(0, len(images)-1)] for _ in range(24)]
    return list(zip(_names, _images)), _names

if __name__ == "__main__":
    # resize_images((128,128))
    print(get_random_image_names())
