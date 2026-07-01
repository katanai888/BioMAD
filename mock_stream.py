import importlib.util
import json
import time
from pathlib import Path

spec = importlib.util.spec_from_file_location('skdh.io.stream', 'src/skdh/io/stream.py')
stream_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stream_module)
StreamIngestor = stream_module.StreamIngestor


def main():
    ingestor = StreamIngestor(
        column_mapping={
            "accel_x": "x",
            "accel_y": "y",
            "accel_z": "z",
        },
        time_column="timestamp",
    )

    samples = [
        {"timestamp": "2024-01-01T00:00:00Z", "accel_x": 0.1, "accel_y": 0.2, "accel_z": 0.9},
        {"timestamp": "2024-01-01T00:00:01Z", "accel_x": 0.2, "accel_y": 0.3, "accel_z": 1.0},
        {"timestamp": "2024-01-01T00:00:02Z", "accel_x": 0.3, "accel_y": 0.4, "accel_z": 1.1},
    ]

    for payload in samples:
        result = ingestor.ingest(payload)
        print(json.dumps({
            "sample": payload,
            "normalized": {
                "time": result["time"].tolist(),
                "accel": result["accel"].tolist(),
                "fs": result["fs"],
            },
        }, indent=2))
        time.sleep(0.1)

    print("Verification summary: stream ingestion produced normalized acceleration data for 3 samples.")


if __name__ == "__main__":
    main()
