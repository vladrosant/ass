import json
from pathlib import Path


def log_processing_time(log_file: Path, method_name: str, processing_time: float) -> None:
    log_file = Path(log_file)
    if log_file.exists():
        with open(log_file, "r") as f:
            log_data = json.load(f)
    else:
        log_data = {}

    log_data.setdefault(method_name, []).append(processing_time)

    with open(log_file, "w") as f:
        json.dump(log_data, f, indent=4)


def next_output_path(base_path: Path, extension: str) -> Path:
    base_path = Path(base_path)
    file_path = base_path.with_suffix(extension)
    counter = 1
    while file_path.exists():
        file_path = base_path.with_name(f"{base_path.name}-{counter}{extension}")
        counter += 1
    return file_path
