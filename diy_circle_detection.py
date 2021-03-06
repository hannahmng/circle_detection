import argparse
from frame_utils import *
from circle import Circle
import cv2
from matplotlib import pyplot as plt

from trial_of_brute_force_search import brute_force_search

DEFAULT_VIDEO_FILES = ["/mnt/storage/data/s3/procedures-gallery-prod/MPL/MPL_001.mp4",
                       "/mnt/storage/data/s3/procedures-gallery-prod/MPL/MPL_002.mp4",
                       "/mnt/storage/data/s3/procedures-gallery-prod/MPL/MPL_003.mp4",
                       "/mnt/storage/data/s3/procedures-gallery-prod/MPL/MPL_004.mp4",
                       "/mnt/storage/data/s3/procedures-gallery-prod/MPL/MPL_005.mp4",
                       "/mnt/storage/data/s3/procedures-gallery-prod/MPL/MPL_006.mp4",
                       "/mnt/storage/data/s3/procedures-gallery-prod/GJM/GJM_001.mp4",
                       "/mnt/storage/data/s3/procedures-gallery-prod/GJM/GJM_002.mp4",
                       "/mnt/storage/data/s3/procedures-gallery-prod/BZMC/0c8fd7a1-6cff-462f-9a49-61a3bc856f67.m2t.NS.NoProp.MP4",
                       "/mnt/storage/data/s3/procedures-gallery-prod/BZMC/0a0ce90d-4ab8-4132-8777-72678629564f.m2t.NS.NoProp.MP4",
                       "/mnt/storage/data/s3/procedures-gallery-prod/BZMC/1e0c28b4-72da-4bf6-9c9f-fea7de5bb5c0.m2t.NS.NoProp.MP4",
                       "/mnt/storage/data/s3/procedures-gallery-prod/BZMC/1e597dc5-e42e-40e0-9507-26c7c96ae86f.m2t.NS.NoProp.MP4",
                       "/mnt/storage/data/s3/procedures-gallery-prod/BZMC/5f40ce68-3632-4038-8fe4-ead393976479.m2t.NS.NoProp.MP4",
                       "/mnt/storage/data/s3/procedures-gallery-prod/BZMC/1be3aeba-8113-4393-8f80-8367756933ec.m2t.NS.NoProp.MP4"]

MS_OPTIONS = [1000, 2000, 50000, 10000, 15000, 20000, 50000, 100000]

radius_ratio = 0.97


ap = argparse.ArgumentParser()

ap.add_argument("--video_files", type=list, required=False, help="video to get frame from", default=DEFAULT_VIDEO_FILES)
ap.add_argument("--ms_options", type=list, required=False, help="times to get frames from (in ms)", default=MS_OPTIONS)

args = ap.parse_args()


def main():

    for video in args.video_files:

        curr_frame_has_mask = False

        frame = choose_frame(video, args.ms_options)

        _, thresh_frame = cv2.threshold(frame, 10, 50, cv2.THRESH_BINARY)
        
        rad, mid_x, mid_y = brute_force_search(thresh_frame)

        if has_mask(thresh_frame):
            curr_frame_has_mask = True
            thresh_frame = thresh_frame[20:, 20:frame.shape[1] - 20]

        edged_frame = cv2.Canny(thresh_frame, 0, 12)

        plt.imshow(edged_frame, cmap='gray')
        plt.show()

        circle = Circle(edged_frame)
        circle.determine_midpoint()
        radius = circle.determine_radius()

        if curr_frame_has_mask:
            circle.midpoint[0] = circle.midpoint[0] - 10

        print(circle.midpoint, radius)

        plot_frame_with_circle(frame, circle.midpoint, circle.radius, radius_ratio)



if __name__ == '__main__':
    main()

