# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common commands

This project uses `uv`. Run everything through it so the venv stays in sync.

- Install dev deps: `uv sync --extra dev`
- Run the full test suite: `uv run pytest`
- Run a single test: `uv run pytest tests/test_schema.py::test_round_trip`
- Lint: `uv run ruff check .`
- Auto-fix lint: `uv run ruff check --fix .`
- Format check: `uv run ruff format --check .`

## Architecture

Touchstones is a small, data-first Python package (src/ layout, `src/touchstones/`). The runtime surface is intentionally minimal: a Pydantic schema, a JSON file of entries, and a thin `Corpus` wrapper. Three pieces hold the design together:

1. **`schema.py` — `Entry` is the source of truth.** Every field is validated by Pydantic, and the model is `frozen=True` with `extra="forbid"`. The cross-field invariants live in a single `model_validator(mode="after")` (`_check_invariants`) and are not optional — they encode the corpus's contracts:
   - `discipline` must appear in `disciplines`
   - `length_tokens` is required iff `text` is set (both-or-neither)
   - `license_status="copyrighted"` forbids bundling `text` (use `fair_use` for excerpts)
   - entries can't self-reference in `related`
   - `disciplines` / `related` / `tags` must be deduped
   When adding a new constraint, extend this validator and add a matching test in `tests/test_schema.py` rather than scattering checks across call sites.

2. **`corpus.py` — `Corpus` enforces collection-level invariants.** The constructor verifies name uniqueness and that every `related` reference resolves to an existing entry — these can't be expressed on a single `Entry` and only make sense once you have the whole list. The module-level singleton `corpus = Corpus.load_default()` is built **eagerly at import time** from `data/entries.json` via `importlib.resources`. That means a malformed `entries.json` will fail at `import touchstones`, not lazily later. Keep this property — it's the whole point of having a schema.

3. **`io.py` — JSON round-trips go through a `TypeAdapter[list[Entry]]`.** `load_entries` / `save_entries` are the only sanctioned way to read/write the data file; both rely on Pydantic's JSON mode so URLs serialize as plain strings and enums as their string values, keeping `entries.json` human-editable. `count_tokens` is a contributor helper that imports `tiktoken` lazily because tiktoken is a dev-only extra — do not promote it to a runtime dep.

`pandas` is similarly an optional extra. `Corpus.to_dataframe()` imports it lazily and raises `ImportError` with install instructions; preserve this pattern for any future optional integrations so the base install stays at just `pydantic`.

## Status note (v0.1)

`src/touchstones/data/entries.json` contains 6 seed entries spanning multiple categories and license statuses. The test suite has two layers:

- `tests/test_schema.py` exercises the `Entry` validators against an in-memory `minimal_entry_dict` fixture (a placeholder, **not** a real corpus entry). When changing the schema, update the fixture and the relevant validator test together.
- `tests/test_corpus.py` tests the full Corpus API against the real singleton (lookup, filter, iteration, texts, labels, related cross-references, DataFrame export).

When adding entries, route the change through `CONTRIBUTING.md`'s field reference and run `uv run pytest` — schema and corpus-level validation both run at load time, so a malformed entry will surface immediately.
