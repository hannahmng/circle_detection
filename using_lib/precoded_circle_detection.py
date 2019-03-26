import argparse
from frame_utils import *

DEFAULT_VIDEO_FILE = "/mnt/storage/data/s3/procedures-gallery-prod/MPL/MPL_001.mp4"

MS_OPTIONS = [1000, 2000, 50000, 10000, 15000, 20000, 50000, 100000]

ap = argparse.ArgumentParser()

ap.add_argument("--video_file", type=str, required=False, help="video to get frame from", default=DEFAULT_VIDEO_FILE)
ap.add_argument("--ms_options", type=list, required=False, help="times to get frames from (in ms)", default=MS_OPTIONS)

args = ap.parse_args()


def main():

    frame = choose_frame(args.video_file, args.ms_options)

    _, thresh_frame = cv2.threshold(frame, 10, 50, cv2.THRESH_BINARY)

    edged_frame = cv2.Canny(thresh_frame, 0, 12)

    plt.imshow(edged_frame, cmap='gray')
    plt.show()

    min_radius = 600
    max_radius = 1000

    circles_log = []

    for guess_accumulator_array_threshold in range(1, 7):
        for guess_dp in range(1, 5):
            for guess_radius in range(min_radius, max_radius, 5):

                print("guessing radius: " + str(guess_radius) +
                      " and dp: " + str(guess_dp) +
                      " vote threshold: " + str(guess_accumulator_array_threshold))

                circles = cv2.HoughCircles(edged_frame,
                                           method=cv2.HOUGH_GRADIENT,
                                           dp=guess_dp,  # resolution ratio (1/)
                                           minDist=100,
                                           param1=10,  # value for scaling w/ canny
                                           param2=guess_accumulator_array_threshold,  # how sure it needs to be
                                           minRadius=(guess_radius - 3),
                                           maxRadius=(guess_radius + 3)
                                           )
                if circles is not None:
                    if circles.shape[1] == 1:
                        circles_log.extend(circles)

    circles_log = np.array(circles_log)

    for cir in circles_log:

        cir = np.round(cir)

        for x, y, r in cir:
            if abs(x-(frame.shape[0]/2)) < 500 and abs(y-(frame.shape[1]/2)) < 500:
                plot_frame_with_circle(frame, [x, y], r)


if __name__ == '__main__':

    main()





