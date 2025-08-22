#!/usr/bin/env bash
set -e

# ------------------------------------------------------------------------------
# This script determines the version numbers used in builds and releases.
#
# It sets three environment variables:
#   - PKG_VER   → The package version (semantic version).
#   - BUILD_VER → The build identifier (may include build number).
#   - PYPI_VER  → A PyPI-compatible version string for publishing.
#
# Behavior:
#   - On a tagged commit (e.g. "v1.2.3"), it uses that tag as the version.
#   - On an untagged commit, it generates a "next dev version" by:
#       • Taking the latest tag (default v0.0.0 if none).
#       • Incrementing the minor version.
#       • Appending "+<run number>".
#   - PYPI_VER is derived from BUILD_VER by replacing "+" with ".dev".
#
# This ensures that:
#   - Release builds (tags) get clean versions like "1.2.3".
#   - Development builds get versions like "1.3.0+45" (PyPI: "1.3.0.dev45").
# ------------------------------------------------------------------------------

if [[ "$GITHUB_REF" == refs/tags/* ]]; then
    # -------------------------------------------------------------
    # Case 1: This build is triggered by a Git tag
    # -------------------------------------------------------------
    # Extract the tag name (strip "refs/tags/")
    tag="${GITHUB_REF#refs/tags/}"
    # Remove leading "v" if present (e.g. "v1.2.3" → "1.2.3")
    export PKG_VER="${tag#v}"
    # For tagged releases, BUILD_VER is the same as PKG_VER
    export BUILD_VER="$PKG_VER"
else
    # -------------------------------------------------------------
    # Case 2: This is not a tagged build (e.g. main branch commit)
    # -------------------------------------------------------------
    # Get the latest tag, or fall back to "v0.0.0" if none exist
    cv=$(git describe --abbrev=0 2>/dev/null || echo "v0.0.0")
    # Remove leading "v" if present
    cv=${cv#v}

    # Split into major/minor components
    major=$(echo "$cv" | cut -d. -f1)
    minor=$(echo "$cv" | cut -d. -f2)

    # Increment the minor version (e.g. "1.2" → "1.3")
    minor=$((minor + 1))

    # Construct the package version: <major>.<minor>.0
    export PKG_VER="${major}.${minor}.0"

    # Append the GitHub Actions run number for uniqueness
    export BUILD_VER="${PKG_VER}+$((GITHUB_RUN_NUMBER + 500))"
fi

# -------------------------------------------------------------
# Derive PyPI-compatible version
# PyPI does not accept "+" in versions, so replace with ".dev"
# Example: "1.3.0+45" → "1.3.0.dev45"
# -------------------------------------------------------------
export PYPI_VER="${BUILD_VER/+/.dev}"

# Print values for debugging in logs
echo "PKG_VER=$PKG_VER"
echo "BUILD_VER=$BUILD_VER"
echo "PYPI_VER=$PYPI_VER"

# Export values as environment variables
echo "PKG_VER=$PKG_VER" >> $GITHUB_ENV
echo "BUILD_VER=$BUILD_VER" >> $GITHUB_ENV
echo "PYPI_VER=$PYPI_VER" >> $GITHUB_ENV
