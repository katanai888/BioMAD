"""Lightweight IO package namespace for SKDH."""

from importlib import import_module

__all__ = (
    "ReadCwa",
    "ReadBin",
    "ReadApdmH5",
    "ReadNumpyFile",
    "ReadCSV",
    "ReadEmpaticaAvro",
    "MultiReader",
    "StreamIngestor",
    "axivity",
    "geneactiv",
    "apdm",
    "empatica",
    "numpy_compressed",
    "csv",
    "multireader",
)


_LAZY_IMPORTS = {
    "ReadCwa": ("skdh.io.axivity", "ReadCwa"),
    "ReadBin": ("skdh.io.geneactiv", "ReadBin"),
    "ReadApdmH5": ("skdh.io.apdm", "ReadApdmH5"),
    "ReadNumpyFile": ("skdh.io.numpy_compressed", "ReadNumpyFile"),
    "ReadCSV": ("skdh.io.csv", "ReadCSV"),
    "ReadEmpaticaAvro": ("skdh.io.empatica", "ReadEmpaticaAvro"),
    "MultiReader": ("skdh.io.multireader", "MultiReader"),
    "StreamIngestor": ("skdh.io.stream", "StreamIngestor"),
}


def __getattr__(name):
    if name in _LAZY_IMPORTS:
        module_name, attr_name = _LAZY_IMPORTS[name]
        module = import_module(module_name)
        value = getattr(module, attr_name)
        globals()[name] = value
        return value

    if name in {"axivity", "geneactiv", "apdm", "empatica", "numpy_compressed", "csv", "multireader"}:
        module = import_module(f"skdh.io.{name}")
        globals()[name] = module
        return module

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
