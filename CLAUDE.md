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

1. **`schema.py` — `Entry` is the source of truth.** Every field is validated by Pydantic, and the model is `frozen=True` with `extra="forbid"`. `text`, `length_tokens`, `language`, and `script` are all **required** — every entry bundles a verbatim standard text, no exceptions. `language` and `script` together with `category` and `discipline` form the four orthogonal **breadth axes** the corpus is structured around (see `docs/coverage.md`). The cross-field invariants live in a single `model_validator(mode="after")` (`_check_invariants`):
   - `discipline` must appear in `disciplines`
   - entries can't self-reference in `related`
   - `disciplines` / `related` / `tags` must be deduped
   When adding a new constraint, extend this validator and add a matching test in `tests/test_schema.py` rather than scattering checks across call sites.

2. **`corpus.py` — `Corpus` enforces collection-level invariants.** The constructor verifies name uniqueness and (by default) that every `related` reference resolves to an existing entry — these can't be expressed on a single `Entry` and only make sense once you have the whole list. `filter()` passes `check_related=False` to the constructor when building subsets, because a filtered view can legitimately omit an entry that another retained entry references. The module-level singleton `corpus = Corpus.load_default()` is built **eagerly at import time** from `data/entries.json` via `importlib.resources`, so a malformed `entries.json` fails at `import touchstones`, not lazily later. Keep this property — it's the whole point of having a schema.

3. **`io.py` — JSON round-trips go through a `TypeAdapter[list[Entry]]`.** `load_entries` / `save_entries` are the only sanctioned way to read/write the data file; both rely on Pydantic's JSON mode so URLs serialize as plain strings and enums as their string values, keeping `entries.json` human-editable. `count_tokens` is a contributor helper that imports `tiktoken` lazily because tiktoken is a dev-only extra — do not promote it to a runtime dep.

`pandas` is similarly an optional extra. `Corpus.to_dataframe()` imports it lazily and raises `ImportError` with install instructions; preserve this pattern for any future optional integrations so the base install stays at just `pydantic`.

## Selection rule

Every entry in the corpus must pass this test: **"When a practitioner of [field] needs [kind of example], what specific verbatim string do they reach for?"** If you can name the field, the need, and the exact string, the entry fits. If the "thing" is famous but doesn't have a canonical verbatim text people reuse (Lena, Utah Teapot, Iris dataset, Mandelbrot set), it does not belong in this corpus. See `CONTRIBUTING.md` for worked examples and the proposal process.

The selection rule above qualifies an entry **in principle**. The complementary test, applied at proposal time, is the **breadth-axis test**: does the entry fill (or strengthen) a useful cell in the four-axis `(category, language, script, discipline)` space defined in `docs/coverage.md`? An entry can pass the per-entry rule and still be a poor *next addition* if it duplicates an already-dense cell. As of this writing the corpus is 11/49 `language=english` and 39/49 `script=latin` (down from a starting 11/19 and 19/19 thanks to four breadth-filling batches), so a new English-natural-language entry still needs an unusually strong reason; an entry that opens a previously empty cell — a non-Latin script, a new programming/notation/protocol language, or an underpopulated discipline — effectively justifies itself.

## Status note

`src/touchstones/data/entries.json` contains 49 entries across 5 `Category` enum values: `natural_language` (35), `code` (4), `sequence` (4), `notation` (3), `protocol` (3). Every entry has non-empty `text`; there are no metadata-only records. The corpus has now been through four breadth-filling batches: the first non-Latin batch (10 entries) broke the script monoculture; the underpopulated-categories batch (7 entries: K&R wc, SICP factorial, Thompson quine, Dragon-book grammar, Wirth syntax notation, RFC 5321 SMTP, RFC 1035 DNS) brought `code`, `notation`, and `protocol` each to N≥3; the first UDHR parallel-text batch (6 UDHR Article 1 translations — French, Spanish, German, Italian, Portuguese, Polish — plus the Triouleyre 1921 French pangram as a small follow-on) opened seven new Latin-script natural-language cells; and the second UDHR parallel-text batch (6 more UDHR Article 1 translations — Latin, Dutch, Catalan, Swahili, Indonesian, Vietnamese) added a verifiable real-Latin entry to pair against Lorem Ipsum and opened the corpus's first Bantu, Austronesian, and Austroasiatic language-family cells. Remaining first-wave priority: continue breaking the English monoculture within Latin script. English's share has dropped from 11/19 → 11/36 → 11/43 → 11/49 as the corpus has grown, but the absolute count is unchanged and many high-leverage Latin-script languages (Czech, Hungarian, Turkish, Tagalog, …) are still absent. The corpus targets ~1500–2000 entries via the three-phase plan described in `docs/coverage.md`. The test suite has two layers:

- `tests/test_schema.py` exercises the `Entry` validators against an in-memory `minimal_entry_dict` fixture (a placeholder, **not** a real corpus entry). When changing the schema, update the fixture and the relevant validator test together.
- `tests/test_corpus.py` tests the full Corpus API against the real singleton (lookup, filter, iteration, texts, labels, related cross-references, DataFrame export).

When adding entries, route the change through `CONTRIBUTING.md`'s field reference and run `uv run pytest` — schema and corpus-level validation both run at load time, so a malformed entry will surface immediately.
