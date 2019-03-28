import argparse
from utils.frame_utils import *
from utils.run_utils import *
from circle import Circle

DEFAULT_VIDEO_FILES = []

MS_OPTIONS = [20000, 50000, 120000, 150000, 500000, 100000000, 250000000, 500000000]

DEFAULT_VERBOSE = True

ap = argparse.ArgumentParser()

ap.add_argument("--video_files", type=list, required=False, help="video to get frame from", default=DEFAULT_VIDEO_FILES)
ap.add_argument("--ms_options", type=list, required=False, help="times to get frames from (in ms)", default=MS_OPTIONS)

ap.add_argument("--verbose", type=bool, required=False, help="show plots during processing", default=DEFAULT_VERBOSE)

args = ap.parse_args()


def main():

    for video in args.video_files:

        curr_frame_has_mask = False

        frame, ms = choose_frame(video, args.ms_options, verbose=args.verbose)

        processed_frame = process_frame(frame)

        if args.verbose:
            plt.imshow(processed_frame, cmap='gray')
            plt.show()

        circle = Circle(processed_frame)
        circle_point = circle.determine_midpoint()
        radius = circle.determine_radius(circle_point)

        if curr_frame_has_mask:
            circle.midpoint[0] = circle.midpoint[0] - 10

        if args.verbose:
            print(circle.midpoint, radius, circle_point)

        plot_frame_with_circle(frame, circle.midpoint, circle.radius)


if __name__ == '__main__':

    main()

