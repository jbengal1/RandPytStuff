import numpy as np

class Grid:
    def __init__(self, array=np.zeros([3, 3]), start=[0, 0], target=[3, 3]):
        self.array = arrays
        self.array_indices =
        self.g_array = array
        self.h_array = array
        self.f_array = self.p_array + self.h_array
        self.start = start
        self.target = target
        self.array_size = len(self.array)

    def setGrid(self, array):
        self.array = array
        self.array_size = len(self.array)

    def setStart(self, start):
        self.start = start

    def setTarget(self, target):
        self.target = target

    # def calcG(self, position):
    #
    #
    # def calcH(self, position):
    #     pass

    def calcG_array(self):
        x_dis = abs(self.start - self.array)
        self.g_array = np.sqrt(self)

    def calcH_array(self):
        pass


def main():
    grid = Grid()



main()
