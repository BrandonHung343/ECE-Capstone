import numpy as np
import cv2
import time
import colorsys

class CVData():
    def __init__(self, numPoints):
        self.lb = np.array([0.0, 0.0, 0.0])
        self.ub = np.array([0.0, 0.0, 0.0])
        self.d1 = 50
        self.d2 = 100
        self.d3 = 25
        self.numPoints = 2
        self.kSize = 11
        self.cK = 25
        self.oK = 11
        self.sigX = 0.5
        self.recList = []

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


def average_over_frame(event, x, y, flags, params):
    cal_frame = params[0]
    dat = params[1]
    d1 = dat.d1
    d2 = dat.d2
    d3 = dat.d3
    ub = np.zeros(3)
    lb = np.zeros(3)
    counter = 0
    
    if event == cv2.EVENT_LBUTTONDOWN:
        dat.recList.append((x, y))
        print(cal_frame[y,x])
        
    elif event == cv2.EVENT_LBUTTONUP:
        dat.recList.append((x, y))
        # ry = recList[0][0]:recList[1][0]
        # rx = recList[0][1]:recList[1][1]
        section = cal_frame[dat.recList[0][1]:dat.recList[1][1], dat.recList[0][0]:dat.recList[1][0]]
        cv2.rectangle(cal_frame, dat.recList[0], dat.recList[1], (0, 255, 0), 2)
        cv2.imshow("calibrate", section)
        avg_color = get_color_dominant(section)
        lb = np.array([avg_color[0] - d1, avg_color[1] - d2, avg_color[2] - d3])
        ub = np.array([avg_color[0] + d1, avg_color[1] + d2, avg_color[2] + d3])
        
        for k in range(3):
            lb[k] = max(lb[k], 0)
            ub[k] = min(ub[k], 255)

        dat.lb = lb
        dat.ub = ub


def get_color_averages(frame):
    numFrames = np.shape(frame)[2]
    avg = np.zeros(numFrames)
    for i in range(numFrames):
        avg[i] = np.around(np.mean(frame[:, :, i]))
        print(avg[i])
    return avg


def get_color_dominant(frame):
    tempFrame = np.float32(np.reshape(frame, (-1,3)))
    
    # frameLen = tempFrame.shape[0] * tempFrame.shape[1] * tempFrame.shape[2]
    # tempFrame = tempFrame.reshape(frameLen, 1)
    nColors = 1
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    _, labels, centers = cv2.kmeans(tempFrame, nColors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)
    hsv = centers[np.argmax(counts)]
    # rgb = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])
    return hsv # np.array(rgb) * 255


def clean_morphological(dat, frame):
    im = frame
    # .MORPH_DILATE, (dat.cK, dat.cK))
    im = cv2.dilate(im, (dat.cK, dat.cK), 1) 
    im = cv2.morphologyEx(im, cv2.MORPH_OPEN, (dat.oK, dat.oK))

    # im = cv2.morphologyEx(im, cv2.MORPH_CLOSE, (dat.oK, dat.oK))
    return im


def calibrate(dat):
    cam = 0
    cv2.namedWindow("calibrate")
    cap = cv2.VideoCapture(cam)
    cap.open(cam)
    ret, cal_frame = cap.read()
    frame = cal_frame
    cal_frame = cv2.cvtColor(cal_frame, cv2.COLOR_RGB2HSV)
    cal_frame = cv2.GaussianBlur(cal_frame, (dat.kSize, dat.kSize), dat.sigX)
    cv2.setMouseCallback("calibrate", average_over_frame, [cal_frame, dat]);
    # cal_frame = white_balance(cal_frame)
    cv2.imshow("calibrate", frame)

    key = cv2.waitKey(0)

    masked = color_mask(dat, cal_frame)
    masked = clean_morphological(dat, masked)

    masked = cv2.cvtColor(masked, cv2.COLOR_HSV2RGB)
    cv2.imshow("calibrate", masked)

    key = cv2.waitKey(0)

    cv2.destroyAllWindows()
    return dat


def color_mask(dat, frame):
    mask = cv2.inRange(frame, dat.lb, dat.ub)
    # grey world white balancing assumption 
    return cv2.bitwise_and(frame, frame, mask=mask)


def white_balance(frame):
    rScale = np.mean(frame[:, :, 1]) / np.mean(frame[:, :, 0])
    bScale = np.mean(frame[:, :, 1]) / np.mean(frame[:, :, 2])
    frame = np.dstack((np.round(frame[:, :, 0] * rScale), frame[:, :, 1], np.round(frame[:, :, 2] * bScale)))
    print(type(frame))
    return frame


def main():
    dat = CVData(4)
    dat.print_info()
    dat = calibrate(dat)
    dat.print_info()


if __name__ == '__main__':
    main()


