import numpy as np
import cv2

from run_avoidance_system import calculate_object_center, compute_move_direction


def test_compute_move_direction_object_top_left():
    assert compute_move_direction(obj_x=10, obj_y=10, center_x=50, center_y=50) == {"x": 1, "y": 1}


def test_compute_move_direction_object_bottom_right():
    assert compute_move_direction(obj_x=90, obj_y=90, center_x=50, center_y=50) == {"x": -1, "y": -1}


def test_compute_move_direction_object_centered():
    assert compute_move_direction(obj_x=50, obj_y=50, center_x=50, center_y=50) == {"x": 0, "y": 0}


def test_calculate_object_center_with_no_contours_returns_none():
    edges = np.zeros((100, 100), dtype=np.uint8)
    assert calculate_object_center(edges) is None


def test_calculate_object_center_finds_blob_centroid():
    edges = np.zeros((100, 100), dtype=np.uint8)
    cv2.rectangle(edges, (20, 20), (40, 40), color=255, thickness=-1)

    center = calculate_object_center(edges)

    assert center is not None
    cx, cy = center
    assert 25 <= cx <= 35
    assert 25 <= cy <= 35
