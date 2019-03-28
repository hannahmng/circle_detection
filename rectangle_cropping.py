import argparse
from utils.frame_utils import *
from utils.run_utils import *

DEFAULT_VIDEO_FILES = ["/mnt/storage/data/s3/procedures-gallery-prod/MPL/MPL_021.mp4"]

# "/mnt/storage/data/s3/procedures-gallery-prod/MPL/MPL_014.mp4", -- one outlier

MS_OPTIONS = [20000, 50000, 120000, 150000, 500000, 100000000, 250000000, 500000000]

DEFAULT_DIR_FOR_CROPPED_IMAGES = "/mnt/storage/research/omri/pre_processing"

DEFAULT_NECESSARY_THRESHOLD = 100
DEFAULT_SEARCH_THRESHOLD = 50
DEFAULT_OFFSET_CHANGE = 10

DEFAULT_VERBOSE = True


ap = argparse.ArgumentParser()

ap.add_argument("--video_files", type=list, required=False, help="video to get frame from", default=DEFAULT_VIDEO_FILES)
ap.add_argument("--ms_options", type=list, required=False, help="times to get frames from (in ms)", default=MS_OPTIONS)

ap.add_argument("--dir_for_saving_cropped_images", type=str, required=False,
                help="directory where to save cropped images", default=DEFAULT_DIR_FOR_CROPPED_IMAGES)

ap.add_argument("--necessary_threshold", type=int, required=False,
                help="threshold after which it is acceptable to stop searching", default=DEFAULT_NECESSARY_THRESHOLD)
ap.add_argument("--search_threshold", type=int, required=False,
                help="threshold after which we are happy to stop searching", default=DEFAULT_SEARCH_THRESHOLD)
ap.add_argument("--offset_change", type=int, required=False, help="step size when searching",
                default=DEFAULT_OFFSET_CHANGE)

ap.add_argument("--verbose", type=bool, required=False, help="show plots during processing", default=DEFAULT_VERBOSE)

args = ap.parse_args()


def crop_frame(frame):

    color_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    processed_frame = process_frame(color_frame)

    if args.verbose:
        plt.imshow(processed_frame, cmap='gray')
        plt.show()

    left_edge, right_edge = calculate_edge_points(args.necessary_threshold, args.search_threshold,
                                                  args.offset_change, processed_frame, frame, args.verbose)

    cropped_frame = color_frame[:, left_edge:right_edge, :]

    if args.verbose:
        plt.imshow(cropped_frame)
        plt.show()

    return cropped_frame


def main():

    for video in args.video_files:

        frame, ms = choose_frame(video, args.ms_options, verbose=args.verbose, b_and_w=False)

        cropped_frame = crop_frame(frame)

        file_path_for_saving_cropped = configure_destination_file_path(video, ms, args.dir_for_saving_cropped_images, is_cropped=True)
        file_path_for_saving_un_cropped = configure_destination_file_path(video, ms, args.dir_for_saving_cropped_images, is_cropped=False)

        cv2.imwrite(file_path_for_saving_cropped, cropped_frame)
        cv2.imwrite(file_path_for_saving_un_cropped, frame)


if __name__ == '__main__':

    main()
