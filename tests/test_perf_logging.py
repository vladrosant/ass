import json

from perf_logging import log_processing_time, next_output_path


def test_log_processing_time_creates_file(tmp_path):
    log_file = tmp_path / "performance_log.json"

    log_processing_time(log_file, "Metodo Teste", 0.123)

    data = json.loads(log_file.read_text())
    assert data == {"Metodo Teste": [0.123]}


def test_log_processing_time_appends_to_existing_method(tmp_path):
    log_file = tmp_path / "performance_log.json"
    log_file.write_text(json.dumps({"Metodo Teste": [0.1]}))

    log_processing_time(log_file, "Metodo Teste", 0.2)

    data = json.loads(log_file.read_text())
    assert data == {"Metodo Teste": [0.1, 0.2]}


def test_log_processing_time_adds_new_method_alongside_existing(tmp_path):
    log_file = tmp_path / "performance_log.json"
    log_file.write_text(json.dumps({"Metodo A": [0.1]}))

    log_processing_time(log_file, "Metodo B", 0.2)

    data = json.loads(log_file.read_text())
    assert data == {"Metodo A": [0.1], "Metodo B": [0.2]}


def test_next_output_path_uses_base_name_when_free(tmp_path):
    base = tmp_path / "edges_output"

    result = next_output_path(base, ".jpg")

    assert result == tmp_path / "edges_output.jpg"


def test_next_output_path_increments_on_collision(tmp_path):
    base = tmp_path / "edges_output"
    (tmp_path / "edges_output.jpg").write_bytes(b"")
    (tmp_path / "edges_output-1.jpg").write_bytes(b"")

    result = next_output_path(base, ".jpg")

    assert result == tmp_path / "edges_output-2.jpg"
