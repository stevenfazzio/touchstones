# touchstones

A curated corpus of **standard example texts** — the specific verbatim strings that fields reach for when they need a canonical example. The Rainbow Passage (speech pathology). "The quick brown fox jumps over the lazy dog" (keyboard and font tests). "Hello, World!" in K&R C. The Harvard Sentences. The SHA-256 "abc" test vector. The Phi X 174 genome. Lorem Ipsum. The Preamble to the US Constitution.

Every entry is a short, verbatim, public-domain or fair-use text with a clean answer to *"when a practitioner of X needs Y, what specific text do they reach for?"* Each one ships with historical context, known issues, and a link to its authoritative source.

## What this is for

Touchstones is **breadth-optimized**: the goal is not size but diversity across the dimensions where embedding and language models behave differently. Most public corpora are dense in one region (Brown = American journalism, C4 = web English, the Pile = English-leaning mixed) and thin or absent everywhere else. Touchstones is the opposite — deliberately sparse, but spread across language, script, structural type, register, and discipline. **Schelling-point selection** ("texts every field independently coordinates on") is what makes the breadth tractable and reproducible: anyone trying to build the same corpus from scratch would converge on roughly the same texts.

The primary intended use is **diagnostic analysis of text embedding and language models** — figuring out which features of text a given model is actually sensitive to. Concrete questions Touchstones is built to support:

- **Feature sensitivity.** Embed every entry, compute pairwise cosines: which axis (category, language, script, discipline, length) dominates the similarity structure of model X?
- **Model comparison.** Embed everything with two models and compare. Where do they agree? Where do they diverge, and on which feature?
- **Collapse detection.** Does this model treat all foreign-language text as similar? All code? All test vectors? A breadth-optimized corpus surfaces collapse on inspection; a uniform corpus hides it.
- **Calibration against intuitive ground truth.** Does the model think the Rainbow Passage is closer to the Harvard Sentences than to the SHA-256 vector? If not, why not?

The framing is **diagnostic probe, not benchmark.** Touchstones is sized for *exploratory* claims ("this model collapses code into prose," "this model is length-dominated below 50 tokens") rather than *confirmatory* ones with p-values. Use it upstream of MTEB-style benchmarks — to find the behavior worth investigating, then build a targeted benchmark for that behavior.

It is also useful as a small, well-attributed public dataset for **tool authors** writing documentation examples, **educators** teaching embedding / tokenization / parsing, and **researchers** probing memorization or building decontamination lists for evaluation sets.

## Installation

Touchstones is pre-1.0 and not yet published to PyPI. Install from source:

```bash
git clone https://github.com/stevenfazzio/touchstones.git
cd touchstones
uv sync
```

For the DataFrame view, include the `pandas` extra:

```bash
uv sync --extra pandas
```

## Usage

```python
from touchstones import corpus

# How big is the corpus, and is a given entry in it?
len(corpus)
"The Rainbow Passage" in corpus

# Iterate. Every entry exposes the four breadth axes the corpus is built around.
for entry in corpus:
    print(entry.name, "—", entry.category, entry.language, entry.script, entry.discipline)

# Look up by name
rainbow = corpus["The Rainbow Passage"]
print(rainbow.text)
print(rainbow.description)

# Filter on discipline, category, or tag (combine kwargs for AND).
speech = corpus.filter(discipline="speech pathology")
code_only = corpus.filter(category="code")
udhr = corpus.filter(tag="parallel-text")

# Texts and labels, ready for embedding pipelines
texts = corpus.texts()
labels = corpus.labels(field="discipline")

# DataFrame view (requires the `pandas` extra)
df = corpus.to_dataframe()
```

## At a glance

**57 entries** across 6 categories:

| category           | count |
| ------------------ | ----: |
| `natural_language` |    38 |
| `code`             |     7 |
| `sequence`         |     4 |
| `notation`         |     4 |
| `protocol`         |     3 |
| `dataset`          |     1 |

Diagnostic ratios the project is actively trying to move:

- `language=english`: **13 / 57**
- `script=latin`: **47 / 57**

The current first-wave priority is breaking the English monoculture within Latin script via *non-English* additions. See [`docs/coverage.md`](docs/coverage.md) for the full diagnostic snapshot, the four breadth axes, and the batch history.

## Roadmap

Target size: **~1500–2000 entries**, reached in three phases:

1. **Breadth.** Fill ~80% of identified cells in the `(category, language, script, discipline)` space at N=1. Estimated 200–400 entries.
2. **Selective densification.** Bring the 20–30 most analysis-critical cells to N=5–10 each. Estimated +200–500 entries.
3. **Family expansion.** Use anchor-and-neighbors curation (each existing entry becomes the seed of a small family of similar standard texts) to reach the final size.

10k+ is explicitly *not* the near-term target — past ~2k, per-entry depth has to drop and the project becomes a different product.

## License

Touchstones is pre-1.0 and a top-level `LICENSE` file is still TODO. The intent is a permissive open-source license for the package code (the Pydantic schema, the `Corpus` wrapper, and the I/O helpers).

Each *entry* in the corpus carries its own `license_status` field — `public_domain`, `fair_use`, or `unclear` — recorded per-text. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the per-entry licensing rules.

## See also

[`docs/coverage.md`](docs/coverage.md) for the full breadth-axis structure, the diagnostic snapshot, and the growth plan. [`CONTRIBUTING.md`](CONTRIBUTING.md) for the per-entry selection rule, field reference, and proposal process.
