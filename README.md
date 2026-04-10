# touchstones

A curated corpus of canonical reference artifacts — the texts, images, datasets, and standards that fields use as their go-to examples. The Rainbow Passage. Anscombe's Quartet. The Lena image. The Utah Teapot. "Hello, World!" in K&R C. The Miranda warning.

Touchstones is built for the PyData ecosystem: it gives you a small, deeply documented dataset where every entry has historical context, known issues, and links to authoritative sources. Useful for demoing UMAP, DataMapPlot, Toponymy, sentence-transformers, or any tool that benefits from a labeled, diverse corpus that humans can actually read.

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

**v0.1 is schema-only.** The data schema is defined, validated, and tested, but no entries have been seeded yet. The corpus loads as an empty list. Entries will land in the next release. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the proposal process and field reference.
