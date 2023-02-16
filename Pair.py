class pair:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):  # moving grids - single point
        return pair(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return pair(self.x - other.x, self.y - other.y)

    def __mul__(self, constant):  # for direction vectors
        return pair(self.x*constant, self.y*constant)

    def get(self):
        return self.x, self.y
