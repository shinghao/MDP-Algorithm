import Constants


class Obstacle:
    def __init__(self, x_coordinates, y_coordinates, dir):
        self.coordinates = x_coordinates, y_coordinates
        self.dir = dir

    def set_direction(self, dir):
        self.dir = dir

    def get_direction(self):
        return self.dir

    def get_coordinates(self):
        return self.coordinates
