import cv2
import numpy
import numpy as np

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(1)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

def empty(a):
    pass

cv2.namedWindow('HSV')
cv2.resizeWindow('HSV', frameWidth, frameHeight)
cv2.createTrackbar('Hue min', 'HSV', 0, 179, empty)
cv2.createTrackbar('Hue max', 'HSV', 0, 179, empty)
cv2.createTrackbar('Saturation min', 'HSV', 0, 255, empty)
cv2.createTrackbar('Saturation max', 'HSV', 0, 255, empty)
cv2.createTrackbar('Value min', 'HSV', 0, 255, empty)
cv2.createTrackbar('Value max', 'HSV', 0, 255, empty)

cap = cv2.VideoCapture()
frameCount = 0

while True:
    frameCount += 1
    if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCount:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        frameCount = 0

    _, img = cap.read('Distracted Driver Crashes Into Attenuator Truck - DRAMATIC CRASH #carcrash #dashcam #shorts - TrafFix Devices (1080p, h264).mp4')
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h_min = cv2.createTrackbar('Hue min', 'HSV', 0, 179, empty)
    h_max = cv2.createTrackbar('Hue max', 'HSV', 0, 179, empty)
    s_min = cv2.createTrackbar('Saturation min', 'HSV', 0, 255, empty)
    s_max = cv2.createTrackbar('Saturation max', 'HSV', 0, 255, empty)
    v_min = cv2.createTrackbar('Value min', 'HSV', 0, 255, empty)
    v_max = cv2.createTrackbar('Value max', 'HSV', 0, 255, empty)
    print(h_min)

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHsv, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)

    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    hStack = np.hstack([img, mask, result])
    cv2.imshow('Horizontal Stacking', hStack)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.waitKey(0)

cap.release()
cv2.destroyAllWindows()