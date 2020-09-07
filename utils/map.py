import cv2
import numpy as np


class Map:

    def __init__(self, file, crop_size):
        self.file = file
        self.img = None
        self.current_crop = None
        self.regions = None
        self.crop_size = crop_size
        self.crop_absolute_corner = [0, 0]
        self.ref_pos = [0, 0]

    def get_crop(self):
        """
        :return: the cropped image
        """
        return self.current_crop

    def set_crop(self, x_min, x_max, y_min, y_max):
        """
        Compute and set the crop of the map to display.
        :param x_min: minimal x pixel index to keep from the original image
        :param x_max: maximal x pixel index to keep from the original image
        :param y_min: minimal y pixel index to keep from the original image
        :param y_max: maximal y pixel index to keep from the original image
        :return:
        """
        img_x, img_y = self.get_img_dimensions()
        x_min = max(0, x_min)
        x_max = min(img_x, x_max)
        y_min = max(0, y_min)
        y_max = min(img_y, y_max)
        self.current_crop = self.img[y_min:y_max, x_min:x_max]

    def get_img_dimensions(self):
        """
        Get the dimensions of the image, in the classic order.
        :return: number of x pixels, number of y pixels
        """
        return len(self.img[0]), len(self.img)

    def load_img(self):
        """
        Read the image from file.
        :return:
        :raise: if the file is not loaded.
        """
        self.img = cv2.imread(self.file)
        self.set_crop(0, self.crop_size[0], 0, self.crop_size[1])

        if self.img is None:
            raise RuntimeError("Error : no image found under filename ", self.file)

    def set_crop_corner(self, x, y):
        """
        Set the top left corner of the new crop, as pixel coordinates in the image
        :param x: the relative x position of the mouse
        :param y: the relative y position of the mouse
        :return:
        """
        self.crop_absolute_corner = [self.crop_absolute_corner[0] + self.ref_pos[0] - x,
                                     self.crop_absolute_corner[1] + self.ref_pos[1] - y]

    def set_ref_pos(self, x, y):
        """
        Set the reference position, ie the position of the mouse when it started the current action
        :param x: the relative x position of the mouse
        :param y: the relative y position of the mouse
        :return:
        """
        self.ref_pos = [x, y]

    def flood_fill(self, seed_x, seed_y):
        """
        Flood fill the area at given coordinates.
        :param seed_x: the relative x position of the seed
        :param seed_y: the relative y position of the seed
        :return:
        """
        abs_pos = self.get_absolute_pos(seed_x, seed_y)
        mask = np.zeros((self.get_img_dimensions()[1] + 2, self.get_img_dimensions()[0] + 2), np.uint8)
        cv2.floodFill(self.img, mask, (abs_pos[0], abs_pos[1]), (0, 0, 255))

    def get_absolute_pos(self, x, y):
        """
        Get the position on the whole map of a pixel on the cropped map.
        :param x: the x position on the crop map
        :param y: the y position on the crop map
        :return: the position in the absolute system of coordinates
        """
        return self.crop_absolute_corner[0] + x, self.crop_absolute_corner[1] + y

    def move_image(self, x, y):
        """
        Move the displayed image knowing the new relative mouse position.
        :param x: the x pos of the mouse
        :param y: the y pos of the mouse
        :return:
        """
        x_min = self.crop_absolute_corner[0] + self.ref_pos[0] - x
        y_min = self.crop_absolute_corner[1] + self.ref_pos[1] - y
        self.set_crop(x_min, x_min + self.crop_size[0], y_min, y_min + self.crop_size[1])
