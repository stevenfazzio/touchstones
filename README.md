# touchstones

A curated corpus of **standard example texts** — the specific verbatim strings that fields reach for when they need a canonical example. The Rainbow Passage (speech pathology). "The quick brown fox jumps over the lazy dog" (keyboard and font tests). "Hello, World!" in K&R C. The Harvard Sentences. Lorem Ipsum. The Preamble to the US Constitution. The SHA-256 "abc" test vector. The Phi X 174 genome.

Every entry is a short, verbatim, public-domain or fair-use text with a clean answer to the question *"when a practitioner of X needs Y, what specific text do they reach for?"* Each one ships with historical context, known issues, and a link to its authoritative source — so you can use the corpus as a small, labeled, human-readable dataset for demoing UMAP, DataMapPlot, Toponymy, sentence-transformers, or any tokenization / embedding / retrieval pipeline.

## Installation

```bash
uv add touchstones
```

For the DataFrame view:

```bash
uv add "touchstones[pandas]"
```

## Usage

```python
from touchstones import corpus

# Iterate
for entry in corpus:
    print(entry.name, "—", entry.discipline)

# Look up by name
rainbow = corpus["The Rainbow Passage"]
print(rainbow.text)
print(rainbow.description)

# Filter by discipline (matches both `discipline` and the `disciplines` list)
speech = corpus.filter(discipline="speech pathology")

# Texts and labels, ready for embedding pipelines
texts = corpus.texts()
labels = corpus.labels(field="discipline")

# DataFrame view (requires the `pandas` extra)
df = corpus.to_dataframe()
```

## Status

**v0.1** ships with 19 seed entries across 5 categories — `natural_language`, `code`, `notation`, `sequence`, and `protocol`. Every entry has verbatim, non-empty `text`; there are no metadata-only records. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the selection rule, proposal process, and field reference.
