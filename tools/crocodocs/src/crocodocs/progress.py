"""Small terminal UX helpers for CrocoDocs commands."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Summary:
    command: str
    rows: list[tuple[str, str]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def add(self, label: str, value: object) -> None:
        """Append a label/value row to the summary table."""
        self.rows.append((label, str(value)))

    def warn(self, message: str) -> None:
        """Append a warning message to the summary."""
        self.warnings.append(message)

    def print(self) -> None:
        """Print the command name, all rows, and any warnings to stdout."""
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
        """Initialize the reporter with the name of the command being tracked."""
        self.command = command
        self._last_stage: str | None = None

    def stage(self, name: str) -> None:
        """Log the start of a named processing stage to stdout."""
        self._last_stage = name
        print(f"[{self.command}] {name}")

    def info(self, message: str) -> None:
        """Log an informational message to stdout."""
        print(f"[{self.command}] {message}")
