import argparse
import time
from pathlib import Path

import cv2

from perf_logging import log_processing_time, next_output_path

REPO_ROOT = Path(__file__).resolve().parent.parent
SAMPLE_IMAGE = REPO_ROOT / "src" / "imsample" / "debris_sample_2.jpg"
LOG_FILE = REPO_ROOT / "docs" / "performance_log.json"
OUTPUT_BASE = REPO_ROOT / "src" / "imoutput" / "canny" / "canny_edges_output"
METHOD_NAME = "canny optimized"


def detect_edges(img):
    return cv2.Canny(img, 100, 200)


def main(show: bool = False) -> Path:
    img = cv2.imread(str(SAMPLE_IMAGE), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"sample image not found: {SAMPLE_IMAGE}")

    start_time = time.time()
    canny_edges = detect_edges(img)
    processing_time = time.time() - start_time
    print(f"canny processing time: {processing_time:.4f}s")

    log_processing_time(LOG_FILE, METHOD_NAME, processing_time)

    file_path = next_output_path(OUTPUT_BASE, ".jpg")
    cv2.imwrite(str(file_path), canny_edges)
    print(f"saved output to: {file_path}")

    if show:
        cv2.imshow("Canny Edges", canny_edges)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return file_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--show", action="store_true", help="display the result in a window")
    args = parser.parse_args()
    main(show=args.show)
