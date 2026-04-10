"""Tests for the touchstones Pydantic schema.

These tests exercise the `Entry` model: required fields, extra-field
rejection, every cross-field validator, frozen-ness, URL handling, and
the empty-list round-trip used by the corpus loader.
"""

from __future__ import annotations

import pytest
from pydantic import TypeAdapter, ValidationError

from touchstones.schema import Entry


@pytest.fixture
def minimal_entry_dict() -> dict:
    """A minimal valid Entry as a dict, ready for `model_validate`.

    All values are placeholders — this fixture is not a real corpus entry.
    Tests mutate copies of this dict to exercise individual validators.
    """
    return {
        "name": "Example Reference",
        "text": "Placeholder text used for testing schema validation.",
        "discipline": "testing",
        "disciplines": ["testing", "demonstration"],
        "category": "natural_language",
        "year_introduced": 2024,
        "creator": "Test Author",
        "source": "Test Suite Documentation",
        "description": "A placeholder entry used to validate the schema's behavior in unit tests.",
        "usage": "Used to verify that the Pydantic Entry model correctly enforces its rules.",
        "license_status": "public_domain",
        "url": "https://example.org/test",
        "length_tokens": 17,
    }


def test_round_trip(minimal_entry_dict: dict) -> None:
    entry = Entry.model_validate(minimal_entry_dict)
    dumped = entry.model_dump(mode="json")
    rebuilt = Entry.model_validate(dumped)
    assert entry == rebuilt


def test_missing_required_field_raises(minimal_entry_dict: dict) -> None:
    minimal_entry_dict.pop("name")
    with pytest.raises(ValidationError):
        Entry.model_validate(minimal_entry_dict)


def test_extra_field_forbidden(minimal_entry_dict: dict) -> None:
    minimal_entry_dict["bogus"] = "nope"
    with pytest.raises(ValidationError):
        Entry.model_validate(minimal_entry_dict)


def test_discipline_must_be_in_disciplines(minimal_entry_dict: dict) -> None:
    minimal_entry_dict["discipline"] = "biology"
    with pytest.raises(ValidationError, match="must appear in disciplines"):
        Entry.model_validate(minimal_entry_dict)


def test_text_none_with_length_tokens_raises(minimal_entry_dict: dict) -> None:
    minimal_entry_dict["text"] = None
    minimal_entry_dict["length_tokens"] = 5
    with pytest.raises(ValidationError, match="length_tokens must be None when text is None"):
        Entry.model_validate(minimal_entry_dict)


def test_text_set_without_length_tokens_raises(minimal_entry_dict: dict) -> None:
    minimal_entry_dict["length_tokens"] = None
    with pytest.raises(ValidationError, match="length_tokens is required"):
        Entry.model_validate(minimal_entry_dict)


def test_copyrighted_with_text_raises(minimal_entry_dict: dict) -> None:
    minimal_entry_dict["license_status"] = "copyrighted"
    with pytest.raises(ValidationError, match="text must be None when license_status"):
        Entry.model_validate(minimal_entry_dict)


def test_copyrighted_with_text_none_is_ok(minimal_entry_dict: dict) -> None:
    minimal_entry_dict["text"] = None
    minimal_entry_dict["length_tokens"] = None
    minimal_entry_dict["license_status"] = "copyrighted"
    entry = Entry.model_validate(minimal_entry_dict)
    assert entry.text is None


def test_self_reference_in_related_raises(minimal_entry_dict: dict) -> None:
    minimal_entry_dict["related"] = ["Example Reference"]
    with pytest.raises(ValidationError, match="cannot list itself in related"):
        Entry.model_validate(minimal_entry_dict)


def test_invalid_category_raises(minimal_entry_dict: dict) -> None:
    minimal_entry_dict["category"] = "not_a_real_category"
    with pytest.raises(ValidationError):
        Entry.model_validate(minimal_entry_dict)


def test_year_introduced_too_early_raises(minimal_entry_dict: dict) -> None:
    minimal_entry_dict["year_introduced"] = -4000
    with pytest.raises(ValidationError):
        Entry.model_validate(minimal_entry_dict)


def test_year_introduced_too_late_raises(minimal_entry_dict: dict) -> None:
    minimal_entry_dict["year_introduced"] = 2200
    with pytest.raises(ValidationError):
        Entry.model_validate(minimal_entry_dict)


def test_invalid_url_raises(minimal_entry_dict: dict) -> None:
    minimal_entry_dict["url"] = "not a url"
    with pytest.raises(ValidationError):
        Entry.model_validate(minimal_entry_dict)


def test_url_serializes_to_string(minimal_entry_dict: dict) -> None:
    entry = Entry.model_validate(minimal_entry_dict)
    dumped = entry.model_dump(mode="json")
    assert isinstance(dumped["url"], str)
    assert dumped["url"].startswith("https://")


def test_frozen_blocks_assignment(minimal_entry_dict: dict) -> None:
    entry = Entry.model_validate(minimal_entry_dict)
    with pytest.raises(ValidationError):
        entry.name = "Something Else"  # type: ignore[misc]


def test_dedupe_disciplines(minimal_entry_dict: dict) -> None:
    minimal_entry_dict["disciplines"] = ["testing", "testing"]
    with pytest.raises(ValidationError, match="must not contain duplicates"):
        Entry.model_validate(minimal_entry_dict)


def test_empty_list_via_type_adapter() -> None:
    adapter = TypeAdapter(list[Entry])
    assert adapter.validate_json("[]") == []
