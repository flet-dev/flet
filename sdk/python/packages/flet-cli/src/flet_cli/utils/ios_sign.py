"""
Reading the provisioning profiles installed for signing iOS builds.

A build names the profile it wants, and Xcode resolves that name — or
UUID — against the profiles installed on the machine. These helpers read
the same profiles, so a build can resolve and validate its own
configuration before handing it to Xcode.
"""

import datetime
import plistlib
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

PROFILE_DIRS = (
    Path.home() / "Library" / "MobileDevice" / "Provisioning Profiles",
    Path.home()
    / "Library"
    / "Developer"
    / "Xcode"
    / "UserData"
    / "Provisioning Profiles",
)
"""
Xcode reads installed profiles from here for command-line builds. Xcode 16 added
~/Library/Developer/Xcode/UserData/Provisioning Profiles for profiles it manages
itself; both are searched so a profile installed either way is recognized.
"""


@dataclass
class ProvisioningProfile:
    """An installed provisioning profile, as Xcode sees it."""

    name: str
    """The profile's name — what `PROVISIONING_PROFILE_SPECIFIER` matches."""

    uuid: str
    """The profile's UUID, also accepted as a specifier."""

    team_id: Optional[str]
    """First team the profile belongs to, if it declares one."""

    application_identifier: Optional[str]
    """The App ID it authorizes, explicit or wildcard."""

    expires: Optional[datetime.datetime]
    """Expiration date, if present."""

    path: Path
    """Where the profile is installed."""

    @property
    def expired(self) -> bool:
        """Whether the profile's expiration date has passed."""
        if self.expires is None:
            return False
        expires = self.expires
        if expires.tzinfo is None:
            expires = expires.replace(tzinfo=datetime.timezone.utc)
        return expires < datetime.datetime.now(datetime.timezone.utc)


def _read_profile(path: Path) -> Optional[ProvisioningProfile]:
    """
    Decode a single CMS-wrapped `.mobileprovision` file.

    Args:
        path: Path to the installed profile.

    Returns:
        The profile's contents, or `None` when the file cannot be decoded
            or lacks the keys Xcode matches on.
    """
    result = subprocess.run(
        ["security", "cms", "-D", "-i", str(path)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    try:
        values = plistlib.loads(result.stdout.encode())
        teams = values.get("TeamIdentifier") or []
        return ProvisioningProfile(
            name=values["Name"],
            uuid=values["UUID"],
            team_id=teams[0] if teams else None,
            application_identifier=(values.get("Entitlements") or {}).get(
                "application-identifier"
            ),
            expires=values.get("ExpirationDate"),
            path=path,
        )
    except (plistlib.InvalidFileException, ValueError, KeyError, TypeError):
        return None


def installed_provisioning_profiles() -> list[ProvisioningProfile]:
    """
    Read every provisioning profile installed for the current user.

    Both directories Xcode reads are scanned, and profiles present in both
    are returned once.

    Returns:
        The installed profiles, ordered by directory then filename.
            Unreadable files are skipped.
    """
    profiles = []
    seen = set()
    for directory in PROFILE_DIRS:
        if not directory.is_dir():
            continue
        for path in sorted(directory.glob("*.mobileprovision")):
            profile = _read_profile(path)
            if profile is not None and profile.uuid not in seen:
                seen.add(profile.uuid)
                profiles.append(profile)
    return profiles


def find_provisioning_profile(
    specifier: str, profiles: list[ProvisioningProfile]
) -> Optional[ProvisioningProfile]:
    """
    Resolve a profile the way Xcode's specifier does — by name or UUID.

    Args:
        specifier: The configured profile name or UUID.
        profiles: Candidates, typically from `installed_provisioning_profiles()`.

    Returns:
        The matching profile, or `None` when nothing matches.
    """
    specifier = specifier.strip()
    for profile in profiles:
        if specifier in (profile.name, profile.uuid):
            return profile
    return None
