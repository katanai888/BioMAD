import numpy as np
import pandas as pd

from skdh.io.stream import StreamIngestor


def test_stream_ingestor_handles_dict_payload():
    ingestor = StreamIngestor(
        column_mapping={"accel_x": "x", "accel_y": "y", "accel_z": "z"}
    )

    payload = {
        "timestamp": "2024-01-01T00:00:00Z",
        "accel_x": 0.1,
        "accel_y": 0.2,
        "accel_z": 0.9,
    }

    result = ingestor.ingest(payload)

    assert result["time"].shape == (1,)
    assert result["accel"].shape == (1, 3)
    np.testing.assert_allclose(result["accel"][0], [0.1, 0.2, 0.9])
    assert result["time"][0] > 0


def test_stream_ingestor_handles_dataframe_payload_with_epoch_values():
    frame = pd.DataFrame(
        {
            "ts": [1704067200, 1704067201],
            "accelerationX": [0.3, 0.4],
            "accelerationY": [-0.2, -0.1],
            "accelerationZ": [1.0, 0.9],
        }
    )

    ingestor = StreamIngestor(
        column_mapping={
            "accelerationX": "x",
            "accelerationY": "y",
            "accelerationZ": "z",
        },
        time_column="ts",
    )

    result = ingestor.ingest(frame)

    assert result["time"].shape == (2,)
    assert result["accel"].shape == (2, 3)
    np.testing.assert_allclose(result["accel"][0], [0.3, -0.2, 1.0])
    assert np.isclose(result["fs"], 1.0)
