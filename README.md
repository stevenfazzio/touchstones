# touchstones

A curated corpus of **standard example texts** — the specific verbatim strings that fields reach for when they need a canonical example. The Rainbow Passage (speech pathology). "The quick brown fox jumps over the lazy dog" (keyboard and font tests). "Hello, World!" in K&R C. The Harvard Sentences. The SHA-256 "abc" test vector. The Phi X 174 genome. Lorem Ipsum. The Preamble to the US Constitution.

Every entry is a short, verbatim, public-domain or fair-use text with a clean answer to *"when a practitioner of X needs Y, what specific text do they reach for?"* Each one ships with historical context, known issues, and a link to its authoritative source.

## What this is for

Touchstones is **breadth-optimized**: the goal is not size but diversity across the dimensions where embedding and language models behave differently. Most public corpora are dense in one region (Brown = American journalism, C4 = web English, the Pile = English-leaning mixed) and thin or absent everywhere else. Touchstones is the opposite — deliberately sparse, but spread across language, script, structural type, register, and discipline. **Schelling-point selection** ("texts every field independently coordinates on") is what makes the breadth tractable and reproducible: anyone trying to build the same corpus from scratch would converge on roughly the same texts.

The primary intended use is **diagnostic analysis of text embedding and language models** — figuring out which features of text a given model is actually sensitive to. Concrete questions Touchstones is built to support:

- **Feature sensitivity.** Embed every entry, compute pairwise cosines: which axis (language, script, type, length, discipline) dominates the similarity structure of model X?
- **Model comparison.** Embed everything with two models and compare. Where do they agree? Where do they diverge, and on which feature?
- **Collapse detection.** Does this model treat all foreign-language text as similar? All code? All test vectors? A breadth-optimized corpus surfaces collapse on inspection; a uniform corpus hides it.
- **Calibration against intuitive ground truth.** Does the model think the Rainbow Passage is closer to the Harvard Sentences than to the SHA-256 vector? If not, why not?

The framing is **diagnostic probe, not benchmark.** Touchstones is sized for *exploratory* claims ("this model collapses code into prose," "this model is length-dominated below 50 tokens") rather than *confirmatory* ones with p-values. Use it upstream of MTEB-style benchmarks — to find the behavior worth investigating, then build a targeted benchmark for that behavior.

It is also useful as a small, well-attributed public dataset for **tool authors** writing documentation examples, **educators** teaching embedding / tokenization / parsing, and **researchers** probing memorization or building decontamination lists for evaluation sets.

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
    print(entry.name, "—", entry.discipline, "—", entry.language, entry.script)

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

The corpus currently has **56 entries** across 5 categories (`natural_language` 38, `code` 7, `sequence` 4, `notation` 4, `protocol` 3). Every entry has verbatim, non-empty `text`. Six breadth-filling batches plus a curatorial correction have moved the diagnostic shape from a starting 11/19 `language=english` and 19/19 `script=latin` to 13/56 and 46/56: the first non-Latin batch (10 entries) opened 9 non-Latin scripts; the underpopulated-categories batch (7 entries) brought `code`, `notation`, and `protocol` each to N≥3; two UDHR Article 1 parallel-text batches (12 entries plus a French pangram follow-on) added 16 non-English natural-language cells, including the first Bantu (Swahili), Austronesian (Indonesian), and Austroasiatic (Vietnamese) language-family entries; a natural-sciences batch (3 entries: Newton's *Axiomata sive Leges Motus*, Sanger's bovine insulin sequence, caffeine SMILES) opened the corpus's first physics, biochemistry, and cheminformatics cells; a deficit-defined-canonicity batch (5 entries: Apple's `goto fail`, the OpenSSL Heartbleed `tls1_process_heartbeat` excerpt, Duff's Device, Chomsky's "Colorless green ideas sleep furiously", Bever's "The horse raced past the barn fell") introduced a new curatorial lens — texts canonical *because of* a flaw they have or a property they lack — and used it to nearly double the `code` category and to make the first lens-justified additions to the dense English cell; and a curatorial correction removed the Pi to 100 Decimal Places entry on the grounds that it failed the per-entry selection rule (the 100-digit cutoff is conventional rather than canonical, and the truncated-vs-rounded ambiguity means there is no single canonical bag of bytes), the same failure mode as Lena, the Utah Teapot, and the Mandelbrot set. The remaining first-wave priority is breaking the English monoculture within Latin script via *non-English* additions — high-leverage Latin-script languages still absent include Czech, Hungarian, Turkish, Tagalog, and Romanian.

Target size: **~1500–2000 entries**, reached in three phases:

1. **Breadth.** Fill ~80% of identified cells in the `(category, language, script, discipline)` space at N=1. Estimated 200–400 entries.
2. **Selective densification.** Bring the 20–30 most analysis-critical cells to N=5–10 each. Estimated +200–500 entries.
3. **Family expansion.** Use anchor-and-neighbors curation (each existing entry becomes the seed of a small family of similar standard texts) to reach the final size.

10k+ is explicitly *not* the near-term target — past ~2k, per-entry depth has to drop and the project becomes a different product.

See [`docs/coverage.md`](docs/coverage.md) for the full breadth-axis structure, the diagnostic snapshot, and the growth plan. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the per-entry selection rule, field reference, and proposal process.
