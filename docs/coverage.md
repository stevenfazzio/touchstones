# Coverage map

This document is the **coverage-planning** companion to `CONTRIBUTING.md`. The selection rule for individual entries lives there; this document tracks which fields the corpus has reached, which it has not, and the conceptual frame we use to decide which fields are even in scope and what shape an entry takes within them.

## The Schelling-point framing

A good standard example text is one practitioners reach for **because everyone else also reaches for it**. The text does not have to be the best in its class, or even particularly distinguished — what makes it canonical is that the choice has been settled, so the field can stop arguing about which example to use and get on with the work.

Texts become Schelling points for some mix of three reasons:

1. **Spanning coverage.** The text exhibits a useful set of features that lets it stand in for a whole class — the Harvard Sentences cover the phoneme space, "The quick brown fox" is short and includes every English letter, RFC 4648's Base64 vectors hit each padding case.
2. **Historical significance.** Being first (or famous-for-being-first) gives a text gravitational pull. K&R's "Hello, world!", Sanger's φX174 sequence, BNF for ALGOL 60, "Mary had a little lamb" on Edison's phonograph.
3. **Coordination against gaming.** When everyone is required to test against the same input, no one can cherry-pick their own. NIST publishes cryptographic test vectors precisely so implementers cannot manufacture flattering examples; OEIS exists so number theorists cannot quietly redefine what "the Fibonacci sequence" means.

Most established Schelling points draw on more than one of these. None of them require the text to be intrinsically interesting, and several of the strongest examples (Lorem Ipsum, Quick Brown Fox) are deliberately *uninteresting* — that is part of why they stuck.

This framing has two consequences for what belongs in the corpus:

- **Famous ≠ canonical.** "Call me Ishmael" is famous; it is not a Schelling point for anything. Famous error messages, famous speech excerpts, and famous literary openings all fail on the same grounds: practitioners do not reach for them as stand-ins for a class of texts.
- **Some fields will be overrepresented, and that is correct.** Linguistics and NLP coordinate on shared example texts as a core part of their methodology, so they will produce many more entries than, say, accounting or surveying. The shape of the corpus reflects the shape of the territory.

## Documents, not collections

Each entry's `text` field must contain exactly one document. When a focal artifact is itself a collection — a TREC topic file, the FIPS 180-4 test vector tables, an OEIS sequence, a parallel-text Bible, the full 720 Harvard Sentences — the entry is *one focal individual exemplar from* that collection, not the collection itself. The collection lives in the entry's `description`, `source`, and `usage` fields, where it provides context. It does not live in the `text` field, where it would dilute the artifact.

**The test:** if the answer to "what is in this `text` field?" is *"an assortment of N independent items"* or *"a sample from a collection of N things,"* you have drifted from a corpus of documents into a corpus of corpuses. The `text` field should hold a single bounded document that stands on its own.

The existing corpus already follows this discipline:

- **FIPS 180-4 SHA-256 abc test vector** is one vector from a published table of many. The entry isn't "FIPS 180-4 test vectors"; it's the specific "abc" vector, with the larger table named in the description.
- **The Harvard Sentences** is List 1 (10 sentences), not the full 72-list, 720-sentence IEEE publication. The full collection is described in metadata; the entry's text is the canonical first list, which is itself the standard testing unit speech researchers reach for.
- **Pi to 100 Decimal Places** is a defined finite slice of an infinite sequence. The entry isn't "the digits of π"; it's a bounded, citable artifact with an exact length.

**The corpus may contain many atomic exemplars from a single collection.** This is a sharpening of the rule, not an exception to it. The unit is one bounded document per entry, but nothing prevents the corpus from sampling the same collection densely — multiple SHA test vectors, multiple TREC topics, multiple FASTA reference sequences, multiple Harvard Sentence lists, the Pater Noster in several languages. Each is its own atomic entry, linked via `related`. The corpus-of-corpuses trap is bundling N items into one entry's `text`; the cure is N separate entries, not "one entry per collection." This is the natural scaling pattern at corpus sizes past a few hundred (see the **anchor-and-neighbors** discussion under "Breadth axes" below).

This rule is the structural complement to the Schelling-point framing. The framing decides which fields are in scope; this rule decides what shape an entry takes within an in-scope field.

## Breadth axes

The corpus is structured around four orthogonal axes that together define the *cells* of the breadth space. Every entry has explicit values on all four:

| Axis | Schema field | Role |
|---|---|---|
| Type | `category` | Structural kind of text — `natural_language`, `code`, `notation`, `sequence`, `protocol`. Closed enum; the most stable axis. |
| Language | `language` | Primary symbol system — natural languages (`english`, `latin`, `japanese`), programming languages (`c`, `python`), notation systems (`bnf`), protocols (`http`), or `none` for non-linguistic data. Open vocabulary. |
| Script | `script` | Writing script the bytes are rendered in (`latin`, `cyrillic`, `cjk_han`, `devanagari`, …). Open vocabulary. |
| Discipline | `discipline` / `disciplines` | Field(s) that reach for this artifact (`speech pathology`, `cryptography`, `linguistics`, …). Open vocabulary. |

A *cell* is one `(category, language, script, discipline)` 4-tuple. Most cells are empty and most empty cells will stay empty (no field uses Korean cryptographic test vectors). The curator's job in **Phase 1 (breadth)** is to identify which empty cells are *interesting* — cells where adding the canonical exemplar opens new analytical territory — and fill them at N=1.

Deliberately *not* in the schema: register, era, structure, length-band. These are real dimensions but they have no clean partition and any attempt to enum them invites endless argument. They stay implicit, captured by the curator's eye and by the per-entry metadata fields (`year_introduced`, `description`, `usage`).

### Diagnostic snapshot

#### Initial baseline (v0.1, 19 entries)

Filling in `language` and `script` for the original 19 seed entries surfaced the bias the breadth framing was designed to make visible:

- **Script:** 19 / 19 are `latin`. The corpus has zero non-Latin entries.
- **Language:** 11 / 19 are `english`. The non-English breakdown is 1 `latin` (Lorem Ipsum), 1 `c`, 1 `bnf`, 1 `http`, and 4 `none` (genome, hashes, π digits). Zero entries in any other natural language.
- **Category:** 12 / 19 are `natural_language`. `code`, `notation`, and `protocol` have exactly one entry each — *enough to bias an embedding analysis, not enough to support a claim.*

These three numbers were the concrete shape of "unconstrained curation reaching for what feels interesting" and the agenda for the first two batches.

#### Current state (43 entries)

After three breadth-filling batches — the **first non-Latin batch** (10 entries), the **underpopulated-categories batch** (7 entries: K&R wc, SICP factorial, Thompson quine, Dragon-book grammar, Wirth syntax notation, RFC 5321 SMTP, RFC 1035 DNS), and the **UDHR parallel-text batch** (6 UDHR Article 1 translations — French, Spanish, German, Italian, Portuguese, Polish — plus the Triouleyre French pangram as a small follow-on, 7 entries total) — the snapshot is:

- **Script:** 33 / 43 are `latin`, plus 10 entries across 9 non-Latin scripts (`arabic`, `cyrillic`, `cjk_han`, `devanagari`, `hangul`, `hebrew`, `hiragana`, `mixed`, and `greek` at N=2). The script monoculture is broken; further non-Latin additions are still high-leverage but no longer urgent.
- **Language:** 11 / 43 are still `english` — the absolute English count has not grown, but its share has dropped from 11/19 → 11/36 → 11/43 as the corpus has filled out. 15 non-English natural languages are now represented: 9 in non-Latin scripts (`arabic`, `russian`, `chinese`, `hindi`, `korean`, `japanese` at N=2, `ancient_greek`, `koine_greek`, `hebrew`) and 6 new in Latin script (`french` at N=2, plus `spanish`, `german`, `italian`, `portuguese`, `polish` each at N=1). Plus 4 `none` (raw bytes), 1 `latin` (Lorem Ipsum), and 9 programming/notation/protocol languages (`c` at N=3, then `bnf`, `cfg`, `dns`, `wsn`, `http`, `scheme`, `smtp` each at N=1).
- **Category:** 29 / 43 are `natural_language`. `code` is 4, `sequence` 4, `notation` 3, `protocol` 3 — each non-NL category remains at N≥3.

The next first-wave priority is **continuing to break the English monoculture within Latin script** (priority #3 below). The UDHR batch made meaningful progress on the *share*, but the English/Latin-script cluster is still the corpus's largest single bias and many obvious Latin-script languages remain absent (Dutch, Catalan, Czech, Hungarian, Vietnamese, Indonesian, Swahili, Turkish, …).

### Anchor-and-neighbors curation

Past ~200 entries, the natural way to grow is **anchor-and-neighbors**: for each existing anchor entry, identify 3–10 texts that occupy a similar position in the breadth-space and have their own weaker Schelling-point status. Anchor + neighbors is how the "documents, not collections" rule scales — see the clarification above. Examples:

- φX174 genome → λ phage, human mtDNA reference (CRS), GFP, hen lysozyme, ubiquitin, bovine insulin
- SHA-256 "abc" → other FIPS 180-4 SHA test vectors, MD5("a"), SHA-1("abc"), HMAC-SHA-1 RFC 2202 vectors
- Harvard Sentences List 1 → Lists 2–10
- Lorem Ipsum → variant lorems (Bacon Ipsum, Hipster Ipsum, Cupcake Ipsum)
- UDHR Article 1 (English) → UDHR Article 1 in 11 other languages so far ✓ (Arabic, Russian, Chinese, Hindi, Korean, French, Spanish, German, Italian, Portuguese, Polish); still to add: Latin Vulgate, Sanskrit, Japanese, Swahili, Tagalog, Vietnamese, … (parallel-text family)

Parallel-text families are especially valuable: when two entries differ on *exactly one axis*, the embedding-analysis use case can attribute embedding shifts to that axis with much more confidence.

### Target and phases

The corpus targets ~1500–2000 entries reached in three phases: **Phase 1 (breadth)** fills ~80% of identified cells at N=1 (~200–400 entries); **Phase 2 (selective densification)** brings the 20–30 most analysis-critical cells to N=5–10 each (+200–500 entries); **Phase 3 (family expansion)** uses anchor-and-neighbors to reach the final size. 10k+ is explicitly *not* the near-term target — past ~2k, per-entry depth has to drop and the project becomes a different product.

## Status legend

| Tag | Meaning |
|---|---|
| `covered` | At least one strong entry exists; further additions face diminishing returns |
| `thin` | One or two entries; the field has known room to grow |
| `untouched` | No entry yet; the field has identified Schelling-point candidates |
| `first wave` | Currently prioritized for the next round of research |

The map names *example artifacts* under each row to make the field's scope concrete; these are not commitments. Per-domain research will refine the actual list before any entries are written. Where an example artifact is collection-shaped, the implied entry is a single focal exemplar from it, not the collection itself.

## Domain map

### Computing & standards

| Field | Status | Example artifacts |
|---|---|---|
| First-program / language intro | `thin` | K&R Hello World ✓, K&R `wc` ✓; *Smalltalk `Transcript show:`, classic Fortran `WRITE`* |
| Programming exercises / pedagogy | `thin` | 99 Bottles ✓; *FizzBuzz reference solution, Ackermann small input* |
| Self-reproducing programs / quines | `thin` | Thompson quine (Reflections on Trusting Trust) ✓; *Hofstadter quine variants, polyglot quines* |
| Algorithm reference implementations | `thin` | SICP factorial ✓; *Dijkstra's binary-search note (EWD316), Knuth literate-program snippets* |
| Cryptographic test vectors | `first wave` | SHA-256("abc") ✓, Base64 RFC 4648 ✓; *HMAC-SHA-1 RFC 2202 single vector, AES FIPS-197 worked example, MD5("")* |
| Encoding round-trip standards | `thin` | Base64 RFC 4648 ✓; *RFC 8259 §13 JSON example, RFC 3986 URI example, RFC 3492 punycode single example* |
| Network protocol exemplars | `thin` | HTTP/1.1 GET ✓, RFC 5321 SMTP transaction (App. D.1) ✓, RFC 1035 DNS message compression (§4.1.4) ✓; *TLS 1.3 ClientHello RFC 8448, IMAP4rev1 RFC 3501 §6.1 example* |
| Grammar / language-theory examples | `thin` | BNF for ALGOL 60 ✓, Dragon-book expression grammar ✓, Wirth Syntax Notation self-definition ✓; *ABNF self-definition (RFC 5234), ISO/IEC 14977 EBNF self-definition* |
| Regular-expression canon | `untouched` | *RFC 5322 email ABNF, RFC 3986 URI ABNF* |
| Floating-point edge cases | `untouched` | *one IEEE 754 binary64 boundary value, one Kahan-summation pathological input* |
| Tokenizer / Unicode test strings | `first wave` | *Markus Kuhn UTF-8 stress test, "I can eat glass" in one canonical language* |
| Information-retrieval benchmark queries | `untouched` | *one TREC ad-hoc topic statement (e.g., Topic 401), one Cranfield query* |

### Linguistics

| Field | Status | Example artifacts |
|---|---|---|
| Read-aloud / phonetic passages | `covered` | Rainbow Passage ✓, Harvard Sentences ✓, North Wind & Sun ✓ |
| IPA / language documentation | `covered` | North Wind & Sun ✓ |
| Garden-path / parsing test sentences | `first wave` | *"The horse raced past the barn fell", "Buffalo buffalo Buffalo buffalo…", "Time flies like an arrow"* |
| Linguistic well-formedness probes | `first wave` | Jabberwocky stanza 1 ✓; *"colorless green ideas sleep furiously"* |
| Vocabulary acquisition exemplars | `untouched` | *Dolch sight-word list (Edward Dolch, 1936)* |
| Minimal-syntax exemplars | `untouched` | *"the cat sat on the mat" as the canonical minimal English declarative* |

### NLP / corpus benchmarks

| Field | Status | Example artifacts |
|---|---|---|
| Treebank exemplar sentences | `untouched` | *Penn Treebank §00 sentence 1: "Pierre Vinken, 61 years old…"* |
| Reference-corpus openings | `untouched` | *first sentence of Brown Corpus A01* |
| Parallel-corpus exemplars | `thin` | UDHR Art. 1 in 12 languages ✓ (English, Arabic, Russian, Chinese, Hindi, Korean, French, Spanish, German, Italian, Portuguese, Polish); *Pater Noster (Latin Vulgate), the historical predecessor of UDHR Art. 1 in cross-language linguistic comparison* |
| Word-vector probes | `untouched` | *"king − man + woman = queen"* |
| Conversational AI exemplars | `untouched` | *ELIZA opening "How do you do. Please tell me your problem."* |

### Typography & design

| Field | Status | Example artifacts |
|---|---|---|
| Pangrams (English) | `covered` | Quick Brown Fox ✓, Now Is The Time ✓ |
| Pangrams (non-English) | `thin` | French "Portez ce vieux whisky au juge blond qui fume" (Triouleyre, 1921, alexandrine, hétéroconsonantique) ✓; *Russian, Japanese; German has several circulating pangrams (Falsches Üben…, Zwölf Boxkämpfer…) but sourcing-validation found none with clear Schelling-point canonicity* |
| Type-specimen phrases | `untouched` | *"Hamburgevons", "Handgloves"* |
| Placeholder / filler text | `covered` | Lorem Ipsum ✓ |

### Poetry

The criterion for inclusion: the poem must be used as a focal exemplar of a *form, period, or movement*, not merely as a famous individual work. This distinguishes Bashō's frog haiku (the canonical haiku) from "Call me Ishmael" (a famous opening that does not stand in for a class).

| Field | Status | Example artifacts |
|---|---|---|
| Canonical haiku | `untouched` | *Bashō's frog haiku ("old pond / a frog jumps in / sound of water"), one canonical translation* |
| Canonical Shakespearean sonnet | `untouched` | *Shakespeare Sonnet 18 ("Shall I compare thee to a summer's day?")* |
| Old English alliterative verse | `untouched` | *opening of Beowulf ("Hwæt! We Gardena in geardagum…")* |
| Middle English exemplar | `untouched` | *opening of Chaucer's Canterbury Tales ("Whan that Aprille with his shoures soote…")* |
| Modernist micro-poem | `untouched` | *William Carlos Williams, "This Is Just To Say"* |
| Imagist exemplar | `untouched` | *Pound, "In a Station of the Metro"* |
| Epic invocation | `untouched` | *opening of the Iliad ("Sing, goddess, of the wrath of Achilles…"), one canonical English translation* |

### Civic, legal, historical

| Field | Status | Example artifacts |
|---|---|---|
| US foundational documents | `thin` | Preamble ✓, Gettysburg ✓; *Declaration of Independence opening, First Amendment* |
| International human-rights instruments | `thin` | UDHR Art. 1 ✓; *Geneva Conventions Common Art. 3, ICCPR Art. 1* |
| Other national constitutions | `untouched` | *French Déclaration Art. 1, Grundgesetz Art. 1, Magna Carta clause 39* |
| Oaths and pledges | `untouched` | *US Presidential Oath, classical Hippocratic Oath* |

### Scientific & mathematical

| Field | Status | Example artifacts |
|---|---|---|
| Genomic reference sequences | `thin` | φX174 ✓; *λ phage, the Cambridge Reference Sequence (human mtDNA)* |
| Protein sequences (FASTA) | `untouched` | *bovine insulin (Sanger), hen lysozyme, ubiquitin, GFP — one entry per protein* |
| Chemical structure notation | `untouched` | *SMILES for caffeine, aspirin, glucose; InChI for water — one entry per molecule* |
| Mathematical constants | `thin` | π to 100 ✓; *e, √2, φ, γ to comparable precision — one entry per constant* |
| Integer sequences | `untouched` | *first N terms of OEIS A000040 (primes), A000045 (Fibonacci), A005150 (look-and-say) — one entry per sequence, with N fixed* |
| Famous formulas in TeX | `untouched` | *Euler's identity, Schrödinger equation — one entry per formula* |
| Physical constants (CODATA display) | `untouched` | *c, h, α, G — one entry per constant, verbatim from NIST* |

### Cultural & historical text landmarks

| Field | Status | Example artifacts |
|---|---|---|
| Children's literature / nursery rhymes | `thin` | Mary Had a Little Lamb ✓; *"See Spot run" / Dick and Jane primer passage, "Twinkle Twinkle"* |
| Nonsense verse | `thin` | Jabberwocky stanza 1 ✓ |
| Audio history landmarks (text content) | `covered` | Mary Had a Little Lamb ✓ (Edison phonograph) |

### Reserved documentation examples

A small but distinctive cluster: identifier strings that standards bodies deliberately published as examples *so they could become Schelling points*. Same intentional construction as NIST cryptographic test vectors. Each identifier is an atomic entry — these are never bundled.

| Field | Status | Example artifacts |
|---|---|---|
| Reserved example domains | `untouched` | *`example.com` (RFC 2606), `example.org`, `example.net`* |
| Loopback / reserved IPs | `untouched` | *`127.0.0.1`, `192.0.2.0/24` (RFC 5737 TEST-NET-1)* |
| DOI documentation example | `untouched` | *`10.1000/182` — the canonical example DOI from the DOI handbook* |
| ORCID test record | `untouched` | *`0000-0002-1825-0097` — Josiah Carberry, the canonical fictional ORCID* |

### Games

| Field | Status | Example artifacts |
|---|---|---|
| Chess in algebraic / PGN | `untouched` | *Ruy Lopez opening moves, Fischer "Game of the Century" PGN — one entry per game* |

## First wave

Under the breadth framing and the diagnostic snapshot above, the immediate priorities are not the most interesting cells but the most *imbalanced* axes. Three priorities, in rough order of analytical leverage:

1. **Break the script monoculture. ✓ Done (first non-Latin batch).** Originally all 19 entries were `script=latin`; the first non-Latin batch added 10 entries opening cells in Arabic, Cyrillic, CJK han, Devanagari, Hangul, Hebrew, hiragana, mixed (Japanese), and a second Greek. Further non-Latin additions are still high-leverage but no longer urgent.

2. **Backfill the underpopulated categories. ✓ Done (underpopulated-categories batch).** Originally `code`, `notation`, and `protocol` each had exactly one entry. The 7-entry batch added K&R `wc`, SICP factorial, and the Thompson quine (code); the Dragon-book expression grammar and Wirth syntax notation self-definition (notation); and the RFC 5321 SMTP transaction scenario plus RFC 1035 DNS message-compression example (protocol). Each non-NL category is now at N≥3, enough to support meaningful category-wise slicing.

3. **Break the language monoculture within Latin script. ⏳ In progress (UDHR parallel-text batch + Triouleyre French pangram).** 11 / 43 entries are still `english`; the absolute English count is unchanged from the v0.1 baseline but English's share has dropped from 11/19 → 11/36 → 11/43 thanks to the UDHR Article 1 batch (French, Spanish, German, Italian, Portuguese, Polish — 6 new Latin-script natural-language cells) and the Triouleyre French pangram follow-on (1921, the canonical French pangram, structurally an alexandrine; bumps `french` to N=2). Remaining work continues along the same axis: more parallel-text family members for texts already in the corpus — UDHR Article 1 in Latin Vulgate, Catalan, Dutch, Sanskrit, Japanese, Swahili, Tagalog, Vietnamese; the Pater Noster in Latin Vulgate; "I can eat glass" in several Latin-script languages. Parallel-text families let analysts hold content constant and isolate the language axis, which is the cleanest factorial structure available for embedding-sensitivity work.

Once priority #3 is in good shape (call it ~30–50 more entries), the previously-named priority clusters — NLP and linguistic Schelling points (e.g., "colorless green ideas sleep furiously", garden-path sentences, the Penn Treebank §00 sentence), cryptographic test vector families, and tokenizer / Unicode coordination strings (Markus Kuhn's UTF-8 stress test) — become the natural Phase 2 targets, with the breadth-axis structure now in place to keep them from re-creating the original bias.

## What does not belong

These categories are explicitly out of scope, recorded here so they do not get re-proposed:

- **Famous-but-not-focal strings.** Recognizable error messages, literary openings, and speech excerpts. They are famous, but practitioners do not use them as stand-ins for a class of texts. (The poetry cluster admits famous poems only when they function as focal exemplars of a *form*, not merely as famous individual works.)
- **File-format magic numbers and headers.** A literal byte field is canonical *as itself*, not as an exemplar of a class.
- **Music in text notation.** Lilypond and ABC sources for nursery tunes are reproducible but no community treats any specific transcription as a Schelling point.
- **Audio test materials, image test materials, and reference datasets accessed through code.** The Utah Teapot, Lena, the Iris dataset, MNIST, SQAM clips: canonical in their fields, but not as text strings anyone bundles. Already covered in `CONTRIBUTING.md`'s "examples that fail" list.
- **Statistical reference tables, A440, currency boilerplate, Rubik's-cube notation.** No focal text exists, even though the surrounding domain is well-defined.
- **Cataloging formats without canonical instances.** MARC 21, Dublin Core, MODS, BibTeX, RDA all have canonical *formats*, but no canonical *instance* records that practitioners reach for by exact bytes. Same gap as file-format magic numbers — the format is canonical, individual instances are interchangeable.
- **Journalism, advertising, marketing.** Famous headlines, leads, slogans, and ad campaigns are recognizable but not focal-as-stand-ins. Slogans are also typically trademarked. The closest borderline candidates (Hemingway six-word story, Conroy's "Two Young Men" direct-mail letter) belong to literature or copywriting craft history rather than to the corpus.
- **Bundled collections.** Per "Documents, not collections" above: TREC topic files, OEIS sequence pointers, parallel-text Bibles, and similar collection-shaped artifacts are out as single entries. Their focal individual exemplars are in.
