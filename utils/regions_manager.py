import numpy as np

from region import Region


class RegionsManager:

    def __init__(self, mask_size):
        self.regions = []
        self.id_set = []

        self.current_region = None
        self.mask = np.zeros(mask_size, np.int8)

    def load_from_file(self, file):
        pass

    def save_to_file(self, file):
        # use a pickle object ? or a .txt file to parse ? or a .py file to run ?
        pass

    def generate_id(self):
        """
        Create a new unused id for a new region
        :return: the id
        """
        if self.id_set:
            return max(self.id_set) + 1
        else:
            # starting at 1. 0 is a value reserved to unattributed territories.
            return 1

    def create_new_region(self):
        """
        Begin the creation of a new region.
        :return:
        """
        new_id = self.generate_id()
        self.current_region = Region(new_id)

    def add_seed(self, seed):
        """
        Add a seed to the current region, if it is not already within another one.
        :param seed: the (regular) (x, y) coordinate of the seed
        :return: True if added, else False
        """
        # TODO : check if sea / out of the map
        is_new_seed = self.is_new_seed(seed)
        if is_new_seed:
            self.current_region.add_seed(seed)
        return is_new_seed

    def add_neighbour(self, neighbour):
        """
        Add a neighbouring relationship between the current region and the one represented by the seed
        :param neighbour: the seed (x, y) representing a neighbour (can be any point within its boundaries)
        :return:
        """
        self.current_region.add_neighbour(neighbour)

    def register_current_region(self):
        """
        When the region's parameters are entered, save it to the list and prepare a new empty one.
        :return:
        """
        self.regions.append(self.current_region)
        self.current_region = None

    def set_tag(self, tag):
        """
        Set the current region's tag (acronym)
        :param tag: A (less than 3 letters long) string
        :return:
        """
        self.current_region.set_tag(tag)

    def is_new_seed(self, seed):
        """
        Is the position described by seed free to be allocated to a region ?
        :param seed: An (x, y) coordinate
        :return: True if free, False if not
        """
        return self.mask[seed[0] + 1, seed[1] + 1] == 0

    def update_mask(self, new_mask):
        """
        Add the flood filled territory described by new_mask to the general mask
        :param new_mask: the mask describing the added territory
        :return:
        """
        self.mask[new_mask == 1] = self.current_region.get_id()
