import cv2


class WindowWidget:
    def __init__(self, window_size, file, window_name="Leg Map"):
        self.window_x, self.window_y = window_size
        self.file = file
        self.window_name = window_name
        self.img = None
        self.current_crop = None
        self.load_img()

        self.ref_pos = None
        self.is_moving = False
        self.crop_absolute_corner = [0, 0]

    def get_img_dimensions(self):
        """
        Get the dimensions of the image, in the classic order.
        :return: number of x pixels, number of y pixels
        """
        return len(self.img[0]), len(self.img)

    def open_window(self):
        """
        Open the window.
        :return:
        """
        cv2.namedWindow(self.window_name)
        self.update()

    def load_img(self):
        """
        Read the image from file.
        :return:
        :raise: if the file is not loaded.
        """
        self.img = cv2.imread(self.file)
        self.set_crop(0, self.window_x, 0, self.window_y)

        if self.img is None:
            raise RuntimeError("Error : no image found under filename ", self.file)

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

    def move_image(self, x, y):
        """
        Move the displayed image knowing the new relative mouse position.
        :param x: the x pos of the mouse
        :param y: the y pos of the mouse
        :return:
        """
        x_min = self.crop_absolute_corner[0] + self.ref_pos[0] - x
        y_min = self.crop_absolute_corner[1] + self.ref_pos[1] - y
        self.set_crop(x_min, x_min + self.window_x, y_min, y_min + self.window_y)

    def update(self):
        """
        Update the displayed image.
        :return:
        """
        if len(self.current_crop) and len(self.current_crop[0]):
            cv2.imshow("Leg Map", self.current_crop)

    def click_handler(self, event, x, y, flags, params):
        """
        Manage mouse behaviours.
        :param event: the event catched
        :param x: the x pos of the mouse
        :param y: the y pos of the mouse
        :param flags:
        :param params:
        :return:
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            self.ref_pos = [x, y]
            self.is_moving = True
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.is_moving:
                self.move_image(x, y)
                self.update()
        elif event == cv2.EVENT_LBUTTONUP:
            self.is_moving = False
            self.crop_absolute_corner = [self.crop_absolute_corner[0] + self.ref_pos[0] - x,
                                         self.crop_absolute_corner[1] + self.ref_pos[1] - y]

    def window_handler(self):
        """
        Main routine to launch the window.
        :return:
        """
        self.load_img()
        self.open_window()
        cv2.setMouseCallback("Leg Map", self.click_handler)
        cv2.waitKey(0)


window_size = (1920, 1080)
file_name = "cleaned.png"
window = WindowWidget(window_size, file_name)
window.window_handler()
