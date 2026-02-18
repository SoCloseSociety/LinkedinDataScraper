"""Intercept LinkedIn Voyager API responses for structured data extraction.

LinkedIn's React frontend fetches all data from an internal REST API
at /voyager/api/... — by intercepting these network responses we get
stable JSON instead of fragile DOM structures.
"""

from __future__ import annotations

import json
import logging
import re
from typing import Optional

from playwright.async_api import Response

from linkedin_scraper.models import Education, Experience, LinkedInProfile

logger = logging.getLogger(__name__)


class VoyagerInterceptor:
    """Capture and parse LinkedIn Voyager API responses."""

    def __init__(self):
        self._search_results: list[dict] = []
        self._profiles: dict[str, dict] = {}  # public_id -> profile data
        self._contact_info: dict[str, dict] = {}  # public_id -> contact data
        self._skills: dict[str, list[str]] = {}  # public_id -> skill list

    # ------------------------------------------------------------------
    # Callback — attach to page.on("response", ...)
    # ------------------------------------------------------------------

    async def handle_response(self, response: Response) -> None:
        url = response.url
        if "/voyager/api/" not in url:
            return
        if response.status != 200:
            return

        try:
            text = await response.text()
            if not text:
                return
            stripped = text.strip()
            # LinkedIn responses are always JSON objects or arrays
            if not (stripped.startswith("{") or stripped.startswith("[")):
                return
            data = json.loads(stripped)
        except Exception:
            return

        if not isinstance(data, dict):
            return

        try:
            url_lower = url.lower()

            # Search results
            if "search" in url_lower and any(
                k in url_lower for k in ("clusters", "blended", "people")
            ):
                self._parse_search(data)

            # Contact info
            elif "profilecontactinfo" in url_lower or "contactinfo" in url_lower:
                self._parse_contact(url, data)

            # Skills
            elif any(k in url_lower for k in ("normskills", "/skills", "featuredbysection")):
                self._parse_skills(url, data)

            # Profile data (identity endpoints)
            elif "/identity/" in url_lower and any(
                k in url_lower for k in ("profile", "position", "education", "dash")
            ):
                self._parse_profile(url, data)

        except Exception as exc:
            logger.debug("Voyager parse error for %s: %s", url, exc)

    # ------------------------------------------------------------------
    # Search results
    # ------------------------------------------------------------------

    def _parse_search(self, data: dict) -> None:
        """Extract mini-profiles from search cluster responses."""
        included = data.get("included", [])
        for item in included:
            recipe = item.get("$type", "") or item.get("_type", "")

            # Mini-profile objects
            if "MiniProfile" in recipe or "miniProfile" in recipe:
                profile = self._extract_mini_profile(item)
                if profile and profile.get("public_id"):
                    # Avoid duplicates
                    if not any(
                        r.get("public_id") == profile["public_id"]
                        for r in self._search_results
                    ):
                        self._search_results.append(profile)
                continue

            # Also check for nested miniProfile inside other objects
            mini = item.get("miniProfile") or item.get("hitInfo", {}).get(
                "com.linkedin.voyager.search.SearchProfile", {}
            ).get("miniProfile")
            if mini:
                profile = self._extract_mini_profile(mini)
                if profile and profile.get("public_id"):
                    if not any(
                        r.get("public_id") == profile["public_id"]
                        for r in self._search_results
                    ):
                        self._search_results.append(profile)

    def _extract_mini_profile(self, item: dict) -> Optional[dict]:
        """Pull relevant fields from a MiniProfile JSON object."""
        public_id = item.get("publicIdentifier") or item.get("public_id", "")
        if not public_id:
            # Try to extract from entityUrn
            urn = item.get("entityUrn", "")
            match = re.search(r"fs_miniProfile:(.+)", urn)
            if match:
                public_id = match.group(1)

        if not public_id:
            return None

        first = item.get("firstName", "")
        last = item.get("lastName", "")
        full_name = f"{first} {last}".strip()

        return {
            "public_id": public_id,
            "full_name": full_name,
            "headline": item.get("occupation", "") or item.get("headline", ""),
            "location": item.get("locationName", ""),
            "profile_url": f"https://www.linkedin.com/in/{public_id}/",
        }

    # ------------------------------------------------------------------
    # Full profile
    # ------------------------------------------------------------------

    def _parse_profile(self, url: str, data: dict) -> None:
        """Extract full profile data from identity API responses."""
        included = data.get("included", [])
        for item in included:
            type_str = item.get("$type", "") or ""

            # Full profile object
            if "Profile" in type_str and item.get("publicIdentifier"):
                pid = item["publicIdentifier"]
                existing = self._profiles.get(pid, {})

                # Parse connections count from various response formats
                conn_count = ""
                conns = item.get("connections")
                if isinstance(conns, dict):
                    paging = conns.get("paging", {})
                    conn_count = str(paging.get("total", "")) if paging else ""
                elif isinstance(conns, (int, float)):
                    conn_count = str(int(conns))

                existing.update({
                    "public_id": pid,
                    "full_name": f"{item.get('firstName', '')} {item.get('lastName', '')}".strip(),
                    "headline": item.get("headline", ""),
                    "location": item.get("locationName", "") or item.get("geoLocationName", ""),
                    "industry": item.get("industryName", "") or item.get("industry", ""),
                    "about": item.get("summary", ""),
                    "connections_count": conn_count,
                    "entityUrn": item.get("entityUrn", ""),
                    "_member_urn": item.get("entityUrn", ""),
                })
                self._profiles[pid] = existing

            # Position objects (experience)
            if "Position" in type_str:
                self._parse_position(item)

            # Education objects
            if "Education" in type_str:
                self._parse_education(item)

    def _parse_position(self, item: dict) -> None:
        """Extract a work position and attach it to the right profile."""
        company_name = ""
        company = item.get("company") or item.get("companyName")
        if isinstance(company, dict):
            company_name = (
                company.get("miniCompany", {}).get("name", "")
                or company.get("name", "")
            )
        elif isinstance(company, str):
            company_name = company

        position = {
            "title": item.get("title", ""),
            "company": company_name,
            "location": item.get("locationName", ""),
            "date_range": self._build_date_range(item.get("timePeriod", {})),
        }

        # Try to find which profile this position belongs to
        pid = self._resolve_owner(item)
        if pid and pid in self._profiles:
            self._profiles[pid].setdefault("positions", []).append(position)
        elif self._profiles:
            # Attach to the last known profile being visited
            last_pid = list(self._profiles.keys())[-1]
            self._profiles[last_pid].setdefault("positions", []).append(position)

    def _parse_education(self, item: dict) -> None:
        """Extract an education entry."""
        school_obj = item.get("school", {}) or {}
        edu = {
            "school": item.get("schoolName", "") or school_obj.get("name", ""),
            "degree": item.get("degreeName", ""),
            "field_of_study": item.get("fieldOfStudy", ""),
            "date_range": self._build_date_range(item.get("timePeriod", {})),
        }
        if not edu["school"] and not edu["degree"]:
            return

        pid = self._resolve_owner(item)
        if pid and pid in self._profiles:
            self._profiles[pid].setdefault("education", []).append(edu)
        elif self._profiles:
            last_pid = list(self._profiles.keys())[-1]
            self._profiles[last_pid].setdefault("education", []).append(edu)

    def _resolve_owner(self, item: dict) -> Optional[str]:
        """Try to determine which profile an item (position/education) belongs to."""
        urn = item.get("entityUrn", "")
        # URN format: urn:li:fs_position:(ACoAABxxxxxxx,123456)
        match = re.search(r"\(([^,)]+)", urn)
        if match:
            member_urn = match.group(1)
            for pid, pdata in self._profiles.items():
                if member_urn in pdata.get("_member_urn", ""):
                    return pid
                # Also check the profile's entityUrn
                p_urn = pdata.get("entityUrn", "")
                if member_urn in p_urn:
                    return pid
        return None

    # ------------------------------------------------------------------
    # Contact info
    # ------------------------------------------------------------------

    def _parse_contact(self, url: str, data: dict) -> None:
        """Extract email, phone, website from contact info response."""
        # URL: .../identity/profiles/{publicId}/profileContactInfo
        match = re.search(r"/profiles/([^/]+)/profileContactInfo", url)
        pid = match.group(1) if match else ""

        contact = {}
        payload = data.get("data", data)

        # Email addresses
        emails = payload.get("emailAddress", {})
        if isinstance(emails, str) and emails:
            contact["email"] = emails
        elif isinstance(emails, dict):
            contact["email"] = emails.get("emailAddress", "")

        # Phone numbers
        phones = payload.get("phoneNumbers", [])
        if isinstance(phones, list) and phones:
            contact["phone"] = phones[0].get("number", "") if isinstance(phones[0], dict) else str(phones[0])

        # Websites
        websites = payload.get("websites", [])
        if isinstance(websites, list) and websites:
            contact["website"] = websites[0].get("url", "") if isinstance(websites[0], dict) else str(websites[0])

        # Twitter
        twitter = payload.get("twitterHandles", [])
        if isinstance(twitter, list) and twitter:
            handle = twitter[0].get("name", "") if isinstance(twitter[0], dict) else str(twitter[0])
            if handle:
                contact["twitter"] = f"https://twitter.com/{handle}"

        if pid:
            self._contact_info[pid] = contact
        elif self._profiles:
            # Attach to last-known profile
            last_pid = list(self._profiles.keys())[-1]
            self._contact_info[last_pid] = contact

    # ------------------------------------------------------------------
    # Skills
    # ------------------------------------------------------------------

    def _parse_skills(self, url: str, data: dict) -> None:
        """Extract skills list."""
        included = data.get("included", [])
        skills = []
        for item in included:
            name = item.get("name", "")
            if name and isinstance(name, str):
                skills.append(name)

        if skills:
            # Attach to last-known profile
            if self._profiles:
                pid = list(self._profiles.keys())[-1]
                self._skills[pid] = skills

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _build_date_range(time_period: dict) -> str:
        if not time_period or not isinstance(time_period, dict):
            return ""
        start = time_period.get("startDate", {})
        end = time_period.get("endDate", {})
        parts = []
        if start:
            month = start.get("month", "")
            year = start.get("year", "")
            parts.append(f"{month}/{year}" if month else str(year))
        if end:
            month = end.get("month", "")
            year = end.get("year", "")
            parts.append(f"{month}/{year}" if month else str(year))
        else:
            parts.append("Present")
        return " - ".join(parts)

    # ------------------------------------------------------------------
    # Public accessors
    # ------------------------------------------------------------------

    def get_search_results(self) -> list[dict]:
        return list(self._search_results)

    def get_profile_data(self, public_id: str) -> dict:
        return self._profiles.get(public_id, {})

    def get_contact_info(self, public_id: str) -> dict:
        return self._contact_info.get(public_id, {})

    def get_skills(self, public_id: str) -> list[str]:
        return self._skills.get(public_id, [])

    def build_profile(
        self,
        public_id: str,
        search_data: Optional[dict] = None,
        search_query: str = "",
        search_location: str = "",
    ) -> LinkedInProfile:
        """Merge all captured data for a public_id into a LinkedInProfile."""
        sd = search_data or {}
        pd = self._profiles.get(public_id, {})
        ci = self._contact_info.get(public_id, {})
        sk = self._skills.get(public_id, [])

        # Build experiences
        experiences = []
        for pos in pd.get("positions", []):
            experiences.append(Experience(
                title=pos.get("title", ""),
                company=pos.get("company", ""),
                location=pos.get("location"),
                date_range=pos.get("date_range"),
            ))

        # Build education
        education = []
        for edu in pd.get("education", []):
            education.append(Education(
                school=edu.get("school", ""),
                degree=edu.get("degree"),
                field_of_study=edu.get("field_of_study"),
                date_range=edu.get("date_range"),
            ))

        profile = LinkedInProfile(
            full_name=pd.get("full_name") or sd.get("full_name", ""),
            headline=pd.get("headline") or sd.get("headline"),
            current_company=experiences[0].company if experiences else None,
            location=pd.get("location") or sd.get("location"),
            profile_url=sd.get("profile_url", f"https://www.linkedin.com/in/{public_id}/"),
            about=pd.get("about"),
            industry=pd.get("industry"),
            connections_count=pd.get("connections_count"),
            email=ci.get("email"),
            phone=ci.get("phone"),
            website=ci.get("website"),
            experiences=experiences,
            current_title=experiences[0].title if experiences else None,
            education=education,
            skills=sk,
            search_query=search_query,
            search_location=search_location,
            data_source="api" if pd else "search",
        )

        return profile

    def clear(self) -> None:
        self._search_results.clear()
        self._profiles.clear()
        self._contact_info.clear()
        self._skills.clear()
