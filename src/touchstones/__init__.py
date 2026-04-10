"""touchstones — a curated corpus of canonical reference artifacts."""

from touchstones.corpus import Corpus, corpus
from touchstones.schema import Category, Entry, LicenseStatus

__version__ = "0.0.1"

__all__ = [
    "Category",
    "Corpus",
    "Entry",
    "LicenseStatus",
    "__version__",
    "corpus",
]
