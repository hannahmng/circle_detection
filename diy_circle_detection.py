import cv2
import argparse
from matplotlib import pyplot as plt
import numpy as np
from circle import Circle

DEFAULT_VIDEO_FILE = "/mnt/storage/data/s3/procedures-gallery-prod/MPL/MPL_001.mp4"
# DEFAULT_VIDEO_FILE = "/mnt/storage/data/s3/procedures-gallery-prod/MPL/MPL_003.mp4"
# DEFAULT_VIDEO_FILE = "/mnt/storage/data/s3/procedures-gallery-prod/BZMC/0b4a61ca-2822-47b0-9d25-9c863d294067.m2t.NS.NoProp.MP4"
# DEFAULT_VIDEO_FILE = "/mnt/storage/data/s3/procedures-gallery-prod/BZMC/0c8fd7a1-6cff-462f-9a49-61a3bc856f67.m2t.NS.NoProp.MP4"
# DEFAULT_VIDEO_FILE = "/mnt/storage/data/s3/procedures-gallery-prod/BZMC/0a0ce90d-4ab8-4132-8777-72678629564f.m2t.NS.NoProp.MP4"
# DEFAULT_VIDEO_FILE = "/mnt/storage/data/s3/procedures-gallery-prod/BZMC/2be08b3d-a680-4b7d-8308-179728a0eef0.m2t.NS.NoProp.MP4"
# DEFAULT_VIDEO_FILE = "/mnt/storage/data/s3/procedures-gallery-prod/BZMC/5f40ce68-3632-4038-8fe4-ead393976479.m2t.NS.NoProp.MP4"

# DEFAULT_VIDEO_FILE = "/mnt/storage/data/s3/procedures-gallery-prod/BZMC/6b9a51be-0b75-4939-b073-f73cba6f2a1f.m2t.NS.NoProp.MP4"

ap = argparse.ArgumentParser()

ap.add_argument("--video_file", type=str, required=False, help="video to get frame from", default=DEFAULT_VIDEO_FILE)

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


def main():

    curr_frame_has_mask = False

    frame = get_frame(args.video_file, 100000)

    plt.imshow(frame, cmap='gray')
    plt.show()

    _, thresh_frame = cv2.threshold(frame, 10, 50, cv2.THRESH_BINARY)

    if has_mask(thresh_frame):
        curr_frame_has_mask = True
        thresh_frame = thresh_frame[20:, 20:frame.shape[1] - 20]

    edged_frame = cv2.Canny(thresh_frame, 0, 50)

    plt.imshow(edged_frame, cmap='gray')
    plt.show()

    circle = Circle(edged_frame)
    circle_point = circle.determine_midpoint()
    radius = circle.determine_radius(circle_point)

    if curr_frame_has_mask:
        circle.midpoint[0] = circle.midpoint[0] - 10

    print(circle.midpoint, radius)

    plot_frame_with_circle(thresh_frame, circle.midpoint, circle.radius)


if __name__ == '__main__':

    main()

