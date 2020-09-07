class Region:

    def __init__(self, acronym, identifier, seeds, neighbours, complete_name=None):

        self.tag = acronym
        self.id = identifier
        self.seeds = seeds
        self.neighbours = neighbours
        self.complete_name = complete_name

    def string_for_creation(self):
        return "Region({0}, {1}, {2}, {3}, {4})".format(self.tag, self.id, self.seeds, self.neighbours, self.complete_name)

    def add_neighbour(self, new_neighbour):
        if new_neighbour not in self.neighbours:
            self.neighbours.append(new_neighbour)

    def add_seed(self, new_seed):
        self.seeds.append(new_seed)
        # TODO : check if redundant seed ? is it possible ?
