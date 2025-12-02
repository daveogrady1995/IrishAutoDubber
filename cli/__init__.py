"""Compatibility shim package `cli` that re-exports the `irishautodub` CLI entry.

This keeps a clearer package name for CLI consumers while the implementation
remains in `irishautodub`.
"""

from importlib import import_module

dub = import_module("irishautodub.dub_to_irish")


def run_dubbing_pipeline(*args, **kwargs):
    return dub.run_dubbing_pipeline(*args, **kwargs)


__all__ = ["dub", "run_dubbing_pipeline"]
