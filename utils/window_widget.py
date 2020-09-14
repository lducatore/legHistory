import cv2
import os

from map import Map


class WindowWidget:
    def __init__(self, size, file, window_name="Leg Map"):
        self.file = file
        self.window_name = window_name
        self.window_size = size

        self.is_moving = False
        self.insertion = False
        self.current_status = -1

        self.map = Map(self.file, self.window_size)

        self.new_region_name = ""

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
                self.map.add_seed(x, y)
            elif self.current_status == 2:
                self.map.flood_fill(x, y)

        self.update()

    def manage_key(self, key):
        """
        Take care of the user's keyboard inputs.
        :param key: the pressed key's ascii code
        :return: True if the window should be closed, False otherwise
        """

        if self.insertion:
            if key == 27:
                # ESC key
                self.insertion = False
                self.current_status = -1
                print("Insertion mode off")
            elif key == 13:
                # ENTER key
                if self.current_status == 1:
                    self.map.regions.set_tag(self.new_region_name)
                elif self.current_status == 2:
                    self.current_status = -1
                    self.map.regions.register_current_region()
                    self.initialize_region()
                self.current_status += 1
                self.print_status()
            elif self.current_status == 1:
                self.new_region_name += chr(key).upper()
                print(self.new_region_name)

        else:
            if key == 27:
                # ESC key
                return True
            if key == ord('i'):
                self.insertion = True
                print("Insertion mode on")
                self.current_status = 0
                self.initialize_region()
                self.print_status()
            elif key in [ord('l'), ord('L')]:
                version = find_last_history_version()
                if version == -1:
                    print("No history file found for loading. Aborting.")
                else:
                    file = "leg_history_" + str(version)
                    print("Loading last history version under file ", file)
                    self.map.regions.load_from_file(file)
            elif key in [ord('s')]:
                version = find_last_history_version()
                file = "leg_history_" + str(version + 1)
                print("Saving history under ", file)
                self.map.regions.save_to_file(file)
            elif key == ord("d"):
                print(self.map.regions)

        return False

    def initialize_region(self):
        """
        Prepare the data holder for a new region. Remove everything previously existing.
        :return:
        """
        self.new_region_name = ""
        self.map.regions.create_new_region()

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
            self.open_window()
            cv2.setMouseCallback(self.window_name, self.click_handler)
            finish = False
            while not finish:

                key = cv2.waitKey(0)

                finish = self.manage_key(key)


def find_last_history_version():
    """
    Find the current version of leg history stored in the utils directory.
    :return: -1 if none found, else the current max number
    """
    current_max = -1
    for file in os.listdir(os.getcwd()):
        if len(file) > 12 and file[:12] == "leg_history_":
            try:
                current_max = max(int(file[12:]), current_max)
            except ValueError:
                continue
    return current_max


window_size = (1920, 1080)
file_name = "cleaned.png"
window = WindowWidget(window_size, file_name)
window.window_handler()
