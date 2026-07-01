"""Flexible stream ingestion for consumer-grade telemetry payloads."""

from __future__ import annotations

from typing import Any, Mapping, Optional

import numpy as np
import pandas as pd


class StreamIngestor:
    """Adapt streaming JSON or DataFrame payloads to SKDH-compatible arrays.

    Parameters
    ----------
    column_mapping : dict, optional
        Mapping from incoming column names to the standard SKDH axis names ``x``,
        ``y``, and ``z``. Keys may be consumer-grade names like ``accel_x`` or
        ``accelerationX`` while values should be ``x``, ``y``, or ``z``.
        The reverse mapping style is also supported, e.g. ``{"x": "accel_x"}``.
    time_column : str, optional
        Name of the timestamp column in the incoming payload. Defaults to
        ``"timestamp"``.
    fs : float, optional
        Sampling frequency to attach to the output. If omitted, it will be inferred
        from the timestamps when possible.
    """

    _AXES = ("x", "y", "z")

    def __init__(self, column_mapping=None, time_column="timestamp", fs=None):
        self.column_mapping = self._normalize_mapping(column_mapping)
        self.time_column = time_column
        self.fs = fs

    def ingest(self, payload):
        """Convert a single JSON payload, a list of payloads, or a DataFrame into SKDH data.

        Returns
        -------
        dict
            Dictionary containing ``time`` (unix seconds), ``accel`` (shape ``(N, 3)``),
            and ``fs``.
        """
        frame = self._coerce_to_frame(payload)
        if frame.empty:
            return {"time": np.array([], dtype=float), "accel": np.empty((0, 3)), "fs": self.fs}

        if self.time_column not in frame.columns:
            raise KeyError(f"Time column {self.time_column!r} not found in payload.")

        time_values = self._parse_time(frame[self.time_column])
        axis_columns = self._resolve_axis_columns(frame)

        accel = np.column_stack([frame[axis_columns[axis]] for axis in self._AXES])
        accel = np.asarray(accel, dtype=float)

        order = np.argsort(time_values)
        time_values = time_values[order]
        accel = accel[order]

        if self.fs is None:
            fs = self._infer_fs(time_values)
        else:
            fs = float(self.fs)

        return {"time": time_values, "accel": accel, "fs": fs}

    @staticmethod
    def _normalize_mapping(column_mapping):
        if column_mapping is None:
            return {}
        if not isinstance(column_mapping, Mapping):
            raise TypeError("column_mapping must be a dictionary-like object.")

        normalized = {}
        for source, target in column_mapping.items():
            source_name = str(source).strip().lower()
            target_name = str(target).strip().lower()

            if target_name in StreamIngestor._AXES:
                normalized[source_name] = target_name
            elif source_name in StreamIngestor._AXES:
                normalized[target_name] = source_name
            else:
                normalized[source_name] = target_name

        return normalized

    def _coerce_to_frame(self, payload):
        if isinstance(payload, pd.DataFrame):
            return payload.copy()
        if isinstance(payload, Mapping):
            return pd.DataFrame([payload])
        if isinstance(payload, (list, tuple)):
            return pd.DataFrame(payload)
        raise TypeError("payload must be a dictionary, list of dictionaries, or pandas.DataFrame")

    def _resolve_axis_columns(self, frame):
        resolved = {}
        column_map = {str(col).strip().lower(): col for col in frame.columns}

        for source, target in self.column_mapping.items():
            if source in column_map:
                resolved[target] = column_map[source]

        for axis in self._AXES:
            if axis in resolved:
                continue

            for alias in self._axis_aliases(axis):
                if alias in column_map:
                    resolved[axis] = column_map[alias]
                    break

            if axis in resolved:
                continue

            for alias in self._axis_aliases(axis):
                if alias in column_map.values():
                    resolved[axis] = next(col for col in frame.columns if str(col).strip().lower() == alias)
                    break

        missing = [axis for axis in self._AXES if axis not in resolved]
        if missing:
            raise KeyError(f"Could not resolve acceleration axes {missing} from payload columns {list(frame.columns)}")

        return resolved

    @staticmethod
    def _axis_aliases(axis):
        axis = axis.lower()
        return [
            axis,
            f"accel_{axis}",
            f"acceleration_{axis}",
            f"accel{axis}",
            f"acceleration{axis}",
            f"acceleration{axis.upper()}",
            f"accel{axis.upper()}",
        ]

    @staticmethod
    def _parse_time(values):
        values = pd.Series(values)
        if values.empty:
            return np.array([], dtype=float)

        if pd.api.types.is_numeric_dtype(values):
            numeric = values.astype(float).to_numpy()
            seconds = np.empty(numeric.shape[0], dtype=float)
            for idx, item in enumerate(numeric):
                if np.isnan(item):
                    seconds[idx] = np.nan
                    continue
                if abs(item) >= 1e18:
                    unit = "ns"
                elif abs(item) >= 1e15:
                    unit = "us"
                elif abs(item) >= 1e12:
                    unit = "ms"
                else:
                    unit = "s"
                seconds[idx] = pd.Timestamp(item, unit=unit, tz="UTC").timestamp()
            return seconds

        if values.dtype == object:
            candidates = values.astype(str).str.strip()
            numeric_strings = pd.to_numeric(candidates, errors="coerce")
            if numeric_strings.notna().any():
                return StreamIngestor._parse_time(numeric_strings)

        parsed = pd.to_datetime(values, utc=True, errors="coerce")
        if parsed.isna().all():
            raise ValueError("Unable to parse timestamps from the incoming payload.")

        seconds = parsed.astype("int64") / 1e9
        seconds = seconds.astype(float)
        seconds[pd.isna(parsed)] = np.nan
        return seconds

    @staticmethod
    def _infer_fs(time_values):
        if time_values.size <= 1:
            return 1.0
        diffs = np.diff(time_values)
        diffs = diffs[np.isfinite(diffs) & (diffs > 0)]
        if diffs.size == 0:
            return 1.0
        return float(1.0 / np.median(diffs))
