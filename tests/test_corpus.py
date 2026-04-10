"""Tests for the corpus singleton and Corpus API.

The default corpus contains 6 seeded entries spanning multiple
categories, license statuses, and text/no-text paths. These tests
exercise the full API surface against real data.
"""

from __future__ import annotations

import pytest

from touchstones import Corpus, corpus
from touchstones.schema import Entry


def test_corpus_singleton_loads() -> None:
    assert isinstance(corpus, Corpus)
    assert len(corpus) == 6
    assert all(isinstance(e, Entry) for e in corpus)


def test_texts_returns_entries_with_text() -> None:
    texts = corpus.texts()
    assert len(texts) == 2
    assert all(isinstance(t, str) for t in texts)


def test_texts_include_none() -> None:
    texts = corpus.texts(include_none=True)
    assert len(texts) == 6
    assert sum(t is None for t in texts) == 4


def test_labels() -> None:
    labels = corpus.labels(field="discipline")
    assert len(labels) == 6
    assert all(isinstance(label, str) for label in labels)


def test_filter_by_category() -> None:
    tabular = corpus.filter(category="tabular")
    assert isinstance(tabular, Corpus)
    assert len(tabular) == 2
    assert all(e.category == "tabular" for e in tabular)


def test_filter_by_discipline() -> None:
    stats = corpus.filter(discipline="statistics")
    assert len(stats) == 2


def test_filter_by_tag() -> None:
    pedagogy = corpus.filter(tag="pedagogy")
    assert len(pedagogy) >= 1
    assert all("pedagogy" in e.tags for e in pedagogy)


def test_filter_combined() -> None:
    result = corpus.filter(category="tabular", tag="pedagogy")
    assert len(result) >= 1
    assert all(e.category == "tabular" and "pedagogy" in e.tags for e in result)


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
    anscombe = corpus["Anscombe's Quartet"]
    iris = corpus["Iris Dataset"]
    assert "Iris Dataset" in anscombe.related
    assert "Anscombe's Quartet" in iris.related

    teapot = corpus["The Utah Teapot"]
    lena = corpus["Lena"]
    assert "Lena" in teapot.related
    assert "The Utah Teapot" in lena.related


def test_copyrighted_entry_has_no_text() -> None:
    lena = corpus["Lena"]
    assert lena.license_status == "copyrighted"
    assert lena.text is None
    assert lena.length_tokens is None


def test_to_dataframe() -> None:
    pytest.importorskip("pandas")
    df = corpus.to_dataframe()
    assert len(df) == 6
    assert "name" in df.columns
    assert "category" in df.columns
    assert "license_status" in df.columns
