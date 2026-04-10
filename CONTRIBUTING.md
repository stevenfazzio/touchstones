# Contributing to touchstones

Touchstones is a curated corpus, not a crowd-sourced dump. Quality matters more than quantity — we'd rather have 50 deeply documented entries than 500 superficial ones.

## What makes a good entry

A canonical reference artifact:

- Is **widely used** as a standard, benchmark, or go-to example in its field.
- Has **historical depth** — there is a story behind why it became canonical.
- Has **documented properties** — known biases, controversies, or replacements that researchers care about.
- Is **legally clear** — public domain, fair use, or correctly attributed.

Examples that fit: the Iris dataset, the Boston Housing dataset (with its known issues), the Lena image, "The North Wind and the Sun," Anscombe's Quartet, the Utah Teapot, "Hello, World!" in K&R C, the Harvard Sentences.

Examples that don't fit: a personal favorite dataset; a recent paper's benchmark with no historical traction; copyrighted material we can't legally include.

## Proposing a new entry

1. Open an issue describing the artifact and why it is canonical.
2. Once accepted, open a PR adding the entry to `src/touchstones/data/entries.json`.
3. Run the test suite (`uv run pytest`) to confirm validation passes.

## Field reference

Each entry must include the following fields. See `src/touchstones/schema.py` for the authoritative definitions.

| Field | Type | Notes |
|---|---|---|
| `name` | str | Short canonical name. Used as the corpus key — must be unique. |
| `text` | str or null | The actual text content. Must be `null` if `license_status` is `copyrighted`. |
| `discipline` | str | Primary field of use. Must appear in `disciplines`. |
| `disciplines` | list[str] | All fields where this artifact is used. No duplicates. |
| `category` | str | One of: `natural_language`, `sequence`, `notation`, `visual`, `audio`, `tabular`, `code`, `3d_model`, `mathematical`, `protocol`. |
| `year_introduced` | int | Year first published or standardized. BCE values are negative. |
| `creator` | str | Person or organization. Use "Anonymous" or "Folk tradition" if unknown. |
| `source` | str | Original publication or standard, with citation. |
| `description` | str | 1–3 sentences: what it is and why it is canonical. |
| `usage` | str | What the artifact is used to test, demonstrate, or benchmark. |
| `known_issues` | str or null | Documented problems, biases, or controversies. `null` if none known. |
| `alternatives` | str or null | Known replacements or modernized versions, with explanation. `null` if none known. |
| `related` | list[str] | Names of other corpus entries that are connected. Empty list if none. |
| `length_tokens` | int or null | Approximate cl100k_base token count. **Required when `text` is set; must be `null` when `text` is `null`.** |
| `license_status` | enum | One of: `public_domain`, `fair_use`, `copyrighted`, `unclear`. |
| `tags` | list[str] | Freeform tags for cross-cutting themes. No duplicates. |
| `url` | str (URL) | Link to authoritative source or full text. |

## Computing `length_tokens`

```python
from touchstones.io import count_tokens
n = count_tokens("the actual text...")
```

The helper uses `tiktoken` with the `cl100k_base` encoding (the GPT-4 tokenizer, which most embedding models approximate). Install `tiktoken` via `uv sync --extra dev` if you don't already have it.

## Licensing rules

- **`public_domain`**: include the text.
- **`fair_use`**: short excerpts of copyrighted works that clearly qualify under fair use (e.g., a single sentence used to demonstrate a phonetic standard). Include the excerpt.
- **`copyrighted`**: do not include the text. Set `text = null` and provide a `url` to an authoritative source. Use `description` and `usage` to give the entry value as a metadata-only record.
- **`unclear`**: when in doubt, set `license_status = "unclear"` and `text = null`.

## Depth over breadth

The v1.0 ceiling is **50 entries**. Every entry should be the kind of thing where someone reads `description`, `usage`, and `known_issues` and says "huh, I didn't know that's where that came from."
