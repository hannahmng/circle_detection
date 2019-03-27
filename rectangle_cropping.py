import argparse
from frame_utils import *
from circle import Circle

DEFAULT_VIDEO_FILES = []

# "/mnt/storage/data/s3/procedures-gallery-prod/MPL/MPL_014.mp4", -- one outlier

MS_OPTIONS = [20000, 50000, 120000, 150000, 500000, 100000000, 250000000, 500000000]

verbose = True
dir_for_saving_cropped_images = "/mnt/storage/research/omri/pre_processing"

ap = argparse.ArgumentParser()

ap.add_argument("--video_files", type=list, required=False, help="video to get frame from", default=DEFAULT_VIDEO_FILES)
ap.add_argument("--ms_options", type=list, required=False, help="times to get frames from (in ms)", default=MS_OPTIONS)

args = ap.parse_args()


def main():

    for video in args.video_files:

        frame, ms = choose_frame(video, args.ms_options, verbose=verbose)
        _, thresh_frame = cv2.threshold(frame, 10, 50, cv2.THRESH_BINARY)

        if has_mask(thresh_frame):
            thresh_frame = thresh_frame[20:, 20:frame.shape[1] - 20]

        edged_frame = cv2.Canny(thresh_frame, 0, 12)

        if verbose:
            plt.imshow(edged_frame, cmap='gray')
            plt.show()

        circle = Circle(edged_frame)

        top_left, top_right = circle.find_edges_of_top_secant()
        bottom_left, bottom_right = circle.find_edges_of_bottom_secant()

        top_mid_point = (1/2) * (top_right[1] + top_left[1])
        bottom_mid_point = (1/2) * (bottom_right[1] + bottom_left[1])
        side_offset = 0

        while abs(top_mid_point - bottom_mid_point) > 50:

            top_right, top_left, bottom_right, bottom_left, top_mid_point, bottom_mid_point, to_break = \
                circle.position_check(top_right, top_left, bottom_right, bottom_left, side_offset)

            if to_break and abs(top_mid_point - bottom_mid_point) < 100:
                break

            side_offset += 10

        if verbose:
            plot_frame_with_corner_points(frame, top_left, top_right, bottom_left, bottom_right)

        left_edge = max(top_left[1], bottom_left[1])
        right_edge = min(top_right[1], bottom_right[1])

        color_frame = get_frame(video, ms, b_w=False)
        cropped_frame = color_frame[:, left_edge:right_edge, :]

        if verbose:
            plt.imshow(cropped_frame)
            plt.show()

        video_name = video.split("/")[-1]
        name_for_saving = "-".join([video_name, str(ms)])
        file_path_for_saving = "/".join([dir_for_saving_cropped_images, name_for_saving]) + ".jpg"
        cv2.imwrite(file_path_for_saving, cropped_frame)


if __name__ == '__main__':

    main()
