import json
from pathlib import Path
from batch_job import process_record, run_batch


def test_process_record():
    rec = {"id": 1, "features": [1.0, 2.0]}
    out = process_record(rec)
    assert out["prediction"] == 3.0


def test_run_batch(tmp_path: Path):
    test_file = tmp_path / "input.jsonl"
    with test_file.open("w") as f:
        f.write(json.dumps({"id": 1, "features": [1, 2]}) + "\n")
        f.write(json.dumps({"id": 2, "features": [3, 4]}) + "\n")

    res = run_batch(test_file)
    assert len(res) == 2
    assert res[0]["prediction"] == 3.0
    assert res[1]["prediction"] == 7.0
