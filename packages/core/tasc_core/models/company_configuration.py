from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CompanyConfiguration:
    name: str
    domain: str | None = None
    contact_email: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "domain": self.domain,
            "contact_email": self.contact_email,
        }
