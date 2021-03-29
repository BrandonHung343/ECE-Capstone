import numpy as np
import cv2

class CVData():
    def __init__(self, numPoints):
        self.lb = np.array([0.0, 0.0, 0.0])
        self.ub = np.array([0.0, 0.0, 0.0])
        self.delta = 75
        self.numPoints = 4
        self.kSize = 11
        self.sigX = 0.5

    def print_info(self):
        print("Lower bound:", self.lb)
        print("Upper bound:", self.ub)


def color_calib(event, x, y, flags, params):
    cal_frame = params[0]
    dat = params[1]
    delta = dat.delta
    ub = np.zeros(3)
    lb = np.zeros(3)
    if event == cv2.EVENT_LBUTTONDOWN:
        for i in range(3):
            if cal_frame[y,x,i] + delta > 255:
                ub[i] = 255
            else:
                ub[i] = cal_frame[y,x,i] + delta
            if cal_frame[y,x,i] - delta < 0:
                lb[i] = 0
            else:
                lb[i] = cal_frame[y,x,i] - delta
        dat.lb = lb
        dat.ub = ub


def calibrate(dat):
    cam = 0
    cv2.namedWindow("calibrate")
    cap = cv2.VideoCapture(cam)
    cap.open(cam)
    ret, cal_frame = cap.read()
    cv2.setMouseCallback("calibrate", color_calib, [cal_frame, dat]);
    cv2.imshow("calibrate", cal_frame)

    key = cv2.waitKey(0)

    masked = color_mask(dat, cal_frame)
    cv2.imshow("calibrate", masked)

    key = cv2.waitKey(0)

    cv2.destroyAllWindows()
    return dat


def color_mask(dat, frame):

    frame = cv2.GaussianBlur(frame, (dat.kSize, dat.kSize), dat.sigX)
    mask = cv2.inRange(frame, dat.lb, dat.ub)
    # grey world white balancing assumption 

    return cv2.bitwise_and(frame, frame, mask=mask)


def white_balance(frame):
    rScale = np.mean(frame[:, :, 1]) / np.mean(frame[:, :, 0])
    bScale = np.mean(frame[:, :, 1]) / np.mean(frame[:, :, 2])
    frame = np.dstack((frame[:, :, 0] * rScale, frame[:, :, 1], frame[:, :, 2] * bScale))
    return frame


def main():
    dat = CVData(4)
    dat.print_info()
    dat = calibrate(dat)
    dat.print_info()

if __name__ == '__main__':
    main()


