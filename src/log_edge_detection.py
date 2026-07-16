import argparse
import time
from pathlib import Path

import cv2
import numpy as np

from perf_logging import log_processing_time, next_output_path

REPO_ROOT = Path(__file__).resolve().parent.parent
SAMPLE_IMAGE = REPO_ROOT / "src" / "imsample" / "debris_sample_2.jpg"
LOG_FILE = REPO_ROOT / "docs" / "performance_log.json"
OUTPUT_BASE = REPO_ROOT / "src" / "imoutput" / "log" / "log_edges_output"
METHOD_NAME = "log optimized"

GAMMA = 1.3


def detect_edges(img):
    # gamma correction recalibrated for better contrast on debris samples
    normalized = img / 255.0
    gamma_corrected = np.power(normalized, GAMMA) * 255
    gamma_corrected = gamma_corrected.astype(np.uint8)

    log_edges = cv2.Laplacian(gamma_corrected, cv2.CV_64F)
    return np.uint8(np.absolute(log_edges))


def main(show: bool = False) -> Path:
    img = cv2.imread(str(SAMPLE_IMAGE), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"sample image not found: {SAMPLE_IMAGE}")

    start_time = time.time()
    log_edges = detect_edges(img)
    processing_time = time.time() - start_time
    print(f"log processing time: {processing_time:.4f}s")

    log_processing_time(LOG_FILE, METHOD_NAME, processing_time)

    file_path = next_output_path(OUTPUT_BASE, ".jpg")
    cv2.imwrite(str(file_path), log_edges)
    print(f"saved output to: {file_path}")

    if show:
        cv2.imshow("LoG Edges", log_edges)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return file_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--show", action="store_true", help="display the result in a window")
    args = parser.parse_args()
    main(show=args.show)
