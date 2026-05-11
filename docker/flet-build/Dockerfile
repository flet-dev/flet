# syntax=docker/dockerfile:1.7
#
# Base image for building Flet web apps.
#
# Bakes Python + uv + Flutter SDK on PATH. No Flet CLI, no app warmup —
# downstream Dockerfiles install the Flet version they need via uv and run
# `flet build web` themselves, picking up the pre-installed Flutter
# automatically (Flet validates Flutter major.minor only and falls back to
# `shutil.which("flutter")` for discovery).
#
# Built and published manually from .github/workflows/flet-build-image.yml
# for both linux/amd64 and linux/arm64. Image: ghcr.io/flet-dev/flet-build.

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ARG TARGETARCH
ARG FLUTTER_VERSION

ENV FLUTTER_VERSION=${FLUTTER_VERSION} \
    FLUTTER_HOME=/opt/flutter \
    PATH="/opt/flutter/bin:${PATH}"

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      ca-certificates curl git unzip xz-utils zip \
 && rm -rf /var/lib/apt/lists/*

RUN git config --global --add safe.directory '*'

# linux/amd64: download prebuilt stable tarball.
# linux/arm64: clone Flutter repo at the version tag - the stable channel
# doesn't ship linux-arm64 binaries (same trick the existing Linux client CI
# uses via subosito/flutter-action's master channel,
# https://github.com/subosito/flutter-action/issues/345).
RUN set -eux; \
    mkdir -p /opt; \
    case "$TARGETARCH" in \
      amd64) \
        curl -fL "https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_${FLUTTER_VERSION}-stable.tar.xz" \
          | tar -xJ -C /opt ;; \
      arm64) \
        git clone --depth 1 --branch "${FLUTTER_VERSION}" \
          https://github.com/flutter/flutter.git /opt/flutter ;; \
      *) echo "Unsupported TARGETARCH=$TARGETARCH"; exit 1 ;; \
    esac

RUN flutter --version \
 && flutter config --no-analytics \
 && flutter precache --web \
      --no-android --no-ios --no-linux --no-windows --no-macos --no-fuchsia

WORKDIR /app
