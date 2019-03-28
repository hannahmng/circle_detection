from circle import Circle
from utils.frame_utils import plot_frame_with_corner_points
import cv2
from utils.frame_utils import has_mask


def calculate_edge_points(necessary_threshold, search_threshold, offset_change, processed_frame, frame, verbose):

    circle = Circle(processed_frame)

    top_mid_point, bottom_mid_point = configure_circle(circle)

    side_offset = 0

    while abs(top_mid_point - bottom_mid_point) > search_threshold:

        top_right, top_left, bottom_right, bottom_left, top_mid_point, bottom_mid_point, to_break = \
            circle.position_check(side_offset)

        if to_break and abs(top_mid_point - bottom_mid_point) < necessary_threshold:
            break
        side_offset += offset_change

    if verbose:
        plot_frame_with_corner_points(frame, circle.top_left, circle.top_right, circle.bottom_left, circle.bottom_right)

    left_edge = max(circle.top_left[1], circle.bottom_left[1])
    right_edge = min(circle.top_right[1], circle.bottom_right[1])

    return left_edge, right_edge


def configure_circle(circle):

    circle.find_edges_of_top_secant()
    circle.find_edges_of_bottom_secant()

    top_mid_point = (1 / 2) * (circle.top_right[1] + circle.top_left[1])
    bottom_mid_point = (1 / 2) * (circle.bottom_right[1] + circle.bottom_left[1])

    return top_mid_point, bottom_mid_point


def configure_destination_file_path(video_file_name, ms, dir_for_saving_images, is_cropped):

    video_name = video_file_name.split("/")[-1]
    if is_cropped:
        name_for_saving = "-".join([video_name, str(ms)])
    else:
        name_for_saving = "-".join([video_name, "uncropped"])
    file_path_for_saving = "/".join([dir_for_saving_images, name_for_saving]) + ".jpg"

    return file_path_for_saving


def process_frame(raw_frame):

    _, thresholded_frame = cv2.threshold(raw_frame, 10, 50, cv2.THRESH_BINARY)

    if has_mask(thresholded_frame):
        thresholded_frame = thresholded_frame[20:, 20:raw_frame.shape[1] - 20]

    processed_frame = cv2.Canny(thresholded_frame, 0, 12)

    return processed_frame
