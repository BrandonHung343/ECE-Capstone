import numpy as np
import cv2
import time
import colorsys
import matplotlib.pyplot as plt
import copy

class CVData():
    def __init__(self, cam, numDomColors, chipHeight, chipWidth, values):
        self.cam = cam
        self.colorAssociation = {}
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
        self.searchArea = False
        self.searchWindow = None
        self.tempColor = None
        self.tempH = None
        self.tempW = None

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
    try:
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
            searching = dat.searchArea

            dat.recList.append((x, y))

            x1 = dat.recList[0][1]
            x2 = dat.recList[1][1]
            y1 = dat.recList[0][0]
            y2 = dat.recList[1][0]
            section = cal_frame[x1:x2, y1:y2]

            # If search area, all we want are the bounds
            if searching:
                dat.searchWindow = (x1, x2, y1, y2)
                while True:
                    cv2.imshow("calibrate", section)
                    k = cv2.waitKey(1) & 0xFF
                    if k == 13:
                        break

            # Otherwise, we are looking for color associations
            else:
                while True:
                    cv2.imshow("calibrate", section)
                    k = cv2.waitKey(1) & 0xFF
                    if k == 13:
                        break
                # print(x1, x2, y1, y2)
                dat.tempH = x2 - x1
                dat.tempW = y2 - y1
                dat.tempColor = get_color_dominant(section)
                # dat.colorAssociation[dat.prog] = domColor[0]
            dat.recList = []

    except:
        print("You may need to redo that one!")
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
    
    nColors = 1
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    _, labels, centers = cv2.kmeans(tempFrame, nColors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)
    
    return centers # np.array(rgb) * 255



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



def calibrate(dat, test=False, testIm=None):
    if not test:
        cam = dat.cam
        cap = dat.cap
        cap.open(cam)
        ret, cal_frame = cap.read()
    else:
        cal_frame = testIm

    org = (13, 25)
    txtColor = (255, 255, 255)
    font = cv2.FONT_HERSHEY_SIMPLEX
    debug = True
    cv2.namedWindow("calibrate")
    cv2.setMouseCallback("calibrate", average_over_frame, [cal_frame, dat]);

    for i in range(len(dat.values)):
        dat.prog = i
        txt = 'Chip Value: ' + str(int(dat.values[dat.prog]))
        tmp = np.copy(cal_frame)
        cv2.putText(tmp, txt, org, font, 1, txtColor, 2)
        # cal_frame = white_balance(cal_frame)
        while True:
            cv2.imshow("calibrate", tmp)
            k = cv2.waitKey(1) & 0xFF
            if k == 13:
                break

        dat.chipHeight += dat.tempH
        dat.chipWidth += dat.tempW
        dat.colorAssociation[i] = dat.tempColor

    dat.chipHeight = np.round(dat.chipHeight / len(dat.values))
    dat.chipWidth = np.round(dat.chipWidth / len(dat.values))

    print("Chip Width: %d, Chip Height: %d" % (dat.chipWidth, dat.chipHeight))
    print("Colors", dat.colorAssociation)
    # Set up the search area calibration
    dat.searchArea = True
    txt = "Expected Chip Area"
    tmp = np.copy(cal_frame)
    cv2.putText(tmp, txt, org, font, 1, txtColor, 2)
    
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

    dat = calibrate(dat, test=True, testIm=cal_frame)

    binThresh = 245
    sizes = cal_frame.shape

    r1 = np.round(dat.searchWindow[0])
    r2 = np.round(dat.searchWindow[1])
    c1 = np.round(dat.searchWindow[2])
    c2 = np.round(dat.searchWindow[3])
    cut_frame = cal_frame[r1:r2, c1:c2]

    grey_mask = bin_thresh(cut_frame, binThresh, dat)
    checkersGroups = get_contours(grey_mask, dat)

    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 0, 255)]
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

    if m > 0:
        theta = -theta

    R = cv2.getRotationMatrix2D((cols/2, rows/2), theta*180/np.pi, 1)
    rotated = cv2.warpAffine(cut_frame, R, (cols, rows))
    cv2.imshow("calibrate", rotated)
    cv2.waitKey(0)

    # print("m: ", m)

    rot_grey = bin_thresh(rotated, binThresh, dat)
    checkersGroups = get_contours(rot_grey, dat)
    rectList = minimum_bounding_rectangle(checkersGroups)
    rotated, rectBottoms = get_cnt_rects(checkersGroups, rotated, colors, rectList, draw=True)
    cv2.imshow("calibrate", rotated)
    cv2.waitKey(0)

    totVal = stack_values(dat, None, rectList, rotated, debug=True)
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
    # print(areaBound)
    updated_checkers = copy.deepcopy(checkers)
    while len(updated_checkers) > 0:
        mySquare = updated_checkers.pop(0)
        myX = mySquare[5][0]
        myY = mySquare[5][1]
        found = False
        checkArea = (mySquare[3]) * (mySquare[4])
        if checkArea <= areaBound:
            # print(myX, myY)
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
                # print("oopsie")
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
    # Normal Ax = b solve. Dof refers to the degree of the polynomial
    # being solved. The default is 2, to return a line of the form mx+c
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
    # print(A)
    # print(b)
    return np.linalg.lstsq(A, b, rcond=None)



def stack_values(dat, colors, rectList, cut_frame, debug=False):
    totVal = 0
    # Want to match the values of the colors to the right stack
    if debug:
        cv2.namedWindow("debug")

    listOfColors = [dat.colorAssociation[key] for key in dat.colorAssociation]

    for i in range(len(dat.values)):
        # First, check the stack value
        # height = rectList[i][3] - rectList[i][2]
        x1 = rectList[i][0]
        x2 = rectList[i][1]
        y1 = rectList[i][2]
        y2 = rectList[i][3]
        height = y2 - y1
        print(cut_frame.shape)
        section = cut_frame[y1:y2, x1:x2]
        print("Stack values:", x1, x2, y1, y2)
        if debug:
            while True:
                cv2.imshow("debug", section)
                k = cv2.waitKey(1) & 0xFF
                if k == 13:
                    break

        secColor = get_color_dominant(section)

        # Find the closest remaining color
        minError = 10000000
        minIndex = -1
        ind = 0
        print("Color Comp: ", secColor)
        for color in listOfColors:
            tempError = np.linalg.norm(secColor - color)
            
            print("Color Real: ", color)
            if tempError < minError and tempError <= dat.delta:
                minIndex = ind
                minError = tempError
            ind += 1

        print("Closest Color: ", dat.colorAssociation[minIndex])
        print("Stack Height:", height)
        print("Estimated Height:", np.round(height / dat.chipHeight))
        print("Value: ", dat.values[minIndex])
        value = dat.values[minIndex] * np.round(height / dat.chipHeight)
        totVal += value
    return totVal



def bounding_box(masked):
    gmasked = cv2.cvtColor(masked, cv2.COLOR_RGB2GRAY)
    contours, hierarchy = cv2.findContours(gmasked, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)
    cnt = max(contours, key=cv2.contourArea)
    x,y,w,h = cv2.boundingRect(cnt)
    gmasked = cv2.rectangle(masked,(x,y),(x+w,y+h),(255,0,0),2)
    return gmasked, (w, h)



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


