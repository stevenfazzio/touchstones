# Contributing to touchstones

Touchstones is a curated corpus of **standard example texts** — specific verbatim strings that fields reach for when they need a canonical example. Quality matters more than quantity.

## The selection rule

Every proposed entry must pass this test:

> **When a practitioner of [field] needs [kind of example], what specific verbatim text do they reach for?**

If you can name the field, the need, and the exact string — *and* the string is short, publicly available, and uncontroversially public-domain or fair-use — the entry probably fits. If you can't, it doesn't.

### Examples that pass

- **Speech pathologist** → reading passage for voice assessment → **The Rainbow Passage**
- **Phonetician** → cross-linguistic IPA comparison passage → **The North Wind and the Sun**
- **C instructor** → minimal program for new toolchains → **"Hello, World!" in K&R C**
- **Graphic designer** → placeholder body text → **Lorem Ipsum**
- **SHA-256 implementer** → canonical correctness test vector → **"abc" → ba7816bf...015ad (FIPS 180-4 §B.1)**
- **TTS/ASR researcher** → demo utterance → **"Mary had a little lamb"**
- **Font/keyboard designer** → English pangram → **"The quick brown fox jumps over the lazy dog"**
- **Illumina sequencing technician** → spike-in control → **The Phi X 174 genome (NC_001422)**
- **NLP researcher** → parallel-text benchmark → **UDHR Article 1**

### Examples that fail

- **The Utah Teapot** — famous, but it's a 3D mesh, not a text people copy-paste.
- **The Iris dataset** — reached for via library import (`sklearn.datasets.load_iris()`), not as a text string anyone bundles.
- **The Mandelbrot set** — a mathematical object with no canonical textual form.
- **The Rosetta Stone** — famous, but no community reaches for "the text of the Rosetta Stone" as a standard reference text.
- **Dijkstra's 1959 shortest-path example** — referenced as a concept, not embedded as a specific verbatim string.

## What makes a good entry

1. **Specific.** There is one exact string that the community uses, not a paraphrasable idea.
2. **Verbatim.** You can point to an authoritative source and the bundled text matches it exactly. Never paraphrase or reconstruct.
3. **Short.** Most good entries are one to a few paragraphs. Long entries are fine when the whole thing is the standard (the Gettysburg Address, the Phi X 174 genome) but the bias is toward "short enough to skim".
4. **Public-domain or fair-use.** See the licensing rules below.
5. **Documented history.** There's a story behind why it became canonical, and it's worth reading in the `description`, `usage`, and `known_issues` fields.

## Proposing a new entry

1. Open an issue describing the artifact, the field that uses it, the specific need it fills, and the authoritative source for the verbatim text.
2. Once accepted, open a PR adding the entry to `src/touchstones/data/entries.json`.
3. Run the test suite (`uv run pytest`) to confirm validation passes.

## Field reference

Each entry must include the following fields. See `src/touchstones/schema.py` for the authoritative definitions.

| Field | Type | Notes |
|---|---|---|
| `name` | str | Short canonical name. Used as the corpus key — must be unique. |
| `text` | str | **Required, non-empty.** The verbatim standard text itself. No editorial trailers, no "[source: …]" footers, no paraphrases. |
| `discipline` | str | Primary field of use. Must appear in `disciplines`. |
| `disciplines` | list[str] | All fields where this artifact is used. No duplicates. |
| `category` | str | One of: `natural_language`, `code`, `notation`, `sequence`, `protocol`. |
| `year_introduced` | int | Year first published or standardized. BCE values are negative. |
| `creator` | str | Person or organization. Use "Anonymous" or "Traditional" if unknown. |
| `source` | str | Original publication or standard, with citation. |
| `description` | str | 1–3 sentences: what it is and why it is canonical. |
| `usage` | str | Name the **[field + need + this exact text]** triple explicitly. |
| `known_issues` | str or null | Documented problems, biases, or controversies. `null` if none known. |
| `alternatives` | str or null | Known replacements or modernized versions, with explanation. `null` if none known. |
| `related` | list[str] | Names of other corpus entries that are connected. Empty list if none. |
| `length_tokens` | int | **Required.** Approximate cl100k_base token count of `text`. Use `count_tokens`. |
| `license_status` | enum | One of: `public_domain`, `fair_use`, `unclear`. |
| `tags` | list[str] | Freeform tags for cross-cutting themes. No duplicates. |
| `url` | str (URL) | Link to the authoritative source or full text. |

## Computing `length_tokens`

```python
from touchstones.io import count_tokens
n = count_tokens("the actual text...")
```

The helper uses `tiktoken` with the `cl100k_base` encoding (the GPT-4 tokenizer, which most embedding models approximate). Install `tiktoken` via `uv sync --extra dev` if you don't already have it.

## Licensing rules

- **`public_domain`** — include the verbatim text. Pre-1929 US publications, US federal government works, and documents released without copyright restriction (UN documents, FIPS standards, RFCs) all qualify.
- **`fair_use`** — include a short verbatim excerpt that clearly qualifies as fair use (e.g., a single sentence or a short stanza used to demonstrate a phonetic or notational standard). The entry must still bundle the actual text.
- **`unclear`** — when in doubt, use `unclear` and include a short representative excerpt under fair-use reasoning.

Entries with `text = null` or metadata-only records are **not accepted**. If the artifact you want to propose can't be represented as a verbatim text anyone reuses, it doesn't fit this corpus.

## Growth and curation

There is no hard cap on corpus size, but each addition must pass the [field + need + verbatim text] rule above. A small corpus of deeply-documented canonical texts is more useful than a large one diluted with marginally-relevant entries. When in doubt, err on the side of rejection: it's easier to add a missing entry later than to prune a mediocre one.
