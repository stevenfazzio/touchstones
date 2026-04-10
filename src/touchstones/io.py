"""IO utilities for the touchstones corpus.

`load_entries` and `save_entries` provide validated round-trips against
the JSON data file. `count_tokens` is a contributor helper that computes
the canonical `length_tokens` value using `tiktoken`'s `cl100k_base`
encoding (the GPT-4 tokenizer, which most embedding models approximate).

`tiktoken` is a development-only dependency: `count_tokens` imports it
lazily so the runtime install stays minimal.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import TypeAdapter

from touchstones.schema import Entry

_entries_adapter: TypeAdapter[list[Entry]] = TypeAdapter(list[Entry])


def load_entries(path: str | Path) -> list[Entry]:
    """Load and validate a list of `Entry` objects from a JSON file.

    Raises `pydantic.ValidationError` if any entry fails the schema.
    """
    return _entries_adapter.validate_json(Path(path).read_bytes())


def save_entries(entries: list[Entry], path: str | Path) -> None:
    """Serialize entries to JSON and write them to `path`.

    Uses Pydantic's JSON dumping so URLs become plain strings and enums
    become their string values; the file stays human-editable.
    """
    payload = _entries_adapter.dump_json(entries, indent=2)
    Path(path).write_bytes(payload)


def count_tokens(text: str) -> int:
    """Return the cl100k_base token count for `text`.

    Used by contributors to populate the `length_tokens` field when
    adding a new entry. Imports `tiktoken` lazily so it can stay a
    development-only dependency.
    """
    try:
        import tiktoken
    except ImportError as exc:
        raise ImportError(
            "count_tokens requires tiktoken; install the dev extras: uv sync --extra dev"
        ) from exc

    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))
