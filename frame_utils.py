import cv2
from matplotlib import pyplot as plt
import numpy as np


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


def choose_frame(video_file, ms_options):

    best_frame = []
    highest_max_val_idx = 0

    for ms in ms_options:

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
