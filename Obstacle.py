import Constants


class Obstacle:
    def __init__(self, x_coord, y_coord, dir):
        self.coordinates = x_coord, y_coord
        self.dir = dir
        self.visited = False

    def set_direction(self, dir):
        self.dir = dir

    def get_direction(self):
        return self.dir

    def get_coordinates(self):
        return self.coordinates
