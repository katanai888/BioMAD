"""
Scikit Digital Health (:mod:`skdh`)
===================================

.. currentmodule:: skdh

Pipeline Processing
-------------------

.. autosummary::
    :toctree: generated/

    Pipeline
"""

from importlib import import_module
from sys import version_info

if version_info >= (3, 8):
    import importlib.metadata

    try:
        __version__ = importlib.metadata.version("scikit-digital-health")
    except importlib.metadata.PackageNotFoundError:
        __version__ = "0.0.0"
else:  # pragma: no cover
    import importlib_metadata

    try:
        __version__ = importlib_metadata.version("scikit-digital-health")
    except importlib_metadata.PackageNotFoundError:
        __version__ = "0.0.0"

__minimum_version__ = "0.9.10"

from skdh.base import BaseProcess, handle_process_returns

__skdh_version__ = __version__


__all__ = [
    "Pipeline",
    "BaseProcess",
    "activity",
    "gait_old",
    "gait",
    "sit2stand",
    "io",
    "sleep",
    "preprocessing",
    "features",
    "utility",
    "context",
    "__skdh_version__",
]


def __getattr__(name):
    if name == "Pipeline":
        from skdh.pipeline import Pipeline

        return Pipeline

    if name in {
        "utility",
        "io",
        "preprocessing",
        "sleep",
        "activity",
        "gait_old",
        "gait",
        "sit2stand",
        "features",
        "context",
    }:
        module = import_module(f"skdh.{name}")
        globals()[name] = module
        return module

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
