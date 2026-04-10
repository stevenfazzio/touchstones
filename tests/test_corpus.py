"""Smoke tests for the empty corpus.

The default corpus is empty in v0.1, so these tests verify the API
surface works against zero entries — no entries to look up, iterate,
filter, or convert. They protect against import-time regressions and
catch the obvious "method exists" failures before any seeding happens.
"""

from __future__ import annotations

import pytest

from touchstones import Corpus, corpus


def test_corpus_singleton_loads_empty() -> None:
    assert isinstance(corpus, Corpus)
    assert len(corpus) == 0
    assert list(corpus) == []
    assert corpus.texts() == []
    assert corpus.texts(include_none=True) == []
    assert corpus.labels(field="discipline") == []


def test_filter_on_empty_corpus_returns_empty() -> None:
    filtered = corpus.filter(discipline="speech pathology")
    assert isinstance(filtered, Corpus)
    assert len(filtered) == 0


def test_lookup_unknown_name_raises() -> None:
    with pytest.raises(KeyError):
        corpus["nonexistent"]


def test_membership_check() -> None:
    assert "nonexistent" not in corpus


def test_to_dataframe_on_empty_corpus() -> None:
    pytest.importorskip("pandas")
    df = corpus.to_dataframe()
    assert len(df) == 0
