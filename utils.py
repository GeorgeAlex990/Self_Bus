import cv2
import numpy as np


def thresholding(img):
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 0, 200])
    upper = np.array([180, 50, 255])
    color_mask = cv2.inRange(imgHsv, lower, upper)

    height, width = img.shape[:2]
    roi_mask = np.zeros_like(color_mask)

    polygons = np.array([
        [
            (int(width * 0), height),
            (int(width * 0.1), int(height * 0.45)),
            (int(width * 0.9), int(height * 0.45)),
            (int(width * 1), height)
        ]
    ], dtype=np.int32)

    cv2.fillPoly(roi_mask, polygons, 255)
    final_mask = cv2.bitwise_and(color_mask, roi_mask)
    return final_mask


class LaneTracker:
    def __init__(self):
        self.left_base = None
        self.right_base = None


tracker = LaneTracker()


def get_lane_center(imgThres, display=False):
    height, width = imgThres.shape

    # Look at the bottom 25% of the frame where the lane lines start
    slice_height = int(height * 0.25)
    histogram = np.sum(imgThres[height - slice_height:, :], axis=0)

    midpoint = int(width / 2)

    # Define narrow search windows for the Green lane's left and right boundaries
    # Left boundary (dashed line separating Blue and Green lanes)
    left_min, left_max = int(width * 0.15), int(midpoint * 0.75)
    # Right boundary (solid line separating Green and Red zones)
    right_min, right_max = int(midpoint * 0.85), int(width * 0.85)

    left_slice = histogram[left_min:left_max]
    right_slice = histogram[right_min:right_max]

    left_base = np.argmax(left_slice) + left_min if len(left_slice) > 0 else int(width * 0.3)
    right_base = np.argmax(right_slice) + right_min if len(right_slice) > 0 else int(width * 0.7)

    has_left = histogram[left_base] >= 200
    has_right = histogram[right_base] >= 200

    typical_lane_width = int(width * 0.45)  # Expected width of your green lane

    # Intelligent fallback if one line is temporarily broken/dashed
    if has_left and has_right:
        tracker.left_base = left_base
        tracker.right_base = right_base
    elif has_right and not has_left:
        left_base = max(0, right_base - typical_lane_width)
        tracker.right_base = right_base
        tracker.left_base = left_base
    elif has_left and not has_right:
        right_base = min(width, left_base + typical_lane_width)
        tracker.left_base = left_base
        tracker.right_base = right_base
    else:
        left_base = tracker.left_base if tracker.left_base is not None else int(width * 0.3)
        right_base = tracker.right_base if tracker.right_base is not None else int(width * 0.7)

    # Calculate the center of the Green lane and compare it to the frame center
    lane_center = (left_base + right_base) // 2
    frame_center = width // 2
    deviation = lane_center - frame_center

    if display:
        img_vis = cv2.cvtColor(imgThres, cv2.COLOR_GRAY2BGR)
        cv2.line(img_vis, (frame_center, 0), (frame_center, height), (0, 255, 255), 1)  # Camera center (Yellow)
        cv2.line(img_vis, (lane_center, 0), (lane_center, height), (0, 255, 0), 2)  # Green lane center (Green)
        cv2.circle(img_vis, (left_base, height - 30), 10, (255, 0, 0), cv2.FILLED)  # Left boundary (Blue)
        cv2.circle(img_vis, (right_base, height - 30), 10, (0, 0, 255), cv2.FILLED)  # Right boundary (Red)
        cv2.imshow('Histogram & Center', img_vis)

    curve = deviation / (width / 2)
    return curve