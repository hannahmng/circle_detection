import cv2
from matplotlib import pyplot as plt
import numpy as np


def get_frame(filepath, ms, b_and_w=True):

    vid = cv2.VideoCapture(filepath)
    vid.set(cv2.CAP_PROP_POS_MSEC, ms)
    _, frame = vid.read()

    if b_and_w:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:
        return frame

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


def plot_frame_with_corner_points(frame, top_left, top_right, bottom_left, bottom_right):

    fig, ax = plt.subplots()
    ax.imshow(frame, cmap='gray')
    ax.autoscale(False)
    ax.scatter(top_left[1], top_left[0], color='r')
    ax.scatter(top_right[1], top_right[0], color='r')
    ax.scatter(bottom_left[1], bottom_left[0], color='r')
    ax.scatter(bottom_right[1], bottom_right[0], color='r')
    plt.show()


def choose_frame(video_file, ms_options, verbose=True, b_and_w=True):

    best_frame = []
    highest_max_val_idx = 0
    best_ms = 0

    for ms in ms_options:

        try:
            frame = get_frame(video_file, int(ms), b_and_w)
        except Exception:
            print("WARNING tried to get frame outside of video length")
            continue

        hist = np.histogram(frame, bins=256)

        cut_data = [hist[0][i] for i in range(len(hist[0])) if hist[1][i] > 2]
        max_val_idx = np.argmax(cut_data)

        if max_val_idx > highest_max_val_idx:
            highest_max_val_idx = max_val_idx
            best_frame = frame
            best_ms = ms

    if verbose:
        plt.imshow(best_frame, cmap='gray')
        plt.show()
        plt.hist(best_frame.ravel(), bins=256, fc='k', ec='k')
        plt.show()

    return best_frame, best_ms
