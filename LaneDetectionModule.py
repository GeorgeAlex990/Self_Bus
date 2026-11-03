import cv2
import numpy as np
import utils


def getLaneCurve(img):
    imgThres = utils.thresholding(img)

    # Get the steering curve value (-1 to 1)
    curve = utils.get_lane_center(imgThres, display=True)

    print(f"Steering Curve: {curve:.2f}")
    return curve


if __name__ == "__main__":
    cap = cv2.VideoCapture(
        'Distracted Driver Crashes Into Attenuator Truck - DRAMATIC CRASH #carcrash #dashcam #shorts - TrafFix Devices (1080p, h264).mp4')

    while cap.isOpened():
        success, img = cap.read()
        if not success:
            break

        h, w = img.shape[:2]
        target_w, target_h = 640, 480
        scale = min(target_w / w, target_h / h)
        new_w = int(w * scale)
        new_h = int(h * scale)

        # Fix minor typo from before for height calculation:
        new_w = int(w * scale)
        new_h = int(h * scale)

        resized_img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

        curve = getLaneCurve(resized_img)

        cv2.imshow('vid', resized_img)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()