from region import Region


class RegionsManager:

    def __init__(self):
        self.regions = None
        self.id_set = []

        self.current_region = None

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
        pass

    def add_neighbour(self, neighbour):
        pass

    def set_tag(self, tag):
        self.current_region.set_tag(tag)
