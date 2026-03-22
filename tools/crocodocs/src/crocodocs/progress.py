"""Small terminal UX helpers for CrocoDocs commands."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Summary:
    command: str
    rows: list[tuple[str, str]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def add(self, label: str, value: object) -> None:
        self.rows.append((label, str(value)))

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def print(self) -> None:
        print()
        print(f"Summary: {self.command}")
        for label, value in self.rows:
            print(f"  {label}: {value}")
        if self.warnings:
            print("  warnings:")
            for warning in self.warnings:
                print(f"    - {warning}")


class ProgressReporter:
    """Simple stage-based progress logging."""

    def __init__(self, command: str) -> None:
        self.command = command
        self._last_stage: str | None = None

    def stage(self, name: str) -> None:
        self._last_stage = name
        print(f"[{self.command}] {name}")

    def info(self, message: str) -> None:
        print(f"[{self.command}] {message}")
