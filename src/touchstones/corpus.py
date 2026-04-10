"""The `Corpus` class and the module-level `corpus` singleton.

`corpus = Corpus.load_default()` is loaded eagerly at import time from
`data/entries.json`. The corpus surface is intentionally small: indexing
by name, iteration, filtering, and helpers for embedding pipelines.

Construct a `Corpus` directly from a `list[Entry]` in tests; use
`Corpus.load_default()` for the bundled corpus.
"""

from __future__ import annotations

from importlib.resources import as_file, files
from typing import Any

from touchstones.io import load_entries
from touchstones.schema import Entry


class Corpus:
    """An immutable collection of canonical reference artifacts."""

    def __init__(self, entries: list[Entry]) -> None:
        self._entries: tuple[Entry, ...] = tuple(entries)
        self._by_name: dict[str, Entry] = {}
        for entry in self._entries:
            if entry.name in self._by_name:
                raise ValueError(f"duplicate entry name: {entry.name!r}")
            self._by_name[entry.name] = entry

        # Validate that every `related` reference points to an existing entry.
        known_names = set(self._by_name)
        for entry in self._entries:
            missing = set(entry.related) - known_names
            if missing:
                raise ValueError(
                    f"entry {entry.name!r} references unknown related entries: {sorted(missing)}"
                )

    @classmethod
    def load_default(cls) -> Corpus:
        """Load the corpus bundled with the installed package."""
        resource = files("touchstones.data") / "entries.json"
        with as_file(resource) as path:
            entries = load_entries(path)
        return cls(entries)

    def __getitem__(self, name: str) -> Entry:
        return self._by_name[name]

    def __iter__(self):
        return iter(self._entries)

    def __len__(self) -> int:
        return len(self._entries)

    def __contains__(self, name: object) -> bool:
        return name in self._by_name

    def filter(
        self,
        *,
        discipline: str | None = None,
        category: str | None = None,
        tag: str | None = None,
    ) -> Corpus:
        """Return a new Corpus containing only entries that match all given filters.

        - `discipline`: matches if present in `Entry.disciplines` (which always
          includes `Entry.discipline` per the schema invariant).
        - `category`: matches if equal to `Entry.category`.
        - `tag`: matches if present in `Entry.tags`.
        """

        def keep(entry: Entry) -> bool:
            return (
                (discipline is None or discipline in entry.disciplines)
                and (category is None or entry.category == category)
                and (tag is None or tag in entry.tags)
            )

        return Corpus([e for e in self._entries if keep(e)])

    def texts(self, *, include_none: bool = False) -> list[str | None]:
        """Return the text content of every entry.

        By default, entries with `text is None` are skipped — useful for
        embedding pipelines that need actual strings. Pass
        `include_none=True` to keep `None` values, aligned with `labels()`.
        """
        if include_none:
            return [e.text for e in self._entries]
        return [e.text for e in self._entries if e.text is not None]

    def labels(self, *, field: str) -> list[Any]:
        """Return the value of `field` for every entry, in iteration order."""
        return [getattr(e, field) for e in self._entries]

    def to_dataframe(self) -> Any:
        """Return a pandas DataFrame view of the corpus.

        Requires the optional `pandas` extra. Each row is one entry; each
        column is one field. URLs and enums are serialized to strings.
        """
        try:
            import pandas as pd
        except ImportError as exc:
            raise ImportError(
                "to_dataframe() requires pandas; install the pandas extra: "
                'uv add "touchstones[pandas]"'
            ) from exc

        rows = [e.model_dump(mode="json") for e in self._entries]
        return pd.DataFrame(rows)


corpus: Corpus = Corpus.load_default()
