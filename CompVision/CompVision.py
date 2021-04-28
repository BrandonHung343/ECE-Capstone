import numpy as np
import cv2
import time
import colorsys
import matplotlib.pyplot as plt
import copy

class CVData():
    def __init__(self, cam, numDomColors, chipHeight, chipWidth, values):
        self.cam = cam
        self.lb = np.zeros((3, numDomColors, len(values)))
        self.ub = np.zeros((3, numDomColors, len(values)))
        self.d1 = 5
        self.d2 = 20
        self.d3 = 1
        self.numPoints = 2
        self.kSize = 35
        self.cK = 10
        self.eK = 50
        self.oK = 10
        self.sigX = 0.5
        self.recList = []
        self.domColors = numDomColors
        self.chipWidth = chipWidth
        self.chipHeight = chipHeight
        self.delta = 30
        self.values = values
        self.prog = 0
        self.cap = cv2.VideoCapture(cam)
        self.window = 1/2
        # Note: size of lb, ub is 3, numDomColors of chip, numValues of chip,

    def print_info(self):
        print("Lower bound:", self.lb)
        print("Upper bound:", self.ub)


def color_calib(event, x, y, flags, params):
    cal_frame = params[0]
    dat = params[1]
    d1 = dat.d1
    d2 = dat.d2
    d3 = dat.d3
    prog = dat.prog
    ub = np.zeros((3, dat.domColors))
    lb = np.zeros((3, dat.domColors))
    
    if event == cv2.EVENT_LBUTTONDOWN:
        print("RGB: ", cal_frame[y, x, :])

        dat.recList.append(cal_frame[y, x, :])
        if len(dat.recList) == dat.domColors:
            print("Computing mask")
            for i in range(dat.domColors):
                chipColor = dat.recList[i]
                # for LAB
                lb[:, i] = np.array([chipColor[0] - d1, chipColor[1] - d2, 0])
                ub[:, i] = np.array([chipColor[0] + d1, chipColor[1] + d2, 255])
                
                for k in range(3):
                    lb[k, i] = max(lb[k, i], 0)
                    ub[k, i] = min(ub[k, i], 255)
            
            dat.lb[:, :, prog] = lb
            dat.ub[:, :, prog] = ub
            dat.recList = []



def coord_get(event, x, y, flags, params):
    cal_frame = params[0]
    dat = params[1]
    d1 = dat.d1
    d2 = dat.d2
    d3 = dat.d3
    prog = dat.prog
    ub = np.zeros((3, dat.domColors))
    lb = np.zeros((3, dat.domColors))
    

    if event == cv2.EVENT_LBUTTONDOWN:
        print("x, y", y, x)



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
        print("RGB: ", cal_frame[y, x, :])

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
            avg_color = np.reshape(avg_color[0], (1, 1, 3))
            print(avg_color)
            avg_color = cv2.cvtColor(avg_color, cv2.COLOR_BGR2HSV)
            print(avg_color)
            avg_color = np.reshape(avg_color, (3))
            print(avg_color)

            avg_color = np.array([avg_color[0] / 2, avg_color[1] * 255, avg_color[2]])
            print(avg_color)

            # for LAB
            lb[:, i] = np.array([avg_color[0] - d1, avg_color[1] - d2, 0])
            ub[:, i] = np.array([avg_color[0] + d1, avg_color[1] + d2, 255])

            print(lb[:, i])
            
            for k in range(3):
                lb[k, i] = max(lb[k, i], 0)
                ub[k, i] = min(ub[k, i], 255)
        
        dat.lb[:, :, prog] = lb
        dat.ub[:, :, prog] = ub
        dat.recList = []
        


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
    hsv.sort(key=lambda x: -x[1])
    print(hsv)
    # rgb = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])
    # for h in hsv:
    #     print(h)
    #     tmp = np.reshape(h[0], (1, 1, 3))
    #     tmp = cv2.cvtColor(tmp, cv2.COLOR_HSV2RGB)
    #     tmp = np.reshape(tmp, (1, 3))
    #     tmp = np.int32(tmp)
    #     print(tmp)
    #     tmp[0, 0] = tmp[0, 0] >> 16 & 0xFF
    #     tmp[0, 1] = tmp[0, 1] >> 8 & 0xFF
    #     tmp[0, 2] = tmp[0, 2] & 0xFF
    #     print("RGB Conversion: ", tmp)
    return hsv # np.array(rgb) * 255



def clean_morphological(dat, frame):
    im = frame
    # .MORPH_DILATE, (dat.cK, dat.cK))
    # im = cv2.dilate(im, (dat.cK, dat.cK), 1) 
    im = cv2.morphologyEx(im, cv2.MORPH_OPEN, (dat.oK, dat.oK))
    # im = cv2.erode(im, (dat.eK, dat.eK), 1)
    im = cv2.morphologyEx(im, cv2.MORPH_CLOSE, (dat.cK, dat.cK))
    im = cv2.dilate(im, (dat.cK, dat.cK))
    # im = cv2.morphologyEx(im, cv2.MORPH_CLOSE, (dat.oK, dat.oK))
    return im



def calibrate(dat):
    cam = dat.cam
    cap = dat.cap
    cv2.namedWindow("calibrate")
    cap.open(cam)
    ret, cal_frame = cap.read()

    binThresh = 220
    grey_mask = cv2.cvtColor(cal_frame, cv2.COLOR_RGB2GRAY)
    grey_mask[grey_mask > binThresh] = 0
    grey_mask[grey_mask > 0] = 1
    cal_frame = cv2.bitwise_and(cal_frame, cal_frame, mask=grey_mask)

    cal_frame = cv2.morphologyEx(cal_frame, cv2.MORPH_CLOSE, (dat.cK, dat.cK))
    cal_frame = cv2.bilateralFilter(cal_frame, dat.kSize, 75, 75)

    org = (13, 25)
    color = (255, 255, 255)
    font = cv2.FONT_HERSHEY_SIMPLEX
    debug = True
    cv2.setMouseCallback("calibrate", average_over_frame, [cal_frame, dat]);

    for i in range(len(dat.values)):
        dat.prog = i
        txt = 'Chip Value: ' + str(int(dat.values[dat.prog]))
        tmp = np.copy(cal_frame)
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
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(frame, dat.lb[:, 0, chip], dat.ub[:, 0, chip])
    # for i in range(len(dat.values)):
    for j in range(dat.domColors):
        tempMask = cv2.inRange(frame, dat.lb[:, j, chip], dat.ub[:, j, chip])
        mask = cv2.bitwise_or(mask, tempMask)

    return cv2.bitwise_and(frame, frame, mask=mask)



def get_stack_value(dat, debug=False):
    cam = dat.cam
    cap = dat.cap
    cap.open(cam)
    ret, frame = cap.read()
    cal_frame = cv2.bilateralFilter(frame, dat.kSize, 75, 75)

    sizes = cal_frame.shape
    r1 = int(np.rint(sizes[0] * 1/4))
    r2 = int(np.rint(sizes[0] * 3/4))
    cut_frame = cal_frame[r1:r2, :, :]

    for i in range(len(dat.values)):
        masked = color_mask(dat, cut_frame, i)
        masked = cv2.cvtColor(masked, cv2.COLOR_HSV2BGR)
        masked = clean_morphological(dat, masked)
        
        masked, bigBox = bounding_box(masked)
        
        if debug:
            print(bigBox)
            cv2.namedWindow("debug_stack")
            cv2.imshow("debug_stack", masked)
            key = cv2.waitKey(0)

        if np.abs(bigBox[0] - dat.chipWidth) <= dat.delta:
            print(bigBox[1] / dat.chipHeight)
            print(np.round(bigBox[1] / dat.chipHeight) * dat.values[i])
        else:
            print("no detection")

        

    cv2.destroyAllWindows()
    return



def test_image(file, dat):
    cv2.namedWindow("calibrate")
    cal_frame = cv2.imread(file)
    # origFrame = np.copy(cal_frame)
    # eat out the white
    binThresh = 220
    grey_mask = cv2.cvtColor(cal_frame, cv2.COLOR_RGB2GRAY)
    grey_mask[grey_mask > binThresh] = 0
    grey_mask[grey_mask > 0] = 1
    cv2.imshow("calibrate", grey_mask)
    cv2.waitKey(0)
    cal_frame = cv2.bitwise_and(cal_frame, cal_frame, mask=grey_mask)
    cv2.imshow("calibrate", cal_frame)
    cv2.waitKey(0)

    cal_frame = cv2.morphologyEx(cal_frame, cv2.MORPH_CLOSE, (dat.cK, dat.cK))
    cal_frame = cv2.bilateralFilter(cal_frame, dat.kSize, 75, 75)
    
    # cal_frame = cv2.cvtColor(cal_frame, cv2.COLOR_RGB2HSV)
    # cal_frame = cv2.GaussianBlur(cal_frame, (dat.kSize, dat.kSize), dat.sigX)
    # origFrame = cv2.cvtColor(cal_frame, cv2.COLOR_BGR2HSV)
    org = (13, 25)
    color = (255, 255, 255)
    font = cv2.FONT_HERSHEY_SIMPLEX
    debug = True
    cv2.setMouseCallback("calibrate", average_over_frame, [cal_frame, dat]);

    for i in range(len(dat.values)):
        dat.prog = i
        txt = 'Chip Value: ' + str(int(dat.values[dat.prog]))
        tmp = np.copy(cal_frame)
        cv2.putText(tmp, txt, org, font, 1, color, 2)
        # cal_frame = white_balance(cal_frame)
        while True:
            cv2.imshow("calibrate", tmp)
            k = cv2.waitKey(1) & 0xFF
            if k == 13:
                break

    for i in range(len(dat.values)):
        sizes = cal_frame.shape
        r1 = int(np.rint(sizes[0] * 1/3))
        r2 = int(np.rint(sizes[0] * 2/3))
        


        print(r1)
        cut_frame = cal_frame[r1:r2, :, :]
        masked = color_mask(dat, cut_frame, i)
        masked = cv2.cvtColor(masked, cv2.COLOR_HSV2BGR)
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

        print(bigBox)

    cv2.destroyAllWindows()
    return



def get_contours(frame, dat):
    contours, hierarchy = cv2.findContours(frame, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)

    # cv2.setMouseCallback("calibrate", coord_get, [cut_frame, dat]);
    cntRects = []
    idNum = 0
    for cnt in contours:
        # cnt = max(contours, key=cv2.contourArea)
        x,y,w,h = cv2.boundingRect(cnt)
        approxCenter = np.array([x+w/2, y+h/2])
        cntRects.append([idNum, x, y, w, h, approxCenter])
        idNum += 1


    return assign_checkers(dat, cntRects)



def get_cnt_rects(checkersGroups, cut_frame, colors, rectList, draw=False):
    rectBottoms = []
    i = 0

    for group in checkersGroups:
        color = colors[i]
        for item in group:
            x = item[1]
            y = item[2]
            w = item[3]
            h = item[4]

            if draw:
                cut_frame = cv2.rectangle(cut_frame,(x,y),(x+w,y+h),color,1)

        bigX = rectList[i][0]
        bigW = rectList[i][1]
        bigY = rectList[i][2]
        bigH = rectList[i][3]

        if draw:
            cut_frame = cv2.rectangle(cut_frame,(bigX, bigY), (bigW, bigH), color, 1)
        i += 1
        
    for i in range(len(rectList)):
        bigX = rectList[i][0]
        # print(bigX)
        bigW = rectList[i][1]
        bigH = rectList[i][3]
        rectBottoms.append(((bigX+bigW)/2, bigH))

    return cut_frame, rectBottoms



def bin_thresh(frame, binThresh, dat):
    grey_mask = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    # grey_mask = grey_mask[r1:r2, :]
    grey_mask[grey_mask > binThresh] = 255
    grey_mask[grey_mask <= binThresh] = 0
    # grey_mask = clean_morphological(dat, grey_mask)
    grey_mask = cv2.morphologyEx(grey_mask, cv2.MORPH_OPEN, (dat.oK, dat.oK))
    return grey_mask



def test_white(file, dat):
    cv2.namedWindow("calibrate")
    cal_frame = cv2.imread(file)

    binThresh = 245
    sizes = cal_frame.shape
    r1 = int(np.rint(sizes[0] * 1/3))
    r2 = int(np.rint(sizes[0] * 2/3))
    cut_frame = cal_frame[r1:r2, :]

    grey_mask = bin_thresh(cut_frame, binThresh, dat)
    checkersGroups = get_contours(grey_mask, dat)

    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
    rectList = minimum_bounding_rectangle(checkersGroups)
    cut_frame, rectBottoms = get_cnt_rects(checkersGroups, cut_frame, colors, rectList, draw=False)
    xs = least_squares(rectBottoms, dof=2)
    # print("results", xs)
    m = xs[0][0]
    c = xs[0][1]
    # print(m)

    cv2.imshow("calibrate", cut_frame)
    cv2.waitKey(0)

    size = cut_frame.shape
    rows = size[0]
    cols = size[1]

    # cut_frame = cv2.line(cut_frame, (int(c), 0), (int(m*cols+c), cols), (255, 255, 255), 1)
    lineDist = np.sqrt((cols)**2 + int((m*cols)**2))
    theta = -(np.pi/2 - np.arccos(cols/lineDist))
    print("RotAng", theta)
    R = cv2.getRotationMatrix2D((cols/2, rows/2), theta*180/np.pi, 1)
    rotated = cv2.warpAffine(cut_frame, R, (cols, rows))
    cv2.imshow("calibrate", rotated)
    cv2.waitKey(0)

    rot_grey = bin_thresh(rotated, binThresh, dat)
    checkersGroups = get_contours(rot_grey, dat)
    rectList = minimum_bounding_rectangle(checkersGroups)
    rotated, rectBottoms = get_cnt_rects(checkersGroups, rotated, colors, rectList, draw=True)
    cv2.imshow("calibrate", rotated)
    cv2.waitKey(0)

    totVal = stack_values(dat, None, rectList)
    print(totVal)

    return



def assign_checkers(dat, checkers):
    wiggleRoom = 3/4
    searchX = wiggleRoom * dat.chipWidth
    areaBound = (dat.chipHeight * dat.chipWidth) / 15
    # print(searchY)
    checkersGroup = [[] for d in dat.values]
    # groupList = []
    nextNonempty = 1
    first = True
    print(areaBound)
    updated_checkers = copy.deepcopy(checkers)
    while len(updated_checkers) > 0:
        mySquare = updated_checkers.pop(0)
        myX = mySquare[5][0]
        myY = mySquare[5][1]
        found = False
        checkArea = (mySquare[3]) * (mySquare[4])
        if checkArea <= areaBound:
            print(myX, myY)
            continue

        if first:
            removed_inds = [0]
            checkersGroup[0].append(updated_checkers.pop(0))
            first = False
            continue

        for group in checkersGroup:
            for box in group:
                cmpX = box[5][0]
                cmpY = box[5][1]
               
                if np.abs(myX - cmpX) <= searchX: #  and np.abs(myY - cmpY) <= searchY
                    found = True
                    group.append(mySquare)
                    break

            if found:
                #group.append(mySquare)
                break

        if not found:
            checkersGroup[nextNonempty].append(mySquare)
            nextNonempty += 1
            if nextNonempty >= len(checkersGroup):
                print("oopsie")
                nextNonempty -= 1
    return checkersGroup



def minimum_bounding_rectangle(checkersGroups):
    rectList = []
    i = 0
    for group in checkersGroups:
        xMin = min(group, key=lambda x: x[1])
        yMin = min(group, key=lambda x: x[2])
        xMax = max(group, key=lambda x: x[1] + x[3])
        yMax = max(group, key=lambda x: x[2] + x[4])

        rectInfo = (xMin[1], xMax[1]+xMax[3], yMin[2], yMax[2]+yMax[4])
        rectList.append(rectInfo)
    return rectList



def least_squares(pts, dof=2):
    rows = len(pts)
    A = np.ones((rows, dof))
    b = np.zeros(rows)
    for i in range(rows):
        b[i] = pts[i][0]
        if dof == 1:
            A[i] = pts[i][1]
        else:
            for j in range(dof-1):
                A[i, j] = pts[i][1]
    print(A)
    print(b)
    return np.linalg.lstsq(A, b, rcond=None)



def stack_values(dat, colors, rectList):
    # find the color values
    totVal = 0
    for i in range(len(dat.values)):
        height = rectList[i][3] - rectList[i][2]
        value = dat.values[i] * np.round(height / dat.chipHeight)
        totVal += value
    return totVal



def edge_detection(frame):
    frame = cv2.GaussianBlur(frame, (3, 3), 0)
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3, borderType=cv2.BORDER_DEFAULT)

    abs_grad_y = cv2.convertScaleAbs(grad_y)
    grad = abs_grad_y # cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
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


def main():
    # dat = CVData(2, 4, 9, [50, 500, 5])
    # # dat.print_info()
    # dat = CVData(1, 1, 10, 90, [1, 2, 5, 10])
    # dat = calibrate(dat)
    # get_stack_value(dat, debug=True)
    # dat.print_info()
    # # test_stereo()
    dat = CVData(0, 1, 10, 90, [1, 2, 5, 10])
    test_white("setup.png", dat)


if __name__ == '__main__':
    main()


