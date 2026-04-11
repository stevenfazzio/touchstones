"""Tests for the corpus singleton and Corpus API.

The default corpus holds 43 verbatim standard-example-text entries spanning
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
    assert len(corpus) == 43
    assert all(isinstance(e, Entry) for e in corpus)


def test_every_entry_has_text() -> None:
    for entry in corpus:
        assert isinstance(entry.text, str)
        assert len(entry.text) > 0
        assert entry.length_tokens > 0


def test_texts_returns_flat_list_of_strings() -> None:
    texts = corpus.texts()
    assert len(texts) == 43
    assert all(isinstance(t, str) and len(t) > 0 for t in texts)


def test_labels() -> None:
    labels = corpus.labels(field="discipline")
    assert len(labels) == 43
    assert all(isinstance(label, str) for label in labels)


def test_filter_by_category() -> None:
    nl = corpus.filter(category="natural_language")
    assert isinstance(nl, Corpus)
    assert len(nl) == 29
    assert all(e.category == "natural_language" for e in nl)


def test_every_entry_has_language_and_script() -> None:
    for entry in corpus:
        assert isinstance(entry.language, str)
        assert len(entry.language) > 0
        assert isinstance(entry.script, str)
        assert len(entry.script) > 0


def test_script_distribution_snapshot() -> None:
    # Diagnostic snapshot after the UDHR parallel-text batch (6 entries) and
    # the French pangram follow-on (1 entry: Triouleyre's "Portez ce vieux
    # whisky"). All seven additions are Latin script, so latin grows from
    # 26 to 33. The non-Latin counts are unchanged. Update this snapshot
    # as additional entries land.
    from collections import Counter

    scripts = Counter(e.script for e in corpus)
    assert scripts["latin"] == 33
    assert scripts["arabic"] == 1
    assert scripts["cyrillic"] == 1
    assert scripts["cjk_han"] == 1
    assert scripts["devanagari"] == 1
    assert scripts["hangul"] == 1
    assert scripts["hiragana"] == 1
    assert scripts["mixed"] == 1
    assert scripts["greek"] == 2
    assert scripts["hebrew"] == 1
    assert sum(scripts.values()) == 43


def test_language_distribution_snapshot() -> None:
    # Diagnostic snapshot after the UDHR parallel-text batch and the French
    # pangram follow-on. The UDHR batch added six new natural languages at
    # N=1 (french, spanish, german, italian, portuguese, polish); the
    # Triouleyre pangram (1921) bumps french from N=1 to N=2. English is
    # unchanged at 11 — no new English entries — but English's share of
    # the corpus drops from 11/36 to 11/43 as the breadth axis fills out.
    # Update this distribution as the corpus grows.
    from collections import Counter

    languages = Counter(e.language for e in corpus)
    # Pre-batch baseline (still correct):
    assert languages["english"] == 11
    assert languages["none"] == 4
    assert languages["latin"] == 1
    assert languages["bnf"] == 1
    assert languages["http"] == 1
    # Updated by the underpopulated-categories batch:
    assert languages["c"] == 3  # Hello World + K&R wc + Thompson quine
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
    # Languages added by the UDHR parallel-text batch:
    assert languages["french"] == 2  # UDHR Article 1 (French) + Portez ce vieux whisky pangram
    assert languages["spanish"] == 1  # UDHR Article 1 (Spanish)
    assert languages["german"] == 1  # UDHR Article 1 (German)
    assert languages["italian"] == 1  # UDHR Article 1 (Italian)
    assert languages["portuguese"] == 1  # UDHR Article 1 (Portuguese)
    assert languages["polish"] == 1  # UDHR Article 1 (Polish)
    assert sum(languages.values()) == 43


def test_filter_by_discipline() -> None:
    # Three entries list `linguistics` in their disciplines: Rainbow,
    # North Wind, and Jabberwocky.
    linguistics = corpus.filter(discipline="linguistics")
    assert len(linguistics) == 3


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
    assert len(df) == 43
    assert "name" in df.columns
    assert "category" in df.columns
    assert "license_status" in df.columns
