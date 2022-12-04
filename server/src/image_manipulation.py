from PIL import Image
from os import listdir, rename
from os.path import abspath
from random import randint
from config import Config

path = abspath(Config.CHARACTER_IMAGES_DIRECTORY_PATH)
images = [f for f in listdir(path)]


def resize_images(size: tuple[int, int] = (256, 256)) -> None:
    for i in images:
        img = Image.open(path + i)
        img = img.resize(size)
        img.save(path + i)


def rename_images() -> None:
    used_names = []

    def get_random_name():
        name = "_".join(names[randint(1, len(names) - 1)].split(","))[:-2]
        if name in used_names:
            return get_random_name()
        else:
            used_names.append(name)
            return name

    with open(Config.CHARACTER_NAMES_FILE_PATH, "r") as f:
        names = f.readlines()
        for i in images:
            rename(path + i, path + get_random_name() + ".png")


def get_images_names():
    return [i.split(".")[0] for i in images]


def get_random_image_names() -> dict[str, list[str]]:
    return get_images_names()[:24]


if __name__ == "__main__":
    print(get_images_names())
