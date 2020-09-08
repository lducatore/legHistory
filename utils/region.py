class Region:

    def __init__(self, identifier, acronym=None, seeds=None, neighbours=None, complete_name=None):
        """
        :param identifier: unique id to identify the region. It is the role of the region manager to ensure uniqueness.
        :param acronym: 2 or 3 letters acronym that describes the region within leg.
        :param seeds: set of coordinates, each one describing an enclosed part of the region
        :param neighbours: set of regions that border the region
        :param complete_name: complete formal name, for better readability
        """

        self.id = identifier
        self.tag = acronym
        self.seeds = seeds
        self.neighbours = neighbours
        self.complete_name = complete_name

    def string_for_creation(self):
        return "Region({0}, {1}, {2}, {3}, {4})".format(self.id, self.tag, self.seeds, self.neighbours, self.complete_name)

    def add_neighbour(self, new_neighbour):
        if new_neighbour not in self.neighbours:
            self.neighbours.append(new_neighbour)

    def add_seed(self, new_seed):
        self.seeds.append(new_seed)
        # TODO : check if redundant seed ? is it possible ? YEP, but at the manager level

    def set_tag(self, tag):
        # TODO : determine what to do if one already exist. Very dangerous method
        self.tag = tag
