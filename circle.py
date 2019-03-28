import numpy as np


class Circle:
    NO_OF_SEARCH_LINES = 10

    def __init__(self, frame):

        self.frame = frame
        self.midpoint = [0, 0]
        self.radius = 0
        self.has_circle = True
        
        self.top_right = [0, 0]
        self.top_left = [0, 0]
        self.bottom_right = [0, 0]
        self.bottom_left = [0, 0]

    def determine_midpoint(self):

        self.top_left, self.top_right = self.find_edges_of_top_secant()
        self.bottom_left, self.bottom_right = self.find_edges_of_bottom_secant()

        self.length_check(height_offset=2)

        self.midpoint[0] = (self.top_right[0] + self.bottom_left[0])/2
        self.midpoint[1] = (self.top_right[1] + self.bottom_left[1])/2

        return self.bottom_right

    def length_check(self, height_offset):

        top_length, top_mid_point, bottom_length, bottom_mid_point = self.calc_meta_info_abt_corner_points()

        if abs(top_length - bottom_length) > 20 or abs(top_mid_point - bottom_mid_point) > 200:

            print(top_length, bottom_length, top_mid_point, bottom_mid_point)

            if self.top_right[0] > self.bottom_right[0]:
                print('WARNING something is wrong - top and bottom have passed each other')

            self.rec_edge_points_depending_on_lengths(top_length, bottom_length, side_offset=0, height_offset=height_offset)
            self.length_check(height_offset=height_offset + 20)

    def position_check(self, side_offset):

        top_length, top_mid_point, bottom_length, bottom_mid_point = self.calc_meta_info_abt_corner_points()
        length_diff = abs(top_mid_point - bottom_mid_point)
        to_break = False

        self.rec_edge_points_depending_on_lengths(top_length, bottom_length, side_offset, height_offset=0)

        top_length, new_top_mid_point, bottom_length, new_bottom_mid_point = self.calc_meta_info_abt_corner_points()
        new_length_diff = abs(top_mid_point - bottom_mid_point)

        if abs(new_length_diff - length_diff) < 5:
            to_break = True

        return self.top_right, self.top_left, self.bottom_right, self.bottom_left, new_top_mid_point, new_bottom_mid_point, to_break

    def rec_edge_points_depending_on_lengths(self, top_length, bottom_length, side_offset, height_offset):

        if top_length < bottom_length:
            self.find_edges_of_top_secant(side_offset=side_offset, height_offset=height_offset)
        elif bottom_length < top_length:
            self.find_edges_of_bottom_secant(side_offset=side_offset, height_offset=height_offset)

    def find_edges_of_top_secant(self, height_offset=0, side_offset=0):

        self.top_left = []
        self.top_right = []

        mid_pixel = int(self.frame.shape[0]/2)

        for line in range(height_offset, self.NO_OF_SEARCH_LINES + height_offset):
            for pixel in range(self.frame.shape[1]):

                if self.frame[line, pixel] > 0:
                    if pixel < mid_pixel:
                        self.top_left.append([line, pixel])
                    elif pixel > mid_pixel:
                        self.top_right.append([line, pixel])

        self.top_left = np.array(self.top_left)
        self.top_right = np.array(self.top_right)

        self.top_left.sort(axis=0)
        self.top_right.sort(axis=0)

        try:
            self.top_left = self.top_left[-(side_offset+1)]
            self.top_right = self.top_right[side_offset]

        except IndexError:
            if height_offset > 200 or side_offset > 800:
                raise TypeError("no circle could be found in this image")
            self.top_left, self.top_right = self.find_edges_of_top_secant(height_offset=height_offset + 20)

    def find_edges_of_bottom_secant(self, height_offset=0, side_offset=0):

        self.bottom_right = []
        self.bottom_left = []

        mid_pixel = int(self.frame.shape[0]/2)

        for line in range(self.frame.shape[0]-self.NO_OF_SEARCH_LINES-height_offset, self.frame.shape[0]-height_offset):
            for pixel in range(self.frame.shape[1]):

                if self.frame[line, pixel] > 0:
                    if pixel < mid_pixel:
                        self.bottom_left.append([line, pixel])
                    elif pixel > mid_pixel:
                        if self.bottom_left and self.bottom_left[-1][0] != line:
                            continue
                        self.bottom_right.append([line, pixel])

        self.bottom_left = np.array(self.bottom_left)
        self.bottom_right = np.array(self.bottom_right)

        self.bottom_left.sort(axis=0)
        self.bottom_right.sort(axis=0)

        try:

            self.bottom_left = self.bottom_left[side_offset]
            self.bottom_right = self.bottom_right[-(side_offset + 1)]

        except ValueError:
            if height_offset > 200 or side_offset > 800:
                raise TypeError("no circle could be found in this image")
            self.find_edges_of_bottom_secant(height_offset=height_offset + 20)

    def determine_radius(self, circle_point):

        delta_x = abs(self.midpoint[1] - circle_point[1])
        delta_y = abs(self.midpoint[0] - circle_point[0])

        self.radius = np.sqrt(delta_x**2 + delta_y**2)

        if self.radius < (1/2.5)*(self.frame.shape[1]):
            raise TypeError("no circle could be found in this image")

        return self.radius
    
    def calc_meta_info_abt_corner_points(self):

        top_length = self.top_right[1] - self.top_left[1]
        top_mid_point = 1 / 2 * (self.top_right[1] + self.top_left[1])
        bottom_length = self.bottom_right[1] - self.bottom_left[1]
        bottom_mid_point = 1 / 2 * (self.bottom_right[1] - self.bottom_left[1])
        
        return top_length, top_mid_point, bottom_length, bottom_mid_point
        
        

