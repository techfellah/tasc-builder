from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectConfiguration:
    language: str
    framework: str
    runtime: str
    output_directory: str

    def to_dict(self) -> dict[str, object]:
        return {
            "language": self.language,
            "framework": self.framework,
            "runtime": self.runtime,
            "output_directory": self.output_directory,
        }
