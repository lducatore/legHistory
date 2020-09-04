# Collection of methods to deal with the map
import cv2
import numpy as np


# TODO : manage North Korea
def clean_map(file_name, save_to=None, colors=None, fill_with=None, is_rgb=True):
    """
    Removes pixel of value in colors from the image contained in the file_name file
    :param file_name: the file containing the image to treat
    :param save_to: where to save the result. If None, not saved.
    :param colors: the list of colors to remove from the map
    :param fill_with: color with which the pixels are to be colored
    :param is_rgb: are the provided color in rgb ?
    :return: the cleaned map
    """
    if colors is None:
        colors = [yellow, green, light_green, dark_green, red, dark_red]

    if fill_with is None:
        fill_with = np.zeros(3, np.int8)

    if is_rgb:
        list(map(lambda l: l.reverse(), colors))

    map_img = cv2.imread(file_name)
    for col in colors:
        map_img[np.all(map_img == col, axis=2)] = fill_with
    cv2.imwrite(save_to, map_img)
    return map_img


# RGB !!!
yellow = [255, 227, 89]
green = [111, 165, 87]
light_green = [149, 211, 50]
dark_green = [0, 127, 14]
red = [193, 51, 51]
dark_red = [136, 0, 21]
grey = [220, 220, 220]

if __name__ == '__main__':
    clean_map("LegMainMap.png",
              save_to="cleaned.png",
              colors=[yellow, green, light_green, dark_green, red, dark_red],
              fill_with=np.array(grey),
              is_rgb=True)
