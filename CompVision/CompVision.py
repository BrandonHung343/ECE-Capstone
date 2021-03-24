import numpy as np
import cv2

frame = None
lb = np.array([0.0, 0.0, 0.0])
ub = np.array([0.0, 0.0, 0.0])
delta = 10

def color_calib(x, y):
    global frame
    for i in range(3):
        if frame[y,x,i] + delta > 255:
                ub[i] = 255
        else:
            ub[i] = frame[y,x,i] + delta
        if frame[y,x,i] - delta < 0:
            lb[i] = 0
        else:
            lb[i] = frame[y,x,i] - delta




def calibrate():
    cam = 0
    cv2.namedWindow("Calibrate")
    cv2.setMouseCallback("Calibrate", color_calib, None);
    cap = cv2.VideoCapture(cam)
    cap.open(cam)
    ret, frame = cap.read()

    while True:
        cv2.imshow("Calibrate", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == 27: # Esc
            cv2.destroyAllWindows()
            cap.release()
            break


def main():
    calibrate()

if __name__ == '__main__':
    main()


