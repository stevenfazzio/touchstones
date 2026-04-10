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
    COPYRIGHTED = "copyrighted"
    UNCLEAR = "unclear"


Category = Literal[
    "natural_language",
    "sequence",
    "notation",
    "visual",
    "audio",
    "tabular",
    "code",
    "3d_model",
    "mathematical",
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
        str | None,
        Field(
            default=None,
            description=(
                "Actual textual content. None if copyrighted, non-textual, "
                "or otherwise not embedded."
            ),
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
        Field(description="Broad artifact grouping (natural_language, visual, tabular, ...)."),
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
        int | None,
        Field(
            default=None,
            ge=0,
            description="Approximate token count (cl100k_base). None for non-text entries.",
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

        # 2. length_tokens is None iff text is None
        if self.text is None and self.length_tokens is not None:
            raise ValueError("length_tokens must be None when text is None")
        if self.text is not None and self.length_tokens is None:
            raise ValueError("length_tokens is required when text is provided")

        # 3. copyrighted entries must not bundle text (use fair_use for excerpts)
        if self.license_status == LicenseStatus.COPYRIGHTED and self.text is not None:
            raise ValueError(
                "text must be None when license_status is 'copyrighted'; "
                "use 'fair_use' if the excerpt qualifies"
            )

        # 4. self-reference check
        if self.name in self.related:
            raise ValueError(f"entry {self.name!r} cannot list itself in related")

        # 5. dedupe checks
        for field_name, value in [
            ("disciplines", self.disciplines),
            ("related", self.related),
            ("tags", self.tags),
        ]:
            if len(set(value)) != len(value):
                raise ValueError(f"{field_name} must not contain duplicates")

        return self
