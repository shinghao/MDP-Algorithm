class Robot():
    def __init__(self, width, height, coordinates, orientation, img):
        self.width = width
        self.height = height
        self.coordinates = coordinates
        self.orientation = orientation
        self.img = img

    def get_coordinates(self):
        return self.coordinates

    def get_orientation(self):
        return self.orientation

    def set_coordinates(self, new_coordinate):
        self.coordinates = new_coordinate

    def set_orientation(self, new_orientation):
        self.orientation = new_orientation
