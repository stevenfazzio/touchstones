"""Tests for the corpus singleton and Corpus API.

The default corpus holds 57 verbatim standard-example-text entries spanning
5 categories and 10 scripts. Every entry has non-empty text under the current
schema, so most tests are simple count / equality assertions against the real
data.
"""

from __future__ import annotations

import pytest

from touchstones import Corpus, corpus
from touchstones.schema import Entry


def test_corpus_singleton_loads() -> None:
    assert isinstance(corpus, Corpus)
    assert len(corpus) == 57
    assert all(isinstance(e, Entry) for e in corpus)


def test_every_entry_has_text() -> None:
    for entry in corpus:
        assert isinstance(entry.text, str)
        assert len(entry.text) > 0
        assert entry.length_tokens > 0


def test_texts_returns_flat_list_of_strings() -> None:
    texts = corpus.texts()
    assert len(texts) == 57
    assert all(isinstance(t, str) and len(t) > 0 for t in texts)


def test_labels() -> None:
    labels = corpus.labels(field="discipline")
    assert len(labels) == 57
    assert all(isinstance(label, str) for label in labels)


def test_filter_by_category() -> None:
    nl = corpus.filter(category="natural_language")
    assert isinstance(nl, Corpus)
    assert len(nl) == 38
    assert all(e.category == "natural_language" for e in nl)


def test_every_entry_has_language_and_script() -> None:
    for entry in corpus:
        assert isinstance(entry.language, str)
        assert len(entry.language) > 0
        assert isinstance(entry.script, str)
        assert len(entry.script) > 0


def test_script_distribution_snapshot() -> None:
    # Diagnostic snapshot after the deficit-defined-canonicity batch (5
    # entries: goto fail, Heartbleed, Duff's Device, Colorless green ideas,
    # The horse raced past the barn fell) — all five are Latin script, so
    # latin grows from 42 to 47. The non-Latin counts are unchanged. Update
    # this snapshot as additional entries land.
    from collections import Counter

    scripts = Counter(e.script for e in corpus)
    assert scripts["latin"] == 47
    assert scripts["arabic"] == 1
    assert scripts["cyrillic"] == 1
    assert scripts["cjk_han"] == 1
    assert scripts["devanagari"] == 1
    assert scripts["hangul"] == 1
    assert scripts["hiragana"] == 1
    assert scripts["mixed"] == 1
    assert scripts["greek"] == 2
    assert scripts["hebrew"] == 1
    assert sum(scripts.values()) == 57


def test_language_distribution_snapshot() -> None:
    # Diagnostic snapshot after the deficit-defined-canonicity batch
    # (5 entries: goto fail, Heartbleed, Duff's Device, Colorless green
    # ideas, The horse raced past the barn fell). The three code entries
    # bring `c` from 3 to 6 (joining Hello World, K&R wc, and the Thompson
    # quine). The two linguistic entries bring `english` from 11 to 13 —
    # the first absolute increase in the English count since the v0.1
    # baseline, and a deliberate one: both entries are "famous because of a
    # flaw" canonical exemplars (semantic anomaly and garden-path
    # respectively) that have no equivalent in any other language. Update
    # this distribution as the corpus grows.
    from collections import Counter

    languages = Counter(e.language for e in corpus)
    # Updated by the deficit-defined-canonicity batch:
    assert languages["english"] == 13  # +Colorless green ideas, +horse raced past barn
    assert languages["c"] == 6  # +goto fail, +Heartbleed, +Duff's Device
    # Pre-batch baseline (still correct for unchanged languages):
    assert languages["bnf"] == 1
    assert languages["http"] == 1
    # Languages added by the first non-Latin batch:
    assert languages["arabic"] == 1
    assert languages["russian"] == 1
    assert languages["chinese"] == 1
    assert languages["hindi"] == 1
    assert languages["korean"] == 1
    assert languages["japanese"] == 2  # Bashō (mixed script) + Iroha (hiragana)
    assert languages["ancient_greek"] == 1
    assert languages["koine_greek"] == 1
    assert languages["hebrew"] == 1
    # Languages added by the underpopulated-categories batch:
    assert languages["scheme"] == 1  # SICP factorial
    assert languages["cfg"] == 1  # Dragon book expression grammar
    assert languages["wsn"] == 1  # Wirth Syntax Notation
    assert languages["smtp"] == 1  # RFC 5321 transaction scenario
    assert languages["dns"] == 1  # RFC 1035 message compression
    # Languages added by the first UDHR parallel-text batch:
    assert languages["french"] == 2  # UDHR Article 1 (French) + Portez ce vieux whisky pangram
    assert languages["spanish"] == 1  # UDHR Article 1 (Spanish)
    assert languages["german"] == 1  # UDHR Article 1 (German)
    assert languages["italian"] == 1  # UDHR Article 1 (Italian)
    assert languages["portuguese"] == 1  # UDHR Article 1 (Portuguese)
    assert languages["polish"] == 1  # UDHR Article 1 (Polish)
    # Languages added by the second UDHR parallel-text batch:
    assert languages["dutch"] == 1  # UDHR Article 1 (Dutch)
    assert languages["catalan"] == 1  # UDHR Article 1 (Catalan)
    assert languages["swahili"] == 1  # UDHR Article 1 (Swahili)
    assert languages["indonesian"] == 1  # UDHR Article 1 (Indonesian)
    assert languages["vietnamese"] == 1  # UDHR Article 1 (Vietnamese)
    # Updated or added by the natural-sciences batch:
    assert languages["latin"] == 3  # Lorem Ipsum + UDHR Latin + Newton's Axiomata
    assert languages["none"] == 5  # +Sanger's bovine insulin sequence
    assert languages["smiles"] == 1  # Caffeine canonical SMILES
    assert sum(languages.values()) == 57


def test_filter_by_discipline() -> None:
    # Five entries list `linguistics` in their disciplines: Rainbow, North
    # Wind, Jabberwocky, Colorless Green Ideas, and The Horse Raced Past
    # the Barn Fell.
    linguistics = corpus.filter(discipline="linguistics")
    assert len(linguistics) == 5


def test_filter_by_tag() -> None:
    pedagogy = corpus.filter(tag="pedagogy")
    assert len(pedagogy) >= 1
    assert all("pedagogy" in e.tags for e in pedagogy)


def test_filter_combined() -> None:
    result = corpus.filter(category="natural_language", tag="phonetics")
    assert len(result) >= 1
    assert all(e.category == "natural_language" and "phonetics" in e.tags for e in result)


def test_lookup_by_name() -> None:
    rainbow = corpus["The Rainbow Passage"]
    assert rainbow.name == "The Rainbow Passage"
    assert rainbow.text is not None
    assert rainbow.length_tokens == 372


def test_lookup_unknown_name_raises() -> None:
    with pytest.raises(KeyError):
        corpus["nonexistent"]


def test_membership_check() -> None:
    assert "The Rainbow Passage" in corpus
    assert "nonexistent" not in corpus


def test_related_cross_references() -> None:
    # Triangle of kept phonetic passages — all mutually related.
    rainbow = corpus["The Rainbow Passage"]
    harvard = corpus["The Harvard Sentences"]
    north_wind = corpus["The North Wind and the Sun"]
    assert "The Harvard Sentences" in rainbow.related
    assert "The Rainbow Passage" in harvard.related
    assert "The North Wind and the Sun" in rainbow.related
    assert "The Rainbow Passage" in north_wind.related

    # A new bidirectional pair wired in during the refactor.
    fox = corpus["The Quick Brown Fox"]
    now = corpus["Now is the Time"]
    assert "Now is the Time" in fox.related
    assert "The Quick Brown Fox" in now.related


def test_to_dataframe() -> None:
    pytest.importorskip("pandas")
    df = corpus.to_dataframe()
    assert len(df) == 57
    assert "name" in df.columns
    assert "category" in df.columns
    assert "license_status" in df.columns
