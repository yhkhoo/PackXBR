# Libraries:
import os
import sys
import subprocess
import traceback

import numpy as np
from PIL import Image

import logic


def process_image(args, img_raw_path, img_scaled_path, scale_factor):
    # get image in array
    img = np.asarray(Image.open(img_raw_path).convert('RGBA'))
    img_height, img_width = img.shape[0:2]

    # tile north and south
    img_tiled_north = tile_dict[args["nTile"]](img, [1, 0, 0, 0], img_height, img_width)
    img_tiled_south = tile_dict[args["sTile"]](img, [0, 1, 0, 0], img_height, img_width)
    # merge
    img = np.vstack((img_tiled_north, img_tiled_south[img_height:]))
    # tile east and west
    img_tiled_east = tile_dict[args["eTile"]](img, [0, 0, 0, 1], img_height, img_width)
    img_tiled_west = tile_dict[args["wTile"]](img, [0, 0, 1, 0], img_height, img_width)
    # merge
    img = np.hstack((img_tiled_west[:, :img_width], img_tiled_east))

    # save
    Image.fromarray(img).save(img_scaled_path)

    # update tile-preview preview
    logic.screen.update_tile_preview(img_scaled_path)

    # xbr
    xbr(input_path=img_scaled_path, output_path=img_scaled_path, algorithm=args["algorithm"], scale_factor=scale_factor)

    # crop in
    img = np.asarray(Image.open(img_scaled_path).convert('RGBA'))
    img_height, img_width = img.shape[0:2]
    crop_height = int(img_height / 3)
    img = img[crop_height:img_height - crop_height, crop_height:img_width - crop_height]

    # save
    Image.fromarray(img).save(img_scaled_path)


def tile_GENERIC(img, direction, width, height, method):
    return np.pad(img, (
        (direction[0] * height, direction[1] * height), (direction[2] * width, direction[3] * width), (0, 0)), method)


tile_dict = {
    "void": lambda img, direction, width, height: tile_GENERIC(img, direction, width, height, "constant"),
    "wrap": lambda img, direction, width, height: tile_GENERIC(img, direction, width, height, "wrap"),
    "extend": lambda img, direction, width, height: tile_GENERIC(img, direction, width, height, "edge"),
    "mirror": lambda img, direction, width, height: tile_GENERIC(img, direction, width, height, "symmetric")
}


# Fixes directories of local files when compiled into auto-py-to-exe
def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        # noinspection PyUnresolvedReferences
        base_path = sys._MEIPASS
    except Exception:
        # If the above fails, it means we aren't compiled, so paths work normally
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# Calls ScalerTest_Windows.exe with the proper args
def xbr(input_path, output_path, algorithm, scale_factor):
    try:
        arguments = f"-{scale_factor}{algorithm} \"{input_path}\" \"{output_path}\""
        subprocess.check_output(  # launch a process with args, pausing main thread until process is finished
            "ScalerTest_Windows.exe " +  # resource_path("ScalerTest_Windows.exe") +  # call in a way that works with files packed into an exe
            arguments,  # args for xBRz on our image
            creationflags=0x08000000)  # don't show the console window doing this.
    except Exception:
        traceback.print_exc()
        exit()


if __name__ == '__main__':
    args = {
        "nTile": "mirror",
        "eTile": "mirror",
        "sTile": "mirror",
        "wTile": "mirror",
        "algorithm": "xbr"
    }
    process_image(args, "test/grass.png", "test/grass_out.png", scale_factor=4)
