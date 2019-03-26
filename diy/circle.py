import numpy as np
from matplotlib import pyplot as plt


class Circle:
    NO_OF_SEARCH_LINES = 5

    def __init__(self, frame):

        self.frame = frame
        self.midpoint = [0, 0]
        self.radius = 0
        self.has_circle = True

    def determine_midpoint(self):

        top_left, top_right = self.find_edges_of_top_secant()

        bottom_left, bottom_right = self.find_edges_of_bottom_secant()

        top_right, bottom_left = self.length_check(top_right, top_left, bottom_right, bottom_left, offset=2)

        self.midpoint[0] = (top_right[0] + bottom_left[0])/2
        self.midpoint[1] = (top_right[1] + bottom_left[1])/2

        return bottom_right

    def length_check(self, top_right, top_left, bottom_right, bottom_left, offset):

        top_length = top_right[1] - top_left[1]
        top_mid_point = 1/2*(top_right[1] + top_left[1])
        bottom_length = bottom_right[1] - bottom_left[1]
        bottom_mid_point = 1/2*(bottom_right[1] - bottom_left[1])

        if abs(top_length - bottom_length) > 20 or abs(top_mid_point - bottom_mid_point) > 20:

            # # todo only for debugging purposes
            # print(top_length, bottom_length, top_mid_point, bottom_mid_point)
            # fig, ax = plt.subplots()
            # ax.imshow(self.frame, cmap='gray')
            # ax.autoscale(False)
            # ax.scatter(top_right[1], top_right[0], color='r')
            # ax.scatter(top_left[1], top_left[0], color='r')
            # ax.scatter(bottom_left[1], bottom_left[0], color='g')
            # ax.scatter(bottom_right[1], bottom_right[0], color='g')
            # plt.show()

            if top_right[0] > bottom_right[0]:
                print('WARNING something is wrong - top and bottom have passed each other')

            if top_length < bottom_length:
                top_left, top_right = self.find_edges_of_top_secant(offset=offset)
                top_right, bottom_left = self.length_check(top_right, top_left, bottom_right, bottom_left, offset=offset+20)

            elif bottom_length < top_length:
                bottom_left, bottom_right = self.find_edges_of_bottom_secant(offset=offset)
                top_right, bottom_left = self.length_check(top_right, top_left, bottom_right, bottom_left, offset=offset+20)

        return top_right, bottom_left

    def find_edges_of_top_secant(self, offset=0):

        top_left = []
        top_right = []

        mid_pixel = int(self.frame.shape[0]/2)

        for line in range(offset, self.NO_OF_SEARCH_LINES + offset):
            for pixel in range(self.frame.shape[1]):

                if self.frame[line, pixel] > 0:
                    if pixel < mid_pixel:
                        top_left.append([line, pixel])
                    elif pixel > mid_pixel:
                        top_right.append([line, pixel])

        if len(top_left) == 0 or len(top_right) == 0:
            if offset > 200:
                raise TypeError("no circle could be found in this image")
            top_left, top_right = self.find_edges_of_top_secant(offset=offset + 20)

        top_left = np.amax(top_left, axis=0)
        top_right = np.amin(top_right, axis=0)

        return top_left, top_right

    def find_edges_of_bottom_secant(self, offset=0):

        bottom_right = []
        bottom_left = []

        mid_pixel = int(self.frame.shape[0]/2)

        for line in range(self.frame.shape[0]-self.NO_OF_SEARCH_LINES-offset, self.frame.shape[0]-offset):
            for pixel in range(self.frame.shape[1]):

                if self.frame[line, pixel] > 0:
                    if pixel < mid_pixel:
                        bottom_left.append([line, pixel])
                    elif pixel > mid_pixel:
                        if bottom_left and bottom_left[-1][0] != line:
                            continue
                        bottom_right.append([line, pixel])

        if len(bottom_left) == 0 or len(bottom_right) == 0:
            if offset > 200:
                raise TypeError("no circle could be found in this image")
            bottom_left, bottom_right = self.find_edges_of_bottom_secant(offset=offset + 20)

        bottom_left = np.amax(bottom_left, axis=0)
        bottom_right = np.amin(bottom_right, axis=0)

        return bottom_left, bottom_right

    def determine_radius(self, circle_point):

        delta_x = abs(self.midpoint[1] - circle_point[1])
        delta_y = abs(self.midpoint[0] - circle_point[0])

        # todo make this be majority vote over several points along middle (for long axis)

        self.radius = np.sqrt(delta_x**2 + delta_y**2)

        if self.radius < (1/2.5)*(self.frame.shape[1]):
            raise TypeError("no circle could be found in this image")

        return self.radius

