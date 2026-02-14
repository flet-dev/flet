import hashlib
import hmac
import logging
import os
import urllib.parse
from datetime import datetime, timedelta, timezone
from typing import Optional

import flet_web

logger = logging.getLogger(flet_web.__name__)


def build_upload_url(
    upload_endpoint_path: str,
    file_name: str,
    expires_in_seconds: int,
    secret_key: Optional[str],
):
    """
    Build a signed relative upload URL for a single file upload operation.

    Args:
        upload_endpoint_path: Upload endpoint path (with or without slashes).
        file_name: File name to include in upload query.
        expires_in_seconds: Signature validity duration in seconds.
        secret_key: Signing key. Overridden by `FLET_SECRET_KEY` env var.

    Returns:
        Relative upload URL containing query parameters and HMAC signature.
    """

    expire_date = datetime.now(timezone.utc) + timedelta(seconds=expires_in_seconds)
    query_string = build_upload_query_string(file_name, expire_date)
    signature = get_upload_signature(
        upload_endpoint_path, query_string, expire_date, secret_key
    )
    return f"/{upload_endpoint_path.strip('/')}?{query_string}&s={signature}"


def build_upload_query_string(file_name: str, expire_date: datetime):
    """
    Build canonical query string used for upload URL signing.

    Args:
        file_name: File name to upload.
        expire_date: Upload expiration timestamp.

    Returns:
        URL-encoded query string with file and expiration values.
    """

    return urllib.parse.urlencode({"f": file_name, "e": expire_date.isoformat()})


def get_upload_signature(
    upload_endpoint_path: str,
    query_string: str,
    expire_date: datetime,
    secret_key: Optional[str],
):
    """
    Compute HMAC signature for upload URL validation.

    Signature derivation:
    - derive a short-lived signing key from secret and expiration timestamp;
    - sign `<normalized-endpoint><query-string>` with that signing key.

    Args:
        upload_endpoint_path: Upload endpoint path (with or without slashes).
        query_string: Canonical upload query string.
        expire_date: Expiration timestamp used in key derivation.
        secret_key: Signing key. Overridden by `FLET_SECRET_KEY` env var.

    Returns:
        Hex-encoded SHA-256 HMAC signature.

    Raises:
        RuntimeError: If no signing secret is provided.
    """

    env_secret_key = os.getenv("FLET_SECRET_KEY")
    if env_secret_key:
        secret_key = env_secret_key
    if not secret_key:
        raise RuntimeError(
            "Specify secret_key parameter or set FLET_SECRET_KEY environment "
            "variable to enable uploads."
        )
    signing_key = hmac.new(
        secret_key.encode("utf-8"),
        expire_date.isoformat().encode("utf-8"),
        hashlib.sha256,
    ).digest()
    return hmac.new(
        signing_key,
        f"{upload_endpoint_path.strip('/')}{query_string}".encode(),
        hashlib.sha256,
    ).hexdigest()
