import cv2
import argparse
from matplotlib import pyplot as plt
import numpy as np
from circle import Circle

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

ap = argparse.ArgumentParser()

ap.add_argument("--video_files", type=list, required=False, help="video to get frame from", default=DEFAULT_VIDEO_FILES)
ap.add_argument("--ms_options", type=list, required=False, help="times to get frames from (in ms)", default=MS_OPTIONS)

args = ap.parse_args()


def get_frame(filepath, ms):

    vid = cv2.VideoCapture(filepath)
    vid.set(cv2.CAP_PROP_POS_MSEC, ms)
    _, frame = vid.read()

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    return frame


def has_mask(frame):

    white_vals_at_top = np.where(frame[:10, :] > 10)

    if len(white_vals_at_top) < 15:
        return True

    return False


def plot_frame_with_circle(frame, midpoint, radius):

    circle_to_be_drawn = plt.Circle((midpoint[1], midpoint[0]), radius, color='r', fill=False)

    fig, ax = plt.subplots()
    ax.imshow(frame, cmap='gray')
    ax.autoscale(False)
    ax.add_artist(circle_to_be_drawn)
    ax.scatter(midpoint[1], midpoint[0], color='r')
    plt.show()


def choose_frame(video_file):

    best_frame = []
    highest_max_val_idx = 0

    for ms in args.ms_options:

        try:
            frame = get_frame(video_file, int(ms))
        except cv2.Error:
            print("WARNING tried to get frame outside of video length")
            continue

        hist = np.histogram(frame, bins=256)

        cut_data = [hist[0][i] for i in range(len(hist[0])) if hist[1][i] > 2]
        max_val_idx = np.argmax(cut_data)

        if max_val_idx > highest_max_val_idx:

            highest_max_val_idx = max_val_idx
            best_frame = frame

    plt.imshow(best_frame, cmap='gray')
    plt.show()

    plt.hist(best_frame.ravel(), bins=256, fc='k', ec='k')
    plt.show()

    return best_frame


def main():

    # todo make more robust to noise at top left

    for video in args.video_files:

        curr_frame_has_mask = False

        frame = choose_frame(video)

        _, thresh_frame = cv2.threshold(frame, 10, 50, cv2.THRESH_BINARY)

        if has_mask(thresh_frame):
            curr_frame_has_mask = True
            thresh_frame = thresh_frame[20:, 20:frame.shape[1] - 20]

        edged_frame = cv2.Canny(thresh_frame, 0, 12)

        plt.imshow(edged_frame, cmap='gray')
        plt.show()

        circle = Circle(edged_frame)
        circle_point = circle.determine_midpoint()
        # if not circle.has_circle:
        #     continue
        radius = circle.determine_radius(circle_point)
        # if not circle.has_circle:
        #     continue

        if curr_frame_has_mask:
            circle.midpoint[0] = circle.midpoint[0] - 10

        print(circle.midpoint, radius, circle_point)

        plot_frame_with_circle(thresh_frame, circle.midpoint, circle.radius)


if __name__ == '__main__':

    main()

