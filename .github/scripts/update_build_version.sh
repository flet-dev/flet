#!/usr/bin/env bash
set -e

# ------------------------------------------------------------------------------
# This script determines the version numbers used in builds and releases.
#
# It sets three environment variables:
#   - PKG_VER   → The package version (semantic version).
#   - BUILD_NUM → The build number (github run number plus offset).
#   - PYPI_VER  → A PyPI-compatible version string for publishing.
#
# Behavior:
#   - On a tagged commit (e.g. "v1.2.3"), it uses that tag as the version.
#   - On an untagged commit, it generates a "next dev version" by:
#       • Taking the latest tag (default v0.0.0 if none).
#       • Incrementing the minor version.
#       • Appending "+<run number>".
#
# This ensures that:
#   - Release builds (tags) get clean versions like "1.2.3".
#   - Development builds get versions like "1.3.0+45" (PyPI: "1.3.0.dev45").
# ------------------------------------------------------------------------------

export BUILD_NUM="$((GITHUB_RUN_NUMBER + 6000))" # TODO: adjust offset as needed

if [[ "$GITHUB_REF" == refs/tags/* ]]; then
    # -------------------------------------------------------------
    # Case 1: This build is triggered by a Git tag
    # -------------------------------------------------------------
    # Extract the tag name (strip "refs/tags/")
    tag="${GITHUB_REF#refs/tags/}"
    # Remove leading "v" if present (e.g. "v1.2.3" → "1.2.3")
    export PKG_VER="${tag#v}"
    export PYPI_VER="$PKG_VER"
else
    # -------------------------------------------------------------
    # Case 2: This is not a tagged build (e.g. main branch commit)
    # -------------------------------------------------------------
    # Get the latest tag, or fall back to "v0.0.0" if none exist
    cv=$(git describe --abbrev=0 2>/dev/null || echo "v0.0.0")
    # Remove leading "v" if present
    cv=${cv#v}

    # Split into major/minor/patch components
    major=$(echo "$cv" | cut -d. -f1)
    minor=$(echo "$cv" | cut -d. -f2)
    patch=$(echo "$cv" | cut -d. -f3)

    # Increment patch version (e.g. "1.2.3" → "1.2.4")
    patch=$((patch + 1))

    # Construct the package version: <major>.<minor>.<patch>
    export PKG_VER="${major}.${minor}.${patch}"
    # PyPI build version: <PKG_VER>+<BUILD_NUM>
    export PYPI_VER="${PKG_VER}.dev${BUILD_NUM}"
fi

# Print values for debugging in logs
echo "PKG_VER=$PKG_VER"
echo "BUILD_NUM=$BUILD_NUM"
echo "PYPI_VER=$PYPI_VER"

# Export values as environment variables
echo "PKG_VER=$PKG_VER" >> $GITHUB_ENV
echo "BUILD_NUM=$BUILD_NUM" >> $GITHUB_ENV
echo "PYPI_VER=$PYPI_VER" >> $GITHUB_ENV

# set GitHub Actions output variables for use in other jobs
{
  echo "PKG_VER=$PKG_VER"
  echo "BUILD_NUM=$BUILD_NUM"
  echo "PYPI_VER=$PYPI_VER"
} >> $GITHUB_OUTPUT
