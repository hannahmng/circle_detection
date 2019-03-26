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

        top_left, top_right = self.find_top_pixels()
        if not self.has_circle:
            return -1
        top_left = np.amax(top_left, axis=0)
        top_right = np.amin(top_right, axis=0)

        bottom_left, bottom_right = self.find_bottom_pixels()
        bottom_left = np.amax(bottom_left, axis=0)
        bottom_right = np.amin(bottom_right, axis=0)

        top_right, bottom_left = self.length_check(top_right, top_left, bottom_right, bottom_left, offset=2)

        self.midpoint[0] = (top_right[0] + bottom_left[0])/2
        self.midpoint[1] = (top_right[1] + bottom_left[1])/2

        return bottom_right

    def length_check(self, top_right, top_left, bottom_right, bottom_left, offset):

        top_length = top_right[1] - top_left[1]
        top_mid_point = 1/2*(top_right[1] + top_left[1])
        bottom_length = bottom_right[1] - bottom_left[1]
        bottom_mid_point = 1/2*(bottom_right[1] - bottom_left[1])

        if abs(top_length - bottom_length) > 20 or abs(top_mid_point - bottom_mid_point) > 200:

            # todo only for debugging purposes
            print(top_length, bottom_length, top_mid_point, bottom_mid_point)

            if top_right[0] > bottom_right[0]:
                print('WARNING something is wrong - top and bottom have passed each other')

            if top_length < bottom_length:
                top_left, top_right = self.find_top_pixels(offset=offset)
                top_left = np.amax(top_left, axis=0)
                top_right = np.amin(top_right, axis=0)
                top_right, bottom_left = self.length_check(top_right, top_left, bottom_right, bottom_left, offset=offset+20)

            elif bottom_length < top_length:
                bottom_left, bottom_right = self.find_bottom_pixels(offset=offset)
                bottom_left = np.amax(bottom_left, axis=0)
                bottom_right = np.amin(bottom_right, axis=0)
                top_right, bottom_left = self.length_check(top_right, top_left, bottom_right, bottom_left, offset=offset+20)

        return top_right, bottom_left

    def find_top_pixels(self, offset=0):

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
                # print("WARNING no circle found")
                # self.has_circle = False
                # return top_left, top_right
            top_left, top_right = self.find_top_pixels(offset=offset+20)

        return top_left, top_right

    def find_bottom_pixels(self, offset=0):

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
                # print("WARNING no circle found")
                # self.has_circle = False
                # return bottom_left, bottom_right
            bottom_left, bottom_right = self.find_bottom_pixels(offset=offset + 20)

        return bottom_left, bottom_right

    def determine_radius(self, circle_point):

        delta_x = abs(self.midpoint[1] - circle_point[1])
        delta_y = abs(self.midpoint[0] - circle_point[0])

        self.radius = np.sqrt(delta_x**2 + delta_y**2)

        if self.radius < (1/2.5)*(self.frame.shape[1]):
            raise TypeError("no circle could be found in this image")
            # print("WARNING the circle found is too small to be valid")
            # self.has_circle = False

        return self.radius

