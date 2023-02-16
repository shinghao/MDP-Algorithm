from Pair import pair


class Obstacle:
    def __init__(self, pos: pair, dir):
        self.pos = pos
        self.dir = dir
        self.visited = False

    def set_direction(self, dir):
        self.dir = dir

    def get_direction(self):
        return self.dir

    # Pair type
    def get_pos(self):
        return self.pos
