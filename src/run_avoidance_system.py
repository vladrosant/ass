from pathlib import Path

import cv2

from sobel_edge_detection import detect_edges

REPO_ROOT = Path(__file__).resolve().parent.parent
SAMPLE_IMAGE = REPO_ROOT / "src" / "imsample" / "debris_sample_2.jpg"


def calculate_object_center(edges):
    # find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    # largest contour is probably the main object
    largest_contour = max(contours, key=cv2.contourArea)
    M = cv2.moments(largest_contour)
    if M["m00"] == 0:
        return None

    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
    return cx, cy


def compute_move_direction(obj_x, obj_y, center_x, center_y) -> dict:
    move_direction = {"x": 0, "y": 0}

    if obj_x < center_x:
        move_direction["x"] = 1  # move right
    elif obj_x > center_x:
        move_direction["x"] = -1  # move left

    if obj_y < center_y:
        move_direction["y"] = 1  # move down
    elif obj_y > center_y:
        move_direction["y"] = -1  # move up

    return move_direction


def main() -> dict | None:
    img = cv2.imread(str(SAMPLE_IMAGE), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"sample image not found: {SAMPLE_IMAGE}")

    sobel_edges = detect_edges(img)

    h, w = img.shape
    center_x, center_y = w // 2, h // 2

    object_center = calculate_object_center(sobel_edges)
    if object_center is None:
        print("no object detected, no maneuver needed")
        return None

    obj_x, obj_y = object_center
    move_direction = compute_move_direction(obj_x, obj_y, center_x, center_y)

    print(f"object detected at: ({obj_x}, {obj_y})")
    print(f"suggested direction: {move_direction}")
    return move_direction


if __name__ == "__main__":
    main()
