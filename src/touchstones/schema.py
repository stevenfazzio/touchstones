"""Pydantic schema for the touchstones corpus.

Defines the `Entry` model — a single canonical reference artifact —
along with its supporting types: the `LicenseStatus` enum and the
`Category` Literal. All entries in `data/entries.json` are validated
against this schema at corpus load time.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Annotated, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    model_validator,
)


class LicenseStatus(StrEnum):
    """Legal status of an entry's text content."""

    PUBLIC_DOMAIN = "public_domain"
    FAIR_USE = "fair_use"
    UNCLEAR = "unclear"


Category = Literal[
    "natural_language",
    "code",
    "notation",
    "sequence",
    "protocol",
]


class Entry(BaseModel):
    """A single canonical reference artifact in the touchstones corpus."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        str_strip_whitespace=True,
    )

    name: Annotated[
        str,
        Field(
            min_length=1,
            max_length=200,
            description=(
                "Short canonical name; serves as the primary key (e.g. 'The Rainbow Passage')."
            ),
        ),
    ]

    text: Annotated[
        str,
        Field(
            min_length=1,
            description="The verbatim text itself — the artifact this entry exists to bundle.",
        ),
    ]

    discipline: Annotated[
        str,
        Field(
            min_length=1,
            max_length=100,
            description="Primary field of use (e.g. 'speech pathology').",
        ),
    ]

    disciplines: Annotated[
        list[str],
        Field(
            min_length=1,
            description="All fields where this artifact is used. Must include `discipline`.",
        ),
    ]

    category: Annotated[
        Category,
        Field(
            description=(
                "Broad artifact grouping (natural_language, code, notation, sequence, protocol)."
            )
        ),
    ]

    language: Annotated[
        str,
        Field(
            min_length=1,
            max_length=50,
            description=(
                "Primary symbol system the text is written in. Lowercase short identifier "
                "shared by natural and programming languages and notation systems "
                "(e.g. 'english', 'latin', 'japanese', 'c', 'python', 'bnf', 'http'). "
                "Use 'none' for non-linguistic data such as raw hashes, numeric sequences, "
                "or genomic strings. The convention is 'what would a search-by-language user type'."
            ),
        ),
    ]

    script: Annotated[
        str,
        Field(
            min_length=1,
            max_length=50,
            description=(
                "Writing script the bytes are rendered in (e.g. 'latin', 'cyrillic', "
                "'cjk_han', 'devanagari', 'arabic', 'hebrew', 'greek'). Use 'mixed' "
                "only for genuine multi-script texts where no script dominates. "
                "Often derivable from `language` but kept as its own axis so the corpus "
                "can be filtered by script independently."
            ),
        ),
    ]

    year_introduced: Annotated[
        int,
        Field(
            ge=-3000,
            le=2100,
            description="Year first published or standardized. BCE values are negative.",
        ),
    ]

    creator: Annotated[
        str,
        Field(
            min_length=1,
            max_length=300,
            description="Person or organization that created or formalized the artifact.",
        ),
    ]

    source: Annotated[
        str,
        Field(
            min_length=1,
            description="Original publication or standard, with citation.",
        ),
    ]

    description: Annotated[
        str,
        Field(
            min_length=20,
            max_length=2000,
            description="1-3 sentence summary of what it is and why it is canonical.",
        ),
    ]

    usage: Annotated[
        str,
        Field(
            min_length=20,
            max_length=2000,
            description="What the artifact is used to test, demonstrate, or benchmark.",
        ),
    ]

    known_issues: Annotated[
        str | None,
        Field(
            default=None,
            max_length=4000,
            description="Documented problems, biases, or controversies. None if none known.",
        ),
    ]

    alternatives: Annotated[
        str | None,
        Field(
            default=None,
            max_length=2000,
            description="Known replacements or modernized versions. None if none known.",
        ),
    ]

    related: Annotated[
        list[str],
        Field(
            default_factory=list,
            description="Names of other corpus entries that are connected. Empty list if none.",
        ),
    ]

    length_tokens: Annotated[
        int,
        Field(
            ge=0,
            description="Approximate token count of `text` using the cl100k_base encoding.",
        ),
    ]

    license_status: Annotated[
        LicenseStatus,
        Field(description="Legal status of the text content."),
    ]

    tags: Annotated[
        list[str],
        Field(
            default_factory=list,
            description="Freeform tags for cross-cutting themes.",
        ),
    ]

    url: Annotated[
        HttpUrl,
        Field(description="Link to authoritative source or full text."),
    ]

    @model_validator(mode="after")
    def _check_invariants(self) -> Entry:
        # 1. discipline must appear in disciplines
        if self.discipline not in self.disciplines:
            raise ValueError(
                f"discipline {self.discipline!r} must appear in disciplines {self.disciplines}"
            )

        # 2. self-reference check
        if self.name in self.related:
            raise ValueError(f"entry {self.name!r} cannot list itself in related")

        # 3. dedupe checks
        for field_name, value in [
            ("disciplines", self.disciplines),
            ("related", self.related),
            ("tags", self.tags),
        ]:
            if len(set(value)) != len(value):
                raise ValueError(f"{field_name} must not contain duplicates")

        return self
