import numpy as np
from matplotlib import pyplot as plt

class Circle:
    NO_OF_SEARCH_LINES = 10

    def __init__(self, frame):

        self.frame = frame
        self.midpoint = [0, 0]
        self.radius = 0
        self.has_circle = True

    def determine_midpoint(self):

        top_left, top_right = self.find_edges_of_top_secant()

        bottom_left, bottom_right = self.find_edges_of_bottom_secant()

        top_right, bottom_left = self.length_check(top_right, top_left, bottom_right, bottom_left, height_offset=2)

        self.midpoint[0] = (top_right[0] + bottom_left[0])/2
        self.midpoint[1] = (top_right[1] + bottom_left[1])/2

        return bottom_right

    def length_check(self, top_right, top_left, bottom_right, bottom_left, height_offset):

        top_length = top_right[1] - top_left[1]
        top_mid_point = 1/2*(top_right[1] + top_left[1])
        bottom_length = bottom_right[1] - bottom_left[1]
        bottom_mid_point = 1/2*(bottom_right[1] - bottom_left[1])

        if abs(top_length - bottom_length) > 20 or abs(top_mid_point - bottom_mid_point) > 200:

            print(top_length, bottom_length, top_mid_point, bottom_mid_point)

            if top_right[0] > bottom_right[0]:
                print('WARNING something is wrong - top and bottom have passed each other')

            if top_length < bottom_length:
                top_left, top_right = self.find_edges_of_top_secant(height_offset=height_offset)
                top_right, bottom_left = self.length_check(top_right, top_left, bottom_right, bottom_left, height_offset=height_offset + 20)

            elif bottom_length < top_length:
                bottom_left, bottom_right = self.find_edges_of_bottom_secant(offset=height_offset)
                top_right, bottom_left = self.length_check(top_right, top_left, bottom_right, bottom_left, height_offset=height_offset + 20)

        return top_right, bottom_left

    def position_check(self, top_right, top_left, bottom_right, bottom_left, side_offset):

        top_length = top_right[1] - top_left[1]
        bottom_length = bottom_right[1] - bottom_left[1]
        top_mid_point = (1 / 2) * (top_right[1] + top_left[1])
        bottom_mid_point = (1 / 2) * (bottom_right[1] + bottom_left[1])

        length_diff = abs(top_mid_point - bottom_mid_point)
        to_break = False

        if top_length < bottom_length:
            top_left, top_right = self.find_edges_of_top_secant(side_offset=side_offset)
        elif bottom_length < top_length:
            bottom_left, bottom_right = self.find_edges_of_bottom_secant(side_offset=side_offset)

        new_top_mid_point = (1/2) * (top_right[1] + top_left[1])
        new_bottom_mid_point = (1/2) * (bottom_right[1] + bottom_left[1])

        new_length_diff = abs(top_mid_point - bottom_mid_point)

        if abs(new_length_diff - length_diff) < 5:
            to_break = True

        return top_right, top_left, bottom_right, bottom_left, new_top_mid_point, new_bottom_mid_point, to_break

    def find_edges_of_top_secant(self, height_offset=0, side_offset=0):

        top_left = []
        top_right = []

        mid_pixel = int(self.frame.shape[0]/2)

        for line in range(height_offset, self.NO_OF_SEARCH_LINES + height_offset):
            for pixel in range(self.frame.shape[1]):

                if self.frame[line, pixel] > 0:
                    if pixel < mid_pixel:
                        top_left.append([line, pixel])
                    elif pixel > mid_pixel:
                        top_right.append([line, pixel])

        top_left = np.array(top_left)
        top_right = np.array(top_right)

        top_left.sort(axis=0)
        top_right.sort(axis=0)

        try:
            top_left = top_left[-(side_offset+1)]
            top_right = top_right[side_offset]

        except IndexError:
            if height_offset > 200 or side_offset > 800:
                raise TypeError("no circle could be found in this image")
            top_left, top_right = self.find_edges_of_top_secant(height_offset=height_offset + 20)

        return top_left, top_right

    def find_edges_of_bottom_secant(self, height_offset=0, side_offset=0):

        bottom_right = []
        bottom_left = []

        mid_pixel = int(self.frame.shape[0]/2)

        for line in range(self.frame.shape[0]-self.NO_OF_SEARCH_LINES-height_offset, self.frame.shape[0]-height_offset):
            for pixel in range(self.frame.shape[1]):

                if self.frame[line, pixel] > 0:
                    if pixel < mid_pixel:
                        bottom_left.append([line, pixel])
                    elif pixel > mid_pixel:
                        if bottom_left and bottom_left[-1][0] != line:
                            continue
                        bottom_right.append([line, pixel])

        bottom_left = np.array(bottom_left)
        bottom_right = np.array(bottom_right)

        bottom_left.sort(axis=0)
        bottom_right.sort(axis=0)

        try:

            bottom_left = bottom_left[side_offset]
            bottom_right = bottom_right[-(side_offset + 1)]

        except ValueError:
            if height_offset > 200 or side_offset > 800:
                raise TypeError("no circle could be found in this image")
            bottom_left, bottom_right = self.find_edges_of_bottom_secant(height_offset=height_offset + 20)

        return bottom_left, bottom_right

    def determine_radius(self, circle_point):

        delta_x = abs(self.midpoint[1] - circle_point[1])
        delta_y = abs(self.midpoint[0] - circle_point[0])

        self.radius = np.sqrt(delta_x**2 + delta_y**2)

        if self.radius < (1/2.5)*(self.frame.shape[1]):
            raise TypeError("no circle could be found in this image")

        return self.radius

