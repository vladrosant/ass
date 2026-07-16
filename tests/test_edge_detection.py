from pathlib import Path

import cv2
import numpy as np
import pytest

import canny_edge_detection
import log_edge_detection
import sobel_edge_detection

REPO_ROOT = Path(__file__).resolve().parent.parent
SAMPLE_IMAGE = REPO_ROOT / "src" / "imsample" / "debris_sample_2.jpg"


@pytest.fixture(scope="module")
def sample_image():
    img = cv2.imread(str(SAMPLE_IMAGE), cv2.IMREAD_GRAYSCALE)
    assert img is not None, f"missing sample image at {SAMPLE_IMAGE}"
    return img


@pytest.mark.parametrize(
    "module",
    [canny_edge_detection, log_edge_detection, sobel_edge_detection],
)
def test_detect_edges_returns_matching_shape(sample_image, module):
    edges = module.detect_edges(sample_image)

    assert edges.shape == sample_image.shape
    assert edges.dtype == np.uint8
