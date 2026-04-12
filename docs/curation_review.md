# Curation review

A research-grounded audit of how Touchstones engages with corpus-curation literature, anchored against three risks named by the maintainer (in priority order):

1. **Utility** — building a corpus that doesn't end up actually useful for diagnostic probing of embedding/LM feature sensitivity.
2. **Bias / arbitrariness** — selection that looks idiosyncratic or has unexamined blind spots.
3. **Tooling** — picking the wrong storage/schema/distribution model for the target scale (~1500–2000 entries).

This document draws on two complementary source pools:

- **Code projects** — what experienced curators actually do in production. The motivation: a semantic-similarity search against the top ~10k GitHub repos found that Touchstones' nearest neighbors sit at cosine 0.38–0.43 — topically adjacent (NLTK, Stanza, sentence-transformers, NLP-progress, MTEB, BIG-bench) but not structurally analogous. There is no "do it like X" project to copy. That novelty raises the antipattern risk and makes seeing how *real* curated probe-style projects organize themselves load-bearing.
- **Methodology and critique literature** — what the field thinks doing this kind of work *well* looks like. Code repos are excellent at showing *what* curators do; papers say *why* certain practices matter and *which failure modes have been characterized*.

Where the two pools converge on the same finding, that's the strongest single warrant for action. Where they diverge, the divergence is itself the finding.

Sources read for this review:

- **Code projects:** `google/BIG-bench`, `embeddings-benchmark/mteb`, `EleutherAI/lm-evaluation-harness`, `huggingface/datasets` (architecture + dataset card spec + FLORES/MASSIVE practice), `nltk/nltk`, `sebastianruder/NLP-progress`.
- **Papers — utility:** Belinkov & Glass 2019 (NLP analysis methods survey), Hewitt & Liang 2019 (control tasks), Pimentel et al. 2020 (information-theoretic critique), Kriegeskorte, Mur & Bandettini 2008 (RSA original), **Chrupała, Higy & Alishahi 2020 (Picking BERT's Brain — RSA applied to BERT embeddings; the closest direct precedent)**, Walther et al. 2016 (RSA reliability), Tenney et al. 2019, Srivastava et al. 2022 (BIG-bench paper).
- **Papers — bias:** Gebru et al. 2018/2021 (Datasheets for Datasets), Bender & Friedman 2018 (Data Statements for NLP), Crawford & Paglen 2019 (Excavating AI), Birhane & Prabhu 2021; Bender et al. 2021 (Stochastic Parrots) and Torralba & Efros 2011 referenced briefly without quotation due to access limitations.
- **Papers — tooling:** Mitchell et al. 2019 (Model Cards), Pushkarna, Zaldivar & Kjartansson 2022 (Data Cards / OFTEn framework), MLCommons 2024 (Croissant metadata format).

This document does not propose any code changes. It only maps gaps and recommends.

---

## Part 1: Framework engagement

### §1 — Utility

**The single most important finding from this entire review: Touchstones is doing representational similarity analysis (RSA), not probing-classifier work.** That framing comes from the literature lens, and it changes everything else in this section.

The Hewitt & Liang 2019 / Pimentel et al. 2020 debate that dominates the NLP probing literature is about whether to use simple selectivity-controlled classifiers or maximally-powerful complex ones. Touchstones uses *no probe at all* — it computes cosine similarity directly on raw embeddings, then asks which axis dominates the resulting structure (`README.md:13`). That puts Touchstones in a different methodological space from the entire probing-classifier tradition. Its real lineage is the cognitive-neuroscience tradition founded by Kriegeskorte, Mur & Bandettini 2008.

This isn't a small framing point. Belinkov & Glass 2019, the canonical NLP analysis methods survey, organizes around six categories — and RSA gets minimal coverage. The survey mentions "directly computing correlations between neural network activations and some property" in passing but does not systematically engage with the RSA tradition. NLP analysis converged on probing-classifier methodology while RSA was being developed in parallel by cognitive neuroscientists. Touchstones is methodologically more isolated within mainstream NLP than its topical neighbors suggested — its real lineage is RSA, and that lineage is under-represented in NLP-survey literature.

**The closest direct precedent: Picking BERT's Brain (Chrupała, Higy & Alishahi 2020).** This is the most directly comparable existing project I found. They apply RSA to BERT embeddings to probe linguistic dependencies (subject-verb sensitivity, pronoun coreference, sentence heads). Concrete numbers from their methodology:

- **n=200 sentences per sample, m=100 samples** for the main experiments
- Stimuli are PCFG-generated, not hand-curated
- They use Spearman's ρ for dissimilarity (not cosine — BERT embeddings violate normality, justified in their Appendix B)
- Significance via non-parametric sign test
- **Notably: diagnostic classifiers failed on the same task** ("All classifiers failed to do better than majority-class performance"), which the authors take as evidence that RSA is the appropriate method when the question is *which aspect of context dominates*, not *whether information is present*

Picking BERT's Brain both validates the RSA approach for LM embeddings and reveals that **Touchstones at 57 entries is structurally underpowered relative to the closest direct precedent** — by 2 orders of magnitude per sample. This finding bears directly on the practice-side question of whether Touchstones' selection rule is well-shaped.

#### The practice lens, mapped onto BIG-bench

The most relevant practice precedent for "what justifies adding an entry to a curated probe corpus" is BIG-bench, whose `docs/doc.md` lays out **nine explicit acceptance criteria** for new tasks. Mapping each onto Touchstones' selection rule (`CONTRIBUTING.md`, `CLAUDE.md:32–37`):

| BIG-bench criterion | Touchstones equivalent | Verdict |
|---|---|---|
| **Specificity** ("cleanly capture some specific capability") | Per-entry rule: "name the field, the need, the exact string" | **Already addressed.** Touchstones' rule is arguably stronger — it requires *all three* to be nameable. |
| **Justification** (README explains what task measures and why) | `description` + `usage` fields on `Entry` (`schema.py`) | **Already addressed**, though `usage` could lean harder on the *probe-utility* framing rather than the artifact's historical role. |
| **Novelty** (fill gaps) | Breadth-axis test (`CLAUDE.md:32–37`, `docs/coverage.md:43–56`) | **Already addressed**, more rigorously than BIG-bench. Touchstones tracks 4 axes; BIG-bench has no algorithmic coverage check. |
| **Thoroughness** ("control for, or average over, potential confounders") | None explicit | **Blind spot.** Partially mitigated by parallel-text family work; see below. |
| **Difficulty** ("not fully solvable by existing models") | None | **Defensible silence.** Touchstones isn't a benchmark; difficulty isn't the right axis. |
| **Not solvable by memorization** (no verbatim training-data overlap) | None | **Defensible silence, but worth saying out loud.** Every Touchstones entry is by design canonical and almost certainly in every LM's training corpus. This is *opposite* to BIG-bench's criterion — and it's correct for an embedding-similarity probe, where the question is "what features dominate the model's similarity structure," not "can the model solve the task." But the README doesn't currently spell out why this inversion is intentional. |
| **Size** (≥32 examples per task) | Whole corpus is 57 entries; per-cell N is typically 1 | **Open methodological question.** See N grounding below. |
| **Correctness**, **Formatting** | Pydantic validation, `frozen=True`, `extra="forbid"` | **Already addressed.** |

#### Failure modes — which transfer to direct-cosine setups, which don't

The probing-classifier literature has named a class of failure modes that the Touchstones docs don't currently engage with. The Hewitt & Liang "control task" framework requires a probe to compute selectivity, and Touchstones has none — but individual *failure modes* identified in that literature partially transfer to direct-cosine setups:

- **Length confounds — TRANSFER.** Cosine similarity on raw embeddings is sensitive to sequence length; short and long entries can cluster spuriously.
- **Type-frequency confounds — TRANSFER.** Frequent tokens dominate embedding magnitudes; similarity can be driven by which common words appear, not by the breadth axis being probed.
- **Position confounds — TRANSFER.** For models with positional encoding, early-position tokens often dominate the pooled embedding.
- **Memorization-of-classifier-weights — DOES NOT TRANSFER cleanly.** Hewitt & Liang's specific concern is that a complex probe MLP might memorize word-identity-to-label mappings; there's no MLP in Touchstones. But a *related* concern transfers: if a model has been heavily trained on canonical texts, its representations of those texts may be unusually well-clustered for reasons unrelated to the breadth axes Touchstones is probing.
- **Selectivity-vs-complexity tradeoffs — DO NOT APPLY.** No probe to tune.

The closest engagement with confound control in the current docs is the parallel-text family idea in `docs/coverage.md:90`: "when two entries differ on *exactly one axis*, the embedding-analysis use case can attribute embedding shifts to that axis with much more confidence." This is exactly the right structural mitigation, but it's named once, not enforced as a curation principle, and not tied to the underlying failure-mode vocabulary. The UDHR Article 1 family is the only place it's been operationalized at scale. **Verdict: blind spot, partially mitigated by parallel-text family work; importing the failure-mode vocabulary makes the mitigation legible.**

#### N=5–10 grounding: an empirical anchor that converges across both lenses

`docs/coverage.md:92–94` asserts N=5–10 per critical cell as the Phase 2 densification target without methodological grounding. Both lenses converge on "this is too low, and the literature doesn't cleanly answer the question."

From the practice lens: BLiMP — the closest design analog among the practice sources — uses **67 paradigms × 1000 minimal pairs each** specifically because per-paradigm claims need that much data to be statistically meaningful. Touchstones at N=1 per cell has no statistical power for per-cell claims; the three-phase plan acknowledges this by promising Phase 2 densification, but the specific N=5–10 number is intuition.

From the literature lens, the same number is even more dramatically under-grounded:

- **Picking BERT's Brain uses n=200 per sample.** That's 20–40× higher than Touchstones' Phase 2 floor, and it's the closest direct precedent for the methodology Touchstones is using.
- **Kriegeskorte 2008** explicitly does not give a minimum-N for RSA. The original paper notes that "informativeness scales quadratically" with stimulus count (96 stimuli yield 4,560 RDM parameters; 4 yield 6) but does not pick a floor.
- **Walther et al. 2016** focuses on which *dissimilarity metric* is most reliable (their answer: cross-validated Mahalanobis distance / LDC, with multivariate noise normalization) rather than how many stimuli are needed.
- Each tradition asks the question differently: RSA cares about RDM informativeness, BLiMP cares about per-paradigm hypothesis-test power, MTEB cares about cross-model leaderboard variance. None give Touchstones a clean floor.

**Verdict: honest no-answer in the literature, but with a 20–40× empirical anchor (Picking BERT's Brain) that Touchstones can cite as a sanity check.** This is the single most important finding in the review and the one that converges across both lenses.

#### Two side findings worth naming

**One:** Belinkov & Glass 2019 explicitly says the survey provides "no corpus design guidance" for probing tasks. Touchstones' four-axis breadth framework (`docs/coverage.md:43–56`) is more rigorous than what exists in the published probing literature. **This is a place where Touchstones could publish a methodological contribution** — not a recommendation per se, but a direction worth flagging.

**Two:** Walther et al. 2016 is borrowable: cross-validated Mahalanobis distance (LDC) is more reliable than cosine for representational dissimilarity. The most direct adaptation requires noise estimates from repeated stimulus presentations (which doesn't map onto LM embeddings — you can't "re-present" a text to a model and get a different reading), but the broader insight (cosine is one choice among several rather than the obvious right answer) is worth surfacing.

**BIG-bench Lite** — a 24-task subset designed for cheaper iteration — is a borrowable practice pattern: a "Touchstones Lite" of, say, 20 entries spanning all current breadth axes would give users a fast diagnostic without loading the full corpus. Cheap to add later, low priority for now.

### §2 — Bias / arbitrariness

The bias section leads with the foundational frameworks because they're foundational. The HuggingFace dataset card guide that the practice lens relies on is *literally derived* from these papers, so reading them in their original form is the right entry point.

#### Foundational frameworks: Datasheets, Data Statements, Excavating AI

**Datasheets for Datasets (Gebru et al. 2018/2021) — seven question groups in detail:** Motivation, Composition, Collection Process, Preprocessing, Uses, Distribution, Maintenance. Each group is structured as a list of explicit questions. Touchstones answers most of them implicitly across `README.md`, `CLAUDE.md`, and `docs/coverage.md`, but not in a single document under the standard headings. The "Maintenance" group is the weakest engagement: it asks who maintains the dataset, contact info, erratum policy, update frequency, communication strategy, and contribution mechanism. Touchstones documents maintenance events (batches, the Pi removal, the Iris addition) as prose in `CLAUDE.md`'s status note rather than as a structured changelog. **Verdict: partial blind spot — addressable by consolidating scattered answers into a single `docs/datasheet.md` under the standard 7-group headings.**

**Data Statements for NLP (Bender & Friedman 2018) — speaker community section.** This is the field that documents *who produced the language data*: geographic origin, socioeconomic indicators, age, native vs. non-native status, other social characteristics. For Touchstones' famous-author entries (Newton, Sanger, Chomsky) the speaker community is implicit in `creator`. For text-as-artifact-of-a-community entries (UDHR Article 1 translations, the Rainbow Passage, Lorem Ipsum's scrambled-Cicero history) the speaker community is the *load-bearing context*, and Touchstones doesn't currently capture it in any structured way.

A concrete example: the 12 UDHR Article 1 translations Touchstones currently has all came from the official UN translation effort. That's a single coordinated production context, not 12 independent ones. An embedding-similarity analysis that finds them clustered should attribute that to "they're all official UN translations of the same source text" *before* attributing it to "the embedding model treats Slavic languages similarly." Without the production-context information in the schema, that attribution can't be made cleanly. **Verdict: blind spot — addressable by widening the `creator` field's prompt in `CONTRIBUTING.md` to include "production context where the artifact is community-produced rather than individually-authored."** No schema change required.

The Data Statements **language variety axis** (dialect, register, historical period, formal/colloquial, orthographic conventions) pushes toward structured fields that `docs/coverage.md:56` rules out as non-axes. That's a defensible non-engagement: Data Statements doesn't actually provide a clean partition either; it just asks the curator to write prose. The current Touchstones approach (capture in `description` and `usage`) is consistent with the spirit of Data Statements without enforcing it as a field.

**Annotator demographics** (Data Statements): N/A — Touchstones has no annotation pipeline. **Verdict: defensible silence.** Document this as a *deliberate* N/A in the eventual `docs/datasheet.md` so a reader from the dataset-card community doesn't read it as an oversight.

**Excavating AI (Crawford & Paglen 2019) — "training data is theory."** This is the most philosophically important finding in the bias section, and it applies to Touchstones in a way the practice lens does not surface. The paper's argument: dataset categories are not neutral discoveries; they are theoretical commitments about what kinds of distinctions matter. ImageNet's "Person" subcategories embedded 19th-century physiognomy logic into computer vision because they inherited WordNet's hierarchy without questioning it.

Touchstones is much less exposed to this critique than ImageNet — its entries are public-domain canonical texts, not photographs of people, and its categories (`natural_language`, `code`, `notation`, `sequence`, `protocol`, `dataset`) are descriptive structural-shape categories, not essentialized identity categories. But the *four-axis breadth framework itself* (`docs/coverage.md:43–56`) embeds a theoretical commitment about which features models are likely sensitive to. The choice of (category, language, script, discipline) is not neutral — it reflects a particular hypothesis about what dimensions of variation embedding models will respond to. A different theory of what models care about would yield different axes.

The deliberately-not-axes list in `docs/coverage.md:56` actually surfaces this — it explicitly *names* the alternative axes considered and rejected (register, era, structure, length-band). That's better engagement with the theory-laden-choice concern than most dataset projects offer. But the *positive* axes are not framed as theoretical commitments anywhere; they're framed as orthogonal structural dimensions that just happen to be the right ones. **Verdict: blind spot, but the appropriate response is acknowledgment, not change.** A short paragraph in `docs/coverage.md` framing the four axes as theory-laden choices, defensible but not neutral, closes it cheaply. The breadth axes are well-justified for diagnostic-probe purposes; they just shouldn't be presented as if they were neutral discoveries.

**Birhane & Prabhu 2021** — recommendations about audit and removal processes. Most of the paper aims at scraped image datasets (which Touchstones is not), but one pattern is directly applicable: the "remove, replace, open" strategy. Touchstones has done one removal (Pi to 100 Decimal Places) and one category-opening addition (the Iris CSV), but the *process* for removals is ad-hoc. There is no documented procedure for "what happens when an entry is found to fail the per-entry selection rule on closer inspection." The Pi removal happened, was prose-documented, and the corpus moved on — but a future contributor wouldn't know how to propose a removal or what review it would get. **Verdict: partial gap — the precedent exists, the process doesn't.**

**Stochastic Parrots and Torralba & Efros (referenced briefly).** Both papers' arguments apply to Touchstones in attenuated form. Stochastic Parrots warns against the "myth of universality" in language coverage — Touchstones explicitly engages with this in its English-monoculture acknowledgments, already addressed. Torralba & Efros's "name that dataset" experiment shows how training-set-specific features dominate model behavior — relevant to Touchstones because every entry is by design canonical and likely in every LM training corpus (covered below). Neither requires a new recommendation.

#### Practice descendants: HuggingFace dataset cards in the wild

The HuggingFace dataset card guide is the practical descendant of Datasheets and Data Statements. It enumerates the sections a complete dataset card should contain — Dataset Description, Dataset Structure, Dataset Creation (Curation Rationale, Source Data, Annotations, Personal/Sensitive Info), Considerations for Using the Data (Social Impact, Discussion of Biases, Other Known Limitations), Additional Information (Curators, Licensing, Citation, Contributions). Mapping each onto Touchstones reproduces most of the verdicts above.

Two findings come specifically from the practice side:

**One: even high-quality dataset cards routinely leave the bias / limitations / intended-use sections blank.** The FLORES-200 card lists 200 languages with ISO 639-3 codes and licensing, but has *no* limitations section, *no* bias statement, *no* explicit intended-use boundaries, and "See paper for details" under curators. MASSIVE is similar. This is useful calibration: the prescription is much stronger than the practice, and Touchstones' current coverage is not unusual by community standards. The gap is real, but it's a community-wide gap, not a Touchstones-specific failure.

**Two: `Entry.known_issues` is the right field for "limitations of using this entry as a probe," but is currently positioned only as "what's wrong with the artifact."** The HF dataset card's "Other Known Limitations" section is exactly the broader framing. Reframing the prompt in `CONTRIBUTING.md` so contributors record both kinds of issue under the same field — artifact defects (e.g., the row-35 Iris errors) AND probe-side caveats (e.g., "this entry is short enough that length-dominated embeddings cluster it spuriously") — closes the gap with no schema change. This finding converges with the practice/literature findings on confound failure modes from §1.

### §3 — Tooling

Of the three risks, tooling is the one where the two lenses contribute the most *different* things — and where the practice lens's "JSON is fine" conclusion is correct but incomplete.

#### The practice lens: JSON is fine at this scale

HuggingFace `datasets` is Apache-Arrow-backed, memory-mapped, zero-copy, git-versioned, and explicitly designed for "internet-scale corpora" where "JSON files cannot scale." NLTK separates code from data and ships corpora as separately-downloaded modules with per-corpus licensing READMEs. NLP-progress is markdown files in language folders, with an explicit 8-step contribution checklist and a "Wish List" section for known coverage gaps.

None of these architectural choices are right for Touchstones at its target scale. The math: a current Touchstones entry is roughly 30–60 lines of pretty-printed JSON. At 2000 entries, `entries.json` would be ~150 KB — well below any threshold where Arrow's advantages kick in. Memory-mapping, streaming, lazy loading, and zero-copy are all solving problems Touchstones doesn't have. The current "eager validation at import time" property (`CLAUDE.md:16–30`, `corpus.py`) is *more* valuable at this scale than a heavier data layer would be: a malformed entry surfaces at `import touchstones`, not lazily later, and that property is the whole point of having a schema.

**Verdict on tooling architecture: defensible at every level for current and target scale.** Touchstones is correctly positioned tooling-wise for its size band. The risk is not that the current tooling won't scale; it's that the maintainer might over-engineer toward the wrong scale band.

The one borrowable idea from the practice side is **NLP-progress's "Wish List."** Touchstones already discusses wanted cells in prose (`docs/coverage.md` lists Czech, Hungarian, Turkish, Tagalog, Romanian as currently-absent high-leverage Latin-script languages). Promoting that to a structured section — or even a `data/wishlist.json` file — would make the next-priority surface explicit instead of having to be re-derived from prose each session.

#### The literature lens: positioning, n=1, and Croissant

The literature adds three things the practice lens missed:

**Model Cards (Mitchell et al. 2019) — 9 sections including Intended Use, Caveats and Recommendations, Ethical Considerations.** Touchstones is a dataset, not a model, so Model Cards aren't directly applicable. But the philosophy of *short structured documentation with explicit Intended Use, Caveats, and Out-of-Scope sections* maps onto what Touchstones already does prose-style. The paper's note that Model Cards are "short (one to two page) records" with "no machine-readable schema formally proposed" matches Touchstones' existing aesthetic of human-editable JSON + prose docs. **The literature is reassurance that a heavyweight tooling solution isn't needed**; the structural commitment (short, structured, with explicit out-of-scope) is more valuable than the format choice.

**Data Cards (Pushkarna, Zaldivar & Kjartansson 2022) — 31 themes across 6 sections, OFTEn framework.** OFTEn = Origins, Factuals, Transformations, Experience, n=1. The "n=1" framing is the most structurally illuminating finding in the entire tooling section: Data Cards explicitly identifies "n=1 examples" as a category of dataset content alongside Origins (provenance) and Factuals (aggregate properties). **Touchstones is in some sense an n=1-only dataset.** Every entry is one canonical artifact; there is no statistical aggregation, no sampling, no representative summarization. The Data Cards literature gives Touchstones a methodological vocabulary it didn't realize it had: Touchstones is a *deliberate n=1 documentation framework applied to embedding-model probing*. That framing is more precise than "diagnostic probe, not benchmark" and is worth borrowing.

The Data Cards paper also gives a useful tooling reality check: the authors used Google Docs and report its limitations ("fragmentation, lost intent, inability to automate"). Their recommendation: "Both human-written contextual explanations and automated fields where accuracy matters." Touchstones' Pydantic + JSON setup is closer to that hybrid than either pure prose or pure spreadsheet — another piece of evidence that the current tooling is well-shaped for the task.

**Croissant (MLCommons 2024) — metadata format for ML-ready datasets, built on schema.org.** This is the modern industry standard for ML dataset metadata, adopted by HuggingFace, Kaggle, and OpenML. It defines four layers (Metadata, Resources, Structure, ML semantics) and ships with a Python library, validator, and visual editor. Touchstones could export to Croissant format relatively cheaply via a `Corpus.to_croissant()` method (parallel to the existing `to_dataframe()`). Cheaper to support than an HF datasets export because Croissant is just a JSON-LD format, not a runtime dependency.

---

## Part 2: Recommendations

Each recommendation is tagged `leverage / cost`. Citations are dual: source (code project or paper) + Touchstones file.

### High leverage

1. **Add a paragraph in `README.md` framing Touchstones as RSA-style probing, not classifier-style probing.** *(High leverage, cheap.)* The README currently says "diagnostic probe, not benchmark" (`README.md:18`) but doesn't name the methodological lineage. Naming it (with Kriegeskorte 2008 + Picking BERT's Brain as references) gives Touchstones a real literature anchor and clarifies for benchmark-literate readers why the corpus is structured the way it is. *Source: Kriegeskorte, Mur & Bandettini 2008. Target: `README.md` "What this is for" section, around line 18.*

2. **Document the "memorization-is-fine, similarity-is-the-probe" inversion explicitly in `README.md`.** *(High leverage, cheap.)* BIG-bench's `docs/doc.md` makes "not solvable by memorization" criterion #6; Touchstones inverts this on purpose because the probe is cosine structure, not task accuracy. The `README.md:11–18` "What this is for" section should add one paragraph saying so out loud — this is the single biggest place a benchmark-literate reader will misread Touchstones' design intent. *Source: BIG-bench `docs/doc.md` criteria 5–6. Target: `README.md` "What this is for" section.*

3. **Cite Picking BERT's Brain as the empirical anchor for the N=5–10 question.** *(High leverage, cheap.)* `docs/coverage.md:92–94` asserts N=5–10 per critical cell as the Phase 2 densification target without grounding. Picking BERT's Brain is the closest direct precedent — RSA applied to BERT embeddings — and uses n=200 per sample. The honest framing for Touchstones: "the literature does not give a clean minimum-N answer; the closest empirical precedent is 20–40× higher than our floor; this is one of the empirical questions Touchstones-using research could most usefully resolve." Either ground N=5–10 in something concrete (a simulation, this citation), or downgrade the per-cell claims the README advertises. *Source: Chrupała, Higy & Alishahi 2020, "Picking BERT's Brain"; Warstadt et al. 2020 BLiMP design as supporting precedent. Target: `docs/coverage.md` "Target and phases" section, lines 92–94.*

4. **Promote `Entry.known_issues` from "what's wrong with the artifact" to "issues + probe limitations."** *(High leverage, cheap.)* Both lenses converge on this: the HuggingFace dataset card's "Other Known Limitations" section and the Datasheets/Model Cards "Caveats" sections all want this broader framing. Reframe the prompt in `CONTRIBUTING.md` so contributors record both kinds of issue under the same field: artifact defects (e.g., the row-35 Iris errors) AND probe-side caveats (e.g., "this entry is short enough that length-dominated embeddings cluster it spuriously"). No schema change required. *Source: HuggingFace dataset card guide; Mitchell et al. 2019 Model Cards; Gebru et al. 2018/2021 Datasheets "Uses" group. Target: `CONTRIBUTING.md` field reference for `known_issues`; `src/touchstones/schema.py` `known_issues` field docstring.*

5. **Acknowledge the four breadth axes as theory-laden choices, not neutral discoveries.** *(High leverage, cheap.)* Excavating AI's "training data is theory" framing applies to Touchstones' axis choices. `docs/coverage.md:56` already does half the work by explicitly naming the rejected non-axes (register, era, structure, length-band); the other half is naming the *accepted* axes (category, language, script, discipline) as theoretical commitments about what features models are likely sensitive to. A short paragraph in `docs/coverage.md` "Breadth axes" section, framing the choice as a hypothesis rather than a discovery, closes the philosophical blind spot cheaply. *Source: Crawford & Paglen 2019, "Excavating AI." Target: `docs/coverage.md` "Breadth axes" section, lines 43–56.*

### Medium leverage

6. **Write a corpus-level `docs/datasheet.md` mapping the Datasheets for Datasets 7 question groups.** *(Medium leverage, medium cost.)* Most answers exist already, scattered across `README.md`, `CLAUDE.md`, and `docs/coverage.md`. Consolidating them into one place under the standard section headings (Motivation, Composition, Collection, Preprocessing, Uses, Distribution, Maintenance) would (a) surface the "Maintenance" gap concretely, (b) make Touchstones legible to readers from the dataset-card community, and (c) reduce the prose-only changelog problem in `CLAUDE.md`'s status section. Both lenses recommend this. *Source: Gebru et al. 2018/2021 (the original 7 question groups); HuggingFace dataset card practice (the descendant). Target: new file `docs/datasheet.md`; cross-link from `README.md`.*

7. **Add a "parallel-text family" obligation to the per-entry rule, and import the failure-mode vocabulary that makes it legible.** *(Medium leverage, cheap.)* `docs/coverage.md:90` already names the principle ("when two entries differ on *exactly one axis*, the embedding-analysis use case can attribute embedding shifts to that axis with much more confidence") but doesn't enforce it and doesn't tie it to the underlying failure modes. Two changes: (a) add a soft requirement to `CONTRIBUTING.md` that a new entry should *either* fill an empty cell *or* form a one-axis-difference pair with an existing entry (the UDHR Article 1 family is the existing proof of concept); (b) add a short "Confound failure modes" subsection to `docs/coverage.md` naming length, type-frequency, and position confounds, with the vocabulary borrowed from probing-classifier literature even though the methodological apparatus doesn't transfer. *Source: BIG-bench `doc.md` criterion 4 ("Thoroughness"); Hewitt & Liang 2019 and Pimentel et al. 2020 (failure-mode vocabulary). Target: `CONTRIBUTING.md` selection rule + `docs/coverage.md` axis discussion.*

8. **Widen the `creator` field's prompt in `CONTRIBUTING.md` to capture community-production context.** *(Medium leverage, cheap.)* Data Statements' speaker-community framing applies most directly to community-produced texts (UDHR translations, Rainbow Passage, Lorem Ipsum). The 12 UDHR Article 1 translations are a single coordinated production context (the official UN translation effort), not 12 independent ones, and an embedding analysis should attribute clustering to that context before attributing it to "the model treats Slavic languages similarly." No schema change required — just prompt the contributor to capture production context in `creator` or `description` where the artifact is community-produced. *Source: Bender & Friedman 2018, "Data Statements for NLP." Target: `CONTRIBUTING.md` field reference for `creator`.*

9. **Adopt the "n=1 documentation framework" framing from Data Cards.** *(Medium leverage, cheap.)* Pushkarna et al. 2022 explicitly identifies "n=1 examples" as a category of dataset content alongside aggregate Factuals and Origins. Touchstones is in some sense a deliberately-n=1 documentation framework applied to embedding-model probing — and that's a more precise positioning than "diagnostic probe, not benchmark." Adding the n=1 framing to `README.md` or `docs/coverage.md` sharpens the positioning and connects Touchstones to the data-documentation literature. *Source: Pushkarna, Zaldivar & Kjartansson 2022, "Data Cards." Target: `README.md` "What this is for" section or `docs/coverage.md` framing.*

10. **Add a "removal and correction" subsection to `CONTRIBUTING.md`.** *(Medium leverage, cheap.)* Touchstones has done one removal (Pi to 100 Decimal Places) but no documented removal process. Birhane & Prabhu's "remove, replace, open" pattern applies. A short subsection in `CONTRIBUTING.md` describing when an entry should be removed, who proposes it, what review it gets, and how the removal is documented (including a pointer to the corresponding entry in the eventual changelog) closes the gap. *Source: Birhane & Prabhu 2021. Target: `CONTRIBUTING.md` (new subsection).*

11. **Add a structured wishlist.** *(Medium leverage, cheap.)* Promote the prose-level "wanted cells" discussion in `docs/coverage.md` to a structured section (or a small `data/wishlist.json`). Each item: cell tuple `(category, language, script, discipline)` + candidate text + reason. NLP-progress's "Wish List" is the precedent — flat markdown is fine. The current state forces re-derivation of "what's missing" from prose every session; structuring it makes the next-priority surface explicit. *Source: `sebastianruder/NLP-progress` README "Wish list" section. Target: `docs/coverage.md` new subsection or `data/wishlist.json` + reference from CONTRIBUTING.md.*

### Low leverage

12. **Add a `Touchstones Lite` subset.** *(Low leverage, cheap.)* A hand-picked 15–25-entry subset spanning all 4 axes at minimum representativeness. Following BIG-bench Lite's precedent. Useful for: embedding-API cost-sensitive iteration, fast smoke tests, README walkthrough examples. Could be a method on `Corpus` or just a documented list of names. *Source: BIG-bench Lite (`google/BIG-bench` README). Target: `src/touchstones/corpus.py` (new method) or `docs/coverage.md` (documented list).*

13. **Add a `Corpus.to_croissant()` export method.** *(Low leverage, cheap.)* Croissant (MLCommons 2024) is the modern industry standard for ML dataset metadata, adopted by HuggingFace, Kaggle, OpenML. Cheaper to support than an HF datasets export because Croissant is just a JSON-LD format, not a runtime dependency. Following the same lazy-import pattern as `to_dataframe()`. *Source: MLCommons 2024 Croissant spec; arxiv 2403.19546. Target: `src/touchstones/corpus.py`.*

14. **Note Walther et al. 2016's metric finding in `README.md`.** *(Low leverage, cheap.)* The README example uses raw cosine similarity. Walther et al. 2016 (in the cognitive-neuroscience RSA tradition) found that cross-validated Mahalanobis distance (LDC) is more reliable than cosine. The most direct adaptation requires noise estimates from repeated stimulus presentations, which doesn't map cleanly to LM embeddings, but the broader insight — that cosine is one choice among several rather than the obvious right answer — is worth surfacing. A footnote or parenthetical is enough. *Source: Walther et al. 2016, NeuroImage. Target: `README.md` "What this is for" section.*

### Non-recommendations (things the literature suggests but Touchstones should NOT do)

- **Do NOT add `register`, `era`, `structure`, or `length-band` as schema enums.** Some Datasheets-style and Data Statements questionnaires push toward structured demographic/contextual axes. `docs/coverage.md:56` already rules these out for good reason — "they have no clean partition and any attempt to enum them invites endless argument" — and the `description` / `usage` / `year_introduced` fields already capture them implicitly. Don't reopen this.
- **Do NOT migrate `entries.json` to Arrow / Parquet / SQLite / Croissant as the canonical format.** At 1500–2000 entries and ~150 KB, the eager-validation-at-import-time property (`CLAUDE.md:16–30`) is more valuable than any storage-layer benefit. Croissant is good as an *export* target (recommendation #13) but the canonical format should remain Touchstones' own JSON, optimized for human editability.
- **Do NOT add per-entry annotator demographics or speaker-community fields.** The HF dataset card prescription and Data Statements both push toward these, but Touchstones has no annotation pipeline (defensible silence), and the speaker-community case is best handled by widening the `creator` field's prompt rather than adding a separate field. A separate field would create empty cells for famous-author entries where the speaker community is just the named author. Document this as a *deliberate* N/A in the eventual `docs/datasheet.md`.
- **Do NOT add a per-entry "difficulty" or "task-accuracy expected" field.** BIG-bench has these because it's a benchmark; Touchstones explicitly is not. Resist any framing that turns entries into scored tasks — `README.md:18` already commits the project to "diagnostic probe, not benchmark," and the schema should not be made to look benchmark-shaped.
- **Do NOT bring in BLiMP-style minimal pairs as a primary structure.** Minimal pairs are powerful for isolating linguistic phenomena, but they require a generation grammar and a phenomenon list — both of which would push Touchstones away from "registry of pre-existing canonical artifacts" and toward "synthetically constructed probe corpus." That's a different project. The transferable parts of the probing-classifier literature are the failure-mode *names* (recommendation #7), not the methodological apparatus.
- **Do NOT adopt the Hewitt & Liang control-task framework or Pimentel et al.'s information-theoretic reframing.** Both presume a probe (classifier or otherwise). Touchstones uses direct cosine similarity with no probe. The probing-classifier debate is interesting context but is not actionable for Touchstones at the methodological level — only at the failure-mode-vocabulary level.
- **Do NOT treat the Datasheets / Data Statements / Model Cards / Data Cards / Croissant frameworks as obligations.** They are reference frameworks, not standards. The right Touchstones engagement is "borrow what fits, name what doesn't, and stay legible to readers from each tradition." A doc that tried to fully comply with all five would be many times its current size and would lose the cohesion that makes Touchstones legible at all.

---

## Part 3: Verdict

The most important finding is that Touchstones' three risks land very differently:

- **Tooling risk is low.** The current architecture is correctly sized for current and target scale; the practice lens reassures and the literature lens (Model Cards' "no machine-readable schema," Data Cards' hybrid recommendation) reinforces. The larger danger is over-engineering toward a scale band Touchstones isn't going to. The literature does add three useful tooling actions (Croissant export, n=1 framing as positioning, the borrowed Model Cards philosophy), but none of them require architectural change.

- **Bias / arbitrariness risk is moderate and mostly a documentation gap, not a curation gap.** Most of the work is consolidation: a `docs/datasheet.md`, a structured wishlist, a `known_issues` reframe, a widened `creator` prompt, a removal/correction subsection, the theory-laden-axes acknowledgment. The corpus-level bias documentation in `docs/coverage.md` is already stronger than what most NLP datasets actually ship — useful calibration from the practice side, where even FLORES and MASSIVE leave the bias sections blank.

- **Utility risk is the largest, and the largest single source of doubt is the unexamined Phase 2 N=5–10 floor.** Both lenses converge: the practice lens via BLiMP's N=1000 per paradigm, the literature lens via Picking BERT's Brain's n=200 per sample. The practice precedent suggests "more is better"; the literature precedent gives a 20–40× empirical anchor. Either ground the floor in something or narrow the per-cell claims the README advertises. The secondary utility concern is that Touchstones is methodologically isolated within mainstream NLP — its real precedent is RSA, not benchmark literature, and naming that lineage is the cheapest single thing the maintainer can do to make the project legible to the right readers.

**The single biggest contribution of this review** — the one finding neither lens could have produced alone — **is the empirical anchor for the N=5–10 question.** The practice lens flagged the gap; the literature lens supplied the number. Picking BERT's Brain at n=200 per sample is a concrete external precedent that is 20–40× higher than Touchstones' Phase 2 floor. That number changes the conversation about Phase 2 from "asserted, not derived" to "asserted at a level the closest empirical precedent suggests is dramatically too low." That's the kind of finding a two-lens review is for.

**The most concentrated single win for the maintainer's effort:** recommendation #3 (cite Picking BERT's Brain as the N anchor) addresses the utility risk directly, takes about a paragraph of writing, and is the only recommendation that touches the load-bearing methodological claim of the whole project.
