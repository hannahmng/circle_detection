import cv2
import argparse
from matplotlib import pyplot as plt
import numpy as np
from diy_circle_detection import get_frame

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


def main():


    frame = get_frame(args.video_file, 100000)

    plt.imshow(frame, cmap='gray')
    plt.show()

    _, thresh_frame = cv2.threshold(frame, 10, 50, cv2.THRESH_BINARY)

    edged_frame = cv2.Canny(thresh_frame, 0, 50)

    plt.imshow(edged_frame, cmap='gray')
    plt.show()

    for radius in range(int((1 / 3) * edged_frame.shape[1]), int((4 / 3) * edged_frame.shape[0])):

        circles = cv2.HoughCircles(edged_frame, cv2.HOUGH_GRADIENT, dp=5, minDist=500, minRadius=radius, param1=50,
                                   param2=20)

        circles = np.uint16(np.around(circles))

        for i in circles[0, :]:
            cv2.circle(thresh_frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
            cv2.circle(thresh_frame, (i[0], i[1]), 2, (0, 0, 255), 3)

        # todo change to plt.imshow -- read circles into
        #  plt.Circle((midpoint[1], midpoint[0]), radius, color='r', fill=False) above
        cv2.imshow('circles', thresh_frame)
        cv2.waitKey(50)


if __name__ == '__main__':

    main()



