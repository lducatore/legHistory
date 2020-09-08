import cv2
import numpy as np

from map import Map


class WindowWidget:
    def __init__(self, size, file, window_name="Leg Map"):
        self.file = file
        self.window_name = window_name
        self.window_size = size

        self.is_moving = False
        self.edition = False
        self.current_status = -1

        self.map = Map(self.file, self.window_size)

        self.new_region_name = ""
        self.seeds = []
        self.neighbours = []

    def open_window(self):
        """
        Open the window.
        :return:
        """
        cv2.namedWindow(self.window_name)
        self.update()

    def update(self):
        """
        Update the displayed image.
        :return:
        """
        cv2.imshow(self.window_name, self.map.get_crop())

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
            self.map.set_ref_pos(x, y)
            self.is_moving = True
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.is_moving:
                self.map.move_image(x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            self.is_moving = False
            self.map.set_crop_corner(x, y)
        elif event == cv2.EVENT_RBUTTONDOWN:
            if self.current_status == 0:
                self.map.flood_fill(x, y)
                self.seeds.append(self.map.get_absolute_pos(x, y))
            elif self.current_status == 2:
                self.map.flood_fill(x, y)


        self.update()

    def manage_key(self, key):
        """
        Take care of the user's keyboard inputs.
        :param key: the pressed key's ascii code
        :return: True if the window should be closed, False otherwise
        """

        if self.edition:
            if key == 27:
                # ESC key
                self.edition = False
                self.current_status = -1
                print("Edition mode off")
            elif key == 13:
                # ENTER key
                self.current_status += 1
                self.current_status %= 3
                self.print_status()
            elif self.current_status == 1:
                self.new_region_name += chr(key).upper()
                print(chr(key).upper(), end="")

        else:
            if key == 27:
                # ESC key
                return True
            if key == ord('e'):
                self.edition = True
                print("Edition mode on")
                self.current_status = 0
                self.initialize_region()
                self.print_status()
        return False

    def initialize_region(self):
        """
        Prepare the data holder for a new region. Remove everything previously existing.
        :return:
        """
        self.new_region_name = ""
        self.seeds = []
        self.neighbours = []

    def print_status(self):
        """
        Notify the user of the current status of the edition.
        :return:
        """
        if self.current_status == -1:
            print("Error : invalid current status : not in edition mode")
        elif self.current_status == 0:
            print("Please right click on ALL THE SEEDS for the region to add. Validate with ENTER once done.")
        elif self.current_status == 1:
            print("Please enter the name of the region. Validate with ENTER once done.")
        elif self.current_status == 2:
            print("Please right click on neighbours of the region to add that are already in the database. "
                  "Validate with ENTER once done.")
        else:
            print("Error : invalid status reached.")

    def window_handler(self):
            """
            Main routine to launch the window.
            :return:
            """
            self.map.load_img()
            self.open_window()
            cv2.setMouseCallback(self.window_name, self.click_handler)
            finish = False
            while not finish:

                key = cv2.waitKey(0)

                finish = self.manage_key(key)


window_size = (1920, 1080)
file_name = "cleaned.png"
window = WindowWidget(window_size, file_name)
window.window_handler()
