import numpy as np
import cv2
import time
import colorsys
import matplotlib.pyplot as plt

class CVData():
    def __init__(self, cam, numDomColors, chipHeight, chipWidth, values):
        self.cam = cam
        self.lb = np.zeros((3, numDomColors, len(values)))
        self.ub = np.zeros((3, numDomColors, len(values)))
        self.d1 = 5
        self.d2 = 75
        self.d3 = 10
        self.numPoints = 2
        self.kSize = 15
        self.cK = 10
        self.eK = 50
        self.oK = 10
        self.sigX = 0.5
        self.recList = []
        self.domColors = 2
        self.chipWidth = chipWidth
        self.chipHeight = chipHeight
        self.delta = 30
        self.values = values
        self.prog = 0
        # Note: size of lb, ub is 3, numDomColors of chip, numValues of chip,

    def print_info(self):
        print("Lower bound:", self.lb)
        print("Upper bound:", self.ub)


def color_calib(event, x, y, flags, params):
    cal_frame = params[0]
    dat = params[1]

    delta = dat.delta
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
    dat = params[1]
    if event == cv2.EVENT_LBUTTONDOWN:
        dat.recList.append((x, y))
        # print(cal_frame[y,x])
        
    elif event == cv2.EVENT_LBUTTONUP:
        cal_frame = params[0]
        dat = params[1]
        d1 = dat.d1
        d2 = dat.d2
        d3 = dat.d3
        prog = dat.prog
        ub = np.zeros((3, dat.domColors))
        lb = np.zeros((3, dat.domColors))

        dat.recList.append((x, y))
        # print(dat.recList)
        
        section = cal_frame[dat.recList[0][1]:dat.recList[1][1], dat.recList[0][0]:dat.recList[1][0]]
        while True:
            cv2.imshow("calibrate", section)
            k = cv2.waitKey(1) & 0xFF
            if k == 13:
                break

        avg_colors = get_color_dominant(section)
        
        for i in range(dat.domColors):
            avg_color = avg_colors[i]
            avg_color = avg_color[0]
            # for LAB
            lb[:, i] = np.array([avg_color[0] - d1, avg_color[1] - d2, 0])
            ub[:, i] = np.array([avg_color[0] + d1, avg_color[1] + d2, 255])
            
            for k in range(3):
                lb[k, i] = max(lb[k, i], 0)
                ub[k, i] = min(ub[k, i], 255)
        
        dat.lb[:, :, prog] = lb
        dat.ub[:, :, prog] = ub
        dat.recList = []
        # dat.print_info()


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
    nColors = 2
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    _, labels, centers = cv2.kmeans(tempFrame, nColors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)
    # print(counts)
    # print(centers)
    hsv = list(zip(centers, counts))
    hsv.sort(key=lambda x: x[1])
    print(hsv)
    # rgb = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])
    return hsv # np.array(rgb) * 255


def clean_morphological(dat, frame):
    im = frame
    # .MORPH_DILATE, (dat.cK, dat.cK))
    # im = cv2.dilate(im, (dat.cK, dat.cK), 1) 
    im = cv2.morphologyEx(im, cv2.MORPH_OPEN, (dat.oK, dat.oK))
    # im = cv2.erode(im, (dat.eK, dat.eK), 1)
    im = cv2.morphologyEx(im, cv2.MORPH_CLOSE, (dat.cK, dat.cK))


    # im = cv2.morphologyEx(im, cv2.MORPH_CLOSE, (dat.oK, dat.oK))
    return im


def calibrate(dat):
    cam = dat.cam
    cv2.namedWindow("calibrate")
    cap = cv2.VideoCapture(cam)
    cap.open(cam)
    ret, cal_frame = cap.read()
    origFrame = np.copy(cal_frame)
    cal_frame = cv2.cvtColor(cal_frame, cv2.COLOR_RGB2HSV)
    # cal_frame = cv2.GaussianBlur(cal_frame, (dat.kSize, dat.kSize), dat.sigX)
    cal_frame = cv2.bilateralFilter(cal_frame, dat.kSize, 75, 75)
    org = (13, 25)
    color = (255, 255, 255)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.setMouseCallback("calibrate", average_over_frame, [cal_frame, dat]);
    for i in range(len(dat.values)):
        dat.prog = i
        txt = 'Chip Value: ' + str(int(dat.values[dat.prog]))
        tmp = np.copy(origFrame)
        cv2.putText(tmp, txt, org, font, 1, color, 2)
        # cal_frame = white_balance(cal_frame)
        while True:
            cv2.imshow("calibrate", tmp)
            k = cv2.waitKey(1) & 0xFF
            if k == 13:
                break

    cv2.destroyAllWindows()
    return dat


def color_mask(dat, frame, chip):
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(frame, dat.lb[:, 0, chip], dat.ub[:, 0, chip])
    # for i in range(len(dat.values)):
    for j in range(dat.domColors):
        tempMask = cv2.inRange(frame, dat.lb[:, j, chip], dat.ub[:, j, chip])
        mask = cv2.bitwise_or(mask, tempMask)

    return cv2.bitwise_and(frame, frame, mask=mask)


def get_stack_value(dat, debug=False):
    cam = dat.cam
    cap = cv2.VideoCapture(cam)
    cap.open(cam)
    ret, frame = cap.read()

    for i in range(len(dat.values)):
        masked = color_mask(dat, frame, i)
        masked = cv2.cvtColor(masked, cv2.COLOR_HSV2RGB)
        cal_frame = cv2.bilateralFilter(frame, dat.kSize, 75, 75)
        masked = clean_morphological(dat, masked)
        
        masked, bigBox = bounding_box(masked)
        
        if debug:
            cv2.namedWindow("debug_stack")
            cv2.imshow("debug_stack", masked)
            key = cv2.waitKey(0)

        if np.abs(bigBox[0] - dat.chipWidth) <= dat.delta:
            print(bigBox[1] / dat.chipHeight)
            print(np.round(bigBox[1] / dat.chipHeight) * dat.values[i])
        else:
            print("no detection")



def white_balance(frame, window_name):
    rScale = np.mean(frame[:, :, 1]) / np.mean(frame[:, :, 0])
    bScale = np.mean(frame[:, :, 1]) / np.mean(frame[:, :, 2])
    frame = np.dstack((np.round(frame[:, :, 0] * rScale), frame[:, :, 1], np.round(frame[:, :, 2] * bScale)))
    print(type(frame))
    return frame

def edge_detection(frame):
    frame = cv2.GaussianBlur(frame, (3, 3), 0)
    
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    
    grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3, borderType=cv2.BORDER_DEFAULT)
    # Gradient-Y
    # grad_y = cv.Scharr(gray,ddepth,0,1)
    grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3, borderType=cv2.BORDER_DEFAULT)
    
    
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)
    grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    return grad


def bounding_box(masked):
    gmasked = cv2.cvtColor(masked, cv2.COLOR_RGB2GRAY)
    contours, hierarchy = cv2.findContours(gmasked, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)
    cnt = max(contours, key=cv2.contourArea)
    x,y,w,h = cv2.boundingRect(cnt)
    gmasked = cv2.rectangle(masked,(x,y),(x+w,y+h),(255,0,0),2)
    return gmasked, (w, h)


def test_stereo():
    # from opencv docs
    # cv2.namedWindow("depth")
    imgL = cv2.imread('test_l.jpg',0)
    imgR = cv2.imread('test_r.jpg',0)
    stereo = cv2.StereoBM_create(numDisparities=16, blockSize=5)
    stereo.setSpeckleRange(16)
    disparity = stereo.compute(imgL,imgR)
    print(disparity.shape)
    plt.imshow((disparity + np.abs(np.min(disparity))) / np.max(disparity))
    plt.show()


# def main():
#     dat = CVData(2, 4, 9, [50, 500, 5])
#     # dat.print_info()
#     dat = calibrate(dat)
#     get_stack_value(dat, debug=True)
#     # dat.print_info()
#     # test_stereo()


# if __name__ == '__main__':
#     main()


