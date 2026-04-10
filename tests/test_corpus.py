"""Tests for the corpus singleton and Corpus API.

The default corpus holds 19 verbatim standard-example-text entries spanning
5 categories. Every entry has non-empty text under the current schema, so
most tests are simple count / equality assertions against the real data.
"""

from __future__ import annotations

import pytest

from touchstones import Corpus, corpus
from touchstones.schema import Entry


def test_corpus_singleton_loads() -> None:
    assert isinstance(corpus, Corpus)
    assert len(corpus) == 19
    assert all(isinstance(e, Entry) for e in corpus)


def test_every_entry_has_text() -> None:
    for entry in corpus:
        assert isinstance(entry.text, str)
        assert len(entry.text) > 0
        assert entry.length_tokens > 0


def test_texts_returns_flat_list_of_strings() -> None:
    texts = corpus.texts()
    assert len(texts) == 19
    assert all(isinstance(t, str) and len(t) > 0 for t in texts)


def test_labels() -> None:
    labels = corpus.labels(field="discipline")
    assert len(labels) == 19
    assert all(isinstance(label, str) for label in labels)


def test_filter_by_category() -> None:
    nl = corpus.filter(category="natural_language")
    assert isinstance(nl, Corpus)
    assert len(nl) == 12
    assert all(e.category == "natural_language" for e in nl)


def test_every_entry_has_language_and_script() -> None:
    for entry in corpus:
        assert isinstance(entry.language, str)
        assert len(entry.language) > 0
        assert isinstance(entry.script, str)
        assert len(entry.script) > 0


def test_corpus_is_currently_all_latin_script() -> None:
    # Diagnostic snapshot at the moment Scheme B landed: 19 of 19 entries use
    # Latin script. This is the bias the script field exists to surface, and
    # this assertion will fail (deliberately) when the first non-Latin entry
    # is added — at which point bump the count or replace with a richer check.
    scripts = {e.script for e in corpus}
    assert scripts == {"latin"}


def test_language_distribution_snapshot() -> None:
    # Diagnostic snapshot at the moment Scheme B landed: english dominates,
    # everything else is a singleton or close to it. Update this distribution
    # as the corpus grows.
    from collections import Counter

    languages = Counter(e.language for e in corpus)
    assert languages["english"] == 11
    assert languages["none"] == 4
    assert languages["latin"] == 1
    assert languages["c"] == 1
    assert languages["bnf"] == 1
    assert languages["http"] == 1
    assert sum(languages.values()) == 19


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
    assert len(df) == 19
    assert "name" in df.columns
    assert "category" in df.columns
    assert "license_status" in df.columns
