# Coverage map

This document is the **coverage-planning** companion to `CONTRIBUTING.md`. The selection rule for individual entries lives there; this document tracks which fields the corpus has reached, which it has not, and the conceptual frame we use to decide which fields are even in scope and what shape an entry takes within them.

## The Schelling-point framing

A good standard example text is one practitioners reach for **because everyone else also reaches for it**. The text does not have to be the best in its class, or even particularly distinguished — what makes it canonical is that the choice has been settled, so the field can stop arguing about which example to use and get on with the work.

Texts become Schelling points for some mix of three reasons:

1. **Spanning coverage.** The text exhibits a useful set of features that lets it stand in for a whole class — the Harvard Sentences cover the phoneme space, "The quick brown fox" is short and includes every English letter, RFC 4648's Base64 vectors hit each padding case.
2. **Historical significance.** Being first (or famous-for-being-first) gives a text gravitational pull. K&R's "Hello, world!", Sanger's φX174 sequence, BNF for ALGOL 60, "Mary had a little lamb" on Edison's phonograph.
3. **Coordination against gaming.** When everyone is required to test against the same input, no one can cherry-pick their own. NIST publishes cryptographic test vectors precisely so implementers cannot manufacture flattering examples; OEIS exists so number theorists cannot quietly redefine what "the Fibonacci sequence" means.

Most established Schelling points draw on more than one of these. None of them require the text to be intrinsically interesting, and several of the strongest examples (Lorem Ipsum, Quick Brown Fox) are deliberately *uninteresting* — that is part of why they stuck.

A useful sibling pattern, sitting alongside the three above, is **deficit-defined canonicity**: a text is canonical because of what it *lacks* or what it *gets wrong*. The flaw is the use case, so substitution is impossible — any other text would have a different flaw, or no flaw, or a less pedagogically clean flaw. Chomsky's "Colorless green ideas sleep furiously" is the canonical syntactically-well-formed-semantically-anomalous English sentence not because Chomsky was first to construct one, but because every linguistics textbook now teaches that exact string. Bever's "The horse raced past the barn fell" is the canonical garden-path sentence on the same grounds. Apple's nine-line `goto fail` excerpt is the canonical example of a single duplicated line breaking TLS authentication. Heartbleed's `tls1_process_heartbeat` excerpt is the canonical example of a missing length check. These texts coordinate practitioners through the same gaming-resistance logic as NIST cryptographic test vectors, except that the "test" is "demonstrate this specific failure" rather than "verify this specific output." Practically, this lens cuts across all four breadth axes — deficit-defined entries can be `natural_language`, `code`, `notation`, etc. — and tends to identify unusually clean Schelling points, because the flaw forces uniqueness. It is not a new axis in the schema sense; it is a *recognition pattern* for finding strong candidates.

This framing has two consequences for what belongs in the corpus:

- **Famous ≠ canonical.** "Call me Ishmael" is famous; it is not a Schelling point for anything. Famous error messages, famous speech excerpts, and famous literary openings all fail on the same grounds: practitioners do not reach for them as stand-ins for a class of texts.
- **Some fields will be overrepresented, and that is correct.** Linguistics and NLP coordinate on shared example texts as a core part of their methodology, so they will produce many more entries than, say, accounting or surveying. The shape of the corpus reflects the shape of the territory.

## Documents, not collections

Each entry's `text` field must contain exactly one document. When a focal artifact is itself a collection — a TREC topic file, the FIPS 180-4 test vector tables, an OEIS sequence, a parallel-text Bible, the full 720 Harvard Sentences — the entry is *one focal individual exemplar from* that collection, not the collection itself. The collection lives in the entry's `description`, `source`, and `usage` fields, where it provides context. It does not live in the `text` field, where it would dilute the artifact.

**The test:** if the answer to "what is in this `text` field?" is *"an assortment of N independent items"* or *"a sample from a collection of N things,"* you have drifted from a corpus of documents into a corpus of corpuses. The `text` field should hold a single bounded document that stands on its own.

**A sharpening on what counts as a "collection":** *plurality* in the `text` field is not the failure mode — *bundling independently-canonical items* is. Constituents that are non-canonical in isolation (the residues of a protein, the rows of a designed experimental dataset, the statements of a function body, the discrete propositions of a numbered axiom set) are part of a single bounded artifact, not a collection of items. The right test is: *could each constituent meaningfully stand alone with its own Schelling-point status?* If yes, the focal artifact is the constituent and the surrounding container is metadata (TREC topic 401, the FIPS 180-4 SHA-256 "abc" vector, the first 20 terms of OEIS A000045, UDHR Article 1 in one specific language). If no, the focal artifact is the whole bounded thing (Sanger's bovine insulin, the UCI Iris CSV, the body of Heartbleed's `tls1_process_heartbeat`, Newton's three Axiomata as a single passage). The first kind of entry has N siblings under anchor-and-neighbours growth (one per topic, one per vector, one per sequence, one per language); the second kind is one entry, period, because there is no smaller canonical unit to peel off. The two readings sometimes meet in the middle — the Harvard Sentences entry is List 1, which is one focal exemplar from the 72-list IEEE collection (first reading) *and* a fixed group of 10 sentences none of which is canonical alone (second reading); both routes arrive at "one entry containing the whole list."

The existing corpus already follows this discipline:

- **FIPS 180-4 SHA-256 abc test vector** is one vector from a published table of many. The entry isn't "FIPS 180-4 test vectors"; it's the specific "abc" vector, with the larger table named in the description. (First reading: focal exemplar from a collection of independently-canonical vectors.)
- **The Harvard Sentences** is List 1 (10 sentences), not the full 72-list, 720-sentence IEEE publication. The full collection is described in metadata; the entry's text is the canonical first list, which is itself the standard testing unit speech researchers reach for. (Both readings: focal list from the 72-list collection *and* fixed 10-sentence group whose constituents have no isolated Schelling-point status.)
- **Sanger's Bovine Insulin Sequence** is one specific 51-residue protein from the proteome, in modern one-letter code: A-chain (21 aa) and B-chain (30 aa). The entry isn't "early protein sequences" or "Sanger's lab notebooks"; it's the bounded artifact for which Sanger received the 1958 Nobel. (Second reading: 51 residues, none independently canonical, together one molecule.)
- **UCI Iris Dataset (`iris.data`)** is 150 rows × 5 fields, but no individual row of `iris.data` has Schelling-point status the way an individual TREC topic does — the dataset's canonicity lives at the dataset level (the 50/50/50 experimental design, the linear separability of *I. setosa*, the row-35/38 errors that fingerprint the file, the bag-of-bytes identity that scikit-learn / R / MATLAB / Weka all reload verbatim). Per the sharpening above, constituents that are non-canonical in isolation are part of a single bounded artifact, not a collection. (Second reading: 150 rows, none independently canonical, together one designed experimental dataset.)

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

#### Current state (57 entries)

After six breadth-filling batches plus a curatorial correction-and-replacement pair — the **first non-Latin batch** (10 entries), the **underpopulated-categories batch** (7 entries: K&R wc, SICP factorial, Thompson quine, Dragon-book grammar, Wirth syntax notation, RFC 5321 SMTP, RFC 1035 DNS), the **first UDHR parallel-text batch** (6 UDHR Article 1 translations — French, Spanish, German, Italian, Portuguese, Polish — plus the Triouleyre French pangram as a small follow-on, 7 entries total), the **second UDHR parallel-text batch** (6 more UDHR Article 1 translations — Latin, Dutch, Catalan, Swahili, Indonesian, Vietnamese), the **natural-sciences batch** (3 entries: Newton's *Axiomata sive Leges Motus* from the Principia, Sanger's bovine insulin sequence, and the canonical SMILES for caffeine — a deliberate course-correction toward the corpus's then-empty physics, biochemistry, and cheminformatics cells), the **deficit-defined-canonicity batch** (5 entries: Apple's `goto fail` excerpt from sslKeyExchange.c, the OpenSSL Heartbleed `tls1_process_heartbeat` excerpt, Duff's Device, Chomsky's "Colorless green ideas sleep furiously", and Bever's "The horse raced past the barn fell" — texts that are canonical *because* of a flaw they have or a property they lack), a **curatorial correction** removing the Pi to 100 Decimal Places entry (which failed the per-entry selection rule on close inspection: the 100-digit cutoff is conventional rather than canonical, and the truncated-vs-rounded ambiguity means there is no single canonical bag of bytes — the same failure mode as Lena, the Utah Teapot, and the Mandelbrot set), and the **UCI Iris CSV addition** (1 entry: `iris.data`, 150 rows, 4549 stored bytes) which opened a new `dataset` category and qualified under the deficit-defined-canonicity lens because the UCI file's two well-known row-35/row-38 data-entry errors are the fingerprint that disambiguates "the Iris dataset" the concept from `iris.data` the artifact — the snapshot is:

- **Script:** 47 / 57 are `latin` (Iris CSV restored the count after the Pi removal; both are `language=none`/`script=latin`), plus 10 entries across 9 non-Latin scripts (`arabic`, `cyrillic`, `cjk_han`, `devanagari`, `hangul`, `hebrew`, `hiragana`, `mixed`, and `greek` at N=2). The script monoculture is broken; further non-Latin additions are still high-leverage but no longer urgent.
- **Language:** 13 / 57 are `english` — the absolute English count rose for the first time since v0.1, by exactly 2, when the deficit-defined-canonicity batch added Chomsky's "Colorless green ideas sleep furiously" and Bever's "The horse raced past the barn fell". Both are canonical *because of a flaw* (semantic anomaly and garden-path misparse respectively) and have no equivalent canonical form in any other language; the increase is therefore lens-justified rather than a relaxation of the English-monoculture priority. English's share has still continued to drop overall: 11/19 → 11/36 → 11/43 → 11/49 → 11/52 → 13/57 → 13/56 → 13/57 (the last two ticks are the Pi removal and the Iris addition, both `language=none`). 20 non-English natural languages are now represented: 9 in non-Latin scripts (`arabic`, `russian`, `chinese`, `hindi`, `korean`, `japanese` at N=2, `ancient_greek`, `koine_greek`, `hebrew`) and 11 in Latin script (`french` at N=2, plus `spanish`, `german`, `italian`, `portuguese`, `polish`, `dutch`, `catalan`, `swahili`, `indonesian`, `vietnamese` each at N=1). Plus 5 `none` (raw bytes — φX174 DNA, Sanger's bovine insulin, RFC 4648 Base64 vectors, FIPS 180-4 SHA-256 "abc", and the UCI Iris CSV), 3 `latin` (Lorem Ipsum, UDHR Article 1 in Latin, and Newton's *Axiomata sive Leges Motus*), and 10 programming/notation/protocol languages (`c` now at N=6 after the goto-fail / Heartbleed / Duff additions, then `bnf`, `cfg`, `dns`, `wsn`, `http`, `scheme`, `smiles`, `smtp` each at N=1).
- **Category:** 38 / 57 are `natural_language`. `code` is 7 (up from 4), `sequence` 4 (down 1 with the Pi removal), `notation` 4, `protocol` 3, and **`dataset` 1** (the UCI Iris CSV — a new sixth category opened to accommodate rectangular tabular reference data, a structural shape that had been entirely absent). The deficit-defined batch nearly doubled the `code` category in a single addition — useful for category-wise slicing now that `code` has the largest non-NL representation. Adding `dataset` brought the closed `Category` Literal to 6 values for the first time since the schema was written.

The second UDHR batch was deliberately chosen to break out of the European-only Latin-script cluster: Swahili is the corpus's first Bantu / Niger-Congo entry and first sub-Saharan-African language entry; Indonesian is the first Austronesian entry; Vietnamese is the first Austroasiatic entry. Latin pairs directly with Lorem Ipsum on the language axis (real-Latin vs. scrambled-Cicero placeholder), giving the corpus its first within-language register-contrast pair. The natural-sciences batch was a deliberate course-correction prompted by noticing that 12/49 entries had become UDHR Article 1 translations — a UDHR-Article-1 monoculture forming inside the now-broken script monoculture. It opens the corpus's first physics, biochemistry, and cheminformatics cells, adds a non-UDHR Latin-language sample (Newton's Latin) and a non-DNA biological sequence (Sanger's bovine insulin) along the way, and surfaces the broader natural-sciences cluster as the next visible breadth gap (chemistry beyond SMILES, astronomy, earth science, additional biology, and physics primary sources beyond Newton remain almost entirely uncovered). The deficit-defined-canonicity batch was a *conceptual* breadth move rather than an axis-filling one: it introduced the deficit-defined recognition pattern documented in the Schelling-point framing above, and used it to triple the `code` category and to make the first lens-justified addition to the dense English cell. It also surfaces a tight micro-cluster — `goto fail` and Heartbleed are both 2014 TLS missing-check CVEs, the kind of within-cluster contrast the embedding-probe use case can directly exploit. The next first-wave priority remains **continuing to break the English monoculture within Latin script** *via non-English additions* (priority #3 below); high-leverage Latin-script languages still absent include Czech, Hungarian, Turkish, Tagalog, and Romanian.

### Anchor-and-neighbors curation

Past ~200 entries, the natural way to grow is **anchor-and-neighbors**: for each existing anchor entry, identify 3–10 texts that occupy a similar position in the breadth-space and have their own weaker Schelling-point status. Anchor + neighbors is how the "documents, not collections" rule scales — see the clarification above. Examples:

- φX174 genome → λ phage, human mtDNA reference (CRS), GFP, hen lysozyme, ubiquitin, bovine insulin ✓ (Sanger 1955)
- SHA-256 "abc" → other FIPS 180-4 SHA test vectors, MD5("a"), SHA-1("abc"), HMAC-SHA-1 RFC 2202 vectors
- Harvard Sentences List 1 → Lists 2–10
- Lorem Ipsum → variant lorems (Bacon Ipsum, Hipster Ipsum, Cupcake Ipsum)
- UDHR Article 1 (English) → UDHR Article 1 in 17 other languages so far ✓ (Arabic, Russian, Chinese, Hindi, Korean, French, Spanish, German, Italian, Portuguese, Polish, Latin, Dutch, Catalan, Swahili, Indonesian, Vietnamese); still to add: Sanskrit, Japanese, Tagalog, Czech, Hungarian, Turkish, … (parallel-text family)

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
| Famous code bugs (deficit-defined) | `thin` | Apple `goto fail` (CVE-2014-1266) ✓, OpenSSL Heartbleed `tls1_process_heartbeat` (CVE-2014-0160) ✓; *Ariane 5 inertial reference Ada excerpt, Trojan Source bidi minimal example, the Therac-25 race-condition pseudocode if a verbatim form can be sourced* |
| Language-lawyer constructs | `thin` | Duff's Device ✓; *the C `i = i++ + ++i` undefined-behavior canonical example, the Pascal `with` statement aliasing example* |
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
| Garden-path / parsing test sentences | `thin` | "The horse raced past the barn fell" (Bever 1970) ✓; *"Buffalo buffalo Buffalo buffalo…", "Time flies like an arrow", "The old man the boat"* |
| Linguistic well-formedness probes | `thin` | Jabberwocky stanza 1 ✓, "Colorless green ideas sleep furiously" (Chomsky 1957) ✓ |
| Vocabulary acquisition exemplars | `untouched` | *Dolch sight-word list (Edward Dolch, 1936)* |
| Minimal-syntax exemplars | `untouched` | *"the cat sat on the mat" as the canonical minimal English declarative* |

### NLP / corpus benchmarks

| Field | Status | Example artifacts |
|---|---|---|
| Treebank exemplar sentences | `untouched` | *Penn Treebank §00 sentence 1: "Pierre Vinken, 61 years old…"* |
| Reference-corpus openings | `untouched` | *first sentence of Brown Corpus A01* |
| Parallel-corpus exemplars | `thin` | UDHR Art. 1 in 18 languages ✓ (English, Arabic, Russian, Chinese, Hindi, Korean, French, Spanish, German, Italian, Portuguese, Polish, Latin, Dutch, Catalan, Swahili, Indonesian, Vietnamese); *Pater Noster (Latin Vulgate), the historical predecessor of UDHR Art. 1 in cross-language linguistic comparison* |
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
| Founding science treatises (primary sources) | `thin` | Newton's *Axiomata sive Leges Motus* (Principia Book I, 1687) ✓; *Galileo Discorsi opening, Lavoisier Traité opening, Darwin Origin opening, Watson-Crick 1953 abstract* |
| Genomic reference sequences | `thin` | φX174 ✓; *λ phage, the Cambridge Reference Sequence (human mtDNA)* |
| Protein sequences (FASTA) | `thin` | bovine insulin (Sanger 1955) ✓; *hen lysozyme, ubiquitin, GFP — one entry per protein* |
| Chemical structure notation | `thin` | caffeine canonical SMILES ✓; *SMILES for aspirin and glucose, InChI for water — one entry per molecule* |
| Mathematical constants | `untouched` | *None — π to 100 was added and later removed in a curatorial correction (the 100-digit cutoff is conventional rather than canonical, and there is no single canonical bag of bytes). A future entry under this row would need to be a constant whose canonical text is unambiguous and whose length is set by the constant rather than by an arbitrary truncation — for example, a published worked example of a continued-fraction expansion, or a NIST CODATA display value with a defined uncertainty.* |
| Integer sequences | `untouched` | *first N terms of OEIS A000040 (primes), A000045 (Fibonacci), A005150 (look-and-say) — one entry per sequence, with N fixed* |
| Famous formulas in TeX | `untouched` | *Euler's identity, Schrödinger equation — one entry per formula* |
| Physical constants (CODATA display) | `untouched` | *c, h, α, G — one entry per constant, verbatim from NIST* |
| Tabular reference datasets | `thin` | UCI Iris (`iris.data`, with the well-known row-35/row-38 errors) ✓; *Anscombe's quartet (the canonical "why you must visualise your data" example), Old Faithful eruptions, Palmer Penguins (the deliberate modern Iris replacement), Boston Housing (deprecated but historically central). One entry per dataset; canonicity is downstream of a specific historical bag of bytes, not of the underlying experiment. The category-name `dataset` was added to the schema specifically to accommodate this row.* |

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

3. **Break the language monoculture within Latin script. ⏳ In progress (two UDHR parallel-text batches + Triouleyre French pangram + Newton's Latin from the natural-sciences batch + the two lens-justified English additions from the deficit-defined batch).** 13 / 56 entries are now `english`; the absolute English count rose by 2 in the deficit-defined-canonicity batch (Chomsky's "Colorless green ideas sleep furiously" and Bever's "The horse raced past the barn fell" — both canonical *because of a flaw* with no equivalent canonical form in any other language) but English's share has continued to drop overall: 11/19 → 11/36 → 11/43 → 11/49 → 11/52 → 13/57 → 13/56, thanks to the first UDHR Article 1 batch (French, Spanish, German, Italian, Portuguese, Polish — 6 new Latin-script natural-language cells), the Triouleyre French pangram follow-on (1921, the canonical French pangram, structurally an alexandrine; bumps `french` to N=2), the second UDHR Article 1 batch (Latin, Dutch, Catalan, Swahili, Indonesian, Vietnamese — 5 new Latin-script natural-language cells, plus a second `latin` entry that pairs Lorem Ipsum with real Latin), and Newton's *Axiomata sive Leges Motus* from the natural-sciences batch (a third `latin` entry, in the early-modern scientific register, distinct from both Lorem Ipsum and the UDHR translation). The second UDHR batch deliberately moved beyond Europe: Swahili (first Bantu / Niger-Congo), Indonesian (first Austronesian), and Vietnamese (first Austroasiatic) each open a previously empty language-family cell. Remaining work continues along the same axis: more parallel-text family members for texts already in the corpus — UDHR Article 1 in Sanskrit, Japanese, Tagalog, Czech, Hungarian, Turkish, Romanian; the Pater Noster in Latin Vulgate; "I can eat glass" in several Latin-script languages. Parallel-text families let analysts hold content constant and isolate the language axis, which is the cleanest factorial structure available for embedding-sensitivity work.

Once priority #3 is in good shape (call it ~30–50 more entries), the previously-named priority clusters — NLP and linguistic Schelling points (e.g., "colorless green ideas sleep furiously", garden-path sentences, the Penn Treebank §00 sentence), cryptographic test vector families, and tokenizer / Unicode coordination strings (Markus Kuhn's UTF-8 stress test) — become the natural Phase 2 targets, with the breadth-axis structure now in place to keep them from re-creating the original bias.

## What does not belong

These categories are explicitly out of scope, recorded here so they do not get re-proposed:

- **Famous-but-not-focal strings.** Recognizable error messages, literary openings, and speech excerpts. They are famous, but practitioners do not use them as stand-ins for a class of texts. (The poetry cluster admits famous poems only when they function as focal exemplars of a *form*, not merely as famous individual works.)
- **File-format magic numbers and headers.** A literal byte field is canonical *as itself*, not as an exemplar of a class.
- **Music in text notation.** Lilypond and ABC sources for nursery tunes are reproducible but no community treats any specific transcription as a Schelling point.
- **Audio test materials, image test materials, and reference datasets accessed primarily as binary blobs.** The Utah Teapot, Lena, MNIST, SQAM clips: canonical in their fields, but not as text strings anyone bundles. Already covered in `CONTRIBUTING.md`'s "examples that fail" list. (Note: "the Iris dataset" as a *concept* is out for the same reason — but the specific UCI `iris.data` file is in, under the deficit-defined-canonicity lens, because its two well-known row-35/row-38 errors give it Schelling-point status as a particular bag of bytes that scikit-learn, R, and every other ML library bundle and reload verbatim. The lesson is that the boundary runs through "as a concept" / "as a specific historical file," not through "image vs. text" or "library import vs. copy-paste." See the **Tabular reference datasets** row in the Scientific & mathematical section above for the row this entry sits under.)
- **Statistical reference tables, A440, currency boilerplate, Rubik's-cube notation.** No focal text exists, even though the surrounding domain is well-defined.
- **Cataloging formats without canonical instances.** MARC 21, Dublin Core, MODS, BibTeX, RDA all have canonical *formats*, but no canonical *instance* records that practitioners reach for by exact bytes. Same gap as file-format magic numbers — the format is canonical, individual instances are interchangeable.
- **Journalism, advertising, marketing.** Famous headlines, leads, slogans, and ad campaigns are recognizable but not focal-as-stand-ins. Slogans are also typically trademarked. The closest borderline candidates (Hemingway six-word story, Conroy's "Two Young Men" direct-mail letter) belong to literature or copywriting craft history rather than to the corpus.
- **Bundled collections.** Per "Documents, not collections" above: TREC topic files, OEIS sequence pointers, parallel-text Bibles, and similar collection-shaped artifacts are out as single entries. Their focal individual exemplars are in.
