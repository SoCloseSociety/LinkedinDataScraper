"""Data models for LinkedIn profile data."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Experience:
    """A single work experience entry."""

    title: str = ""
    company: str = ""
    location: Optional[str] = None
    date_range: Optional[str] = None
    duration: Optional[str] = None
    description: Optional[str] = None

    def summary(self) -> str:
        parts = []
        if self.title:
            parts.append(self.title)
        if self.company:
            parts.append(f"@ {self.company}")
        return " ".join(parts) if parts else ""


@dataclass
class Education:
    """A single education entry."""

    school: str = ""
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    date_range: Optional[str] = None

    def summary(self) -> str:
        parts = []
        if self.degree:
            parts.append(self.degree)
        if self.field_of_study:
            parts.append(self.field_of_study)
        if self.school:
            parts.append(f"- {self.school}")
        return " ".join(parts) if parts else self.school


@dataclass
class LinkedInProfile:
    """Complete LinkedIn profile data."""

    # Identity (from search results)
    full_name: str = ""
    headline: Optional[str] = None
    current_company: Optional[str] = None
    location: Optional[str] = None
    profile_url: str = ""

    # Profile detail page
    about: Optional[str] = None
    industry: Optional[str] = None
    connections_count: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None

    # Experience
    experiences: list[Experience] = field(default_factory=list)
    current_title: Optional[str] = None

    # Education
    education: list[Education] = field(default_factory=list)

    # Skills
    skills: list[str] = field(default_factory=list)

    # Metadata
    scraped_at: str = field(default_factory=lambda: datetime.now().isoformat())
    search_query: str = ""
    search_location: str = ""
    data_source: str = "search"  # "search" | "profile" | "api"

    def experience_summary(self, max_entries: int = 3) -> str:
        return " | ".join(
            e.summary() for e in self.experiences[:max_entries] if e.summary()
        )

    def education_summary(self, max_entries: int = 2) -> str:
        return " | ".join(
            e.summary() for e in self.education[:max_entries] if e.summary()
        )

    def skills_summary(self, max_entries: int = 5) -> str:
        return ", ".join(self.skills[:max_entries])
