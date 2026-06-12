# Build configuration lives in pyproject.toml (src layout, setuptools).
# This shim exists only for `python setup.py ...` compatibility.
from setuptools import setup

if __name__ == "__main__":
    setup()
