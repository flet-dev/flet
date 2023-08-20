import hashlib
import hmac
import logging
import os
import sys
import urllib.parse
from datetime import datetime, timedelta
from typing import Optional

import flet_runtime

logger = logging.getLogger(flet_runtime.__name__)


def build_upload_url(
    upload_endpoint_path: str,
    file_name: str,
    expires_in_seconds: int,
    secret_key: Optional[str],
):
    expire_date = datetime.utcnow() + timedelta(seconds=expires_in_seconds)
    query_string = build_upload_query_string(file_name, expire_date)
    signature = get_upload_signature(
        upload_endpoint_path, query_string, expire_date, secret_key
    )
    return f"/{upload_endpoint_path.strip('/')}?{query_string}&s={signature}"


def build_upload_query_string(file_name: str, expire_date: datetime):
    return urllib.parse.urlencode({"f": file_name, "e": expire_date.isoformat()})


def get_upload_signature(
    upload_endpoint_path: str,
    query_string: str,
    expire_date: datetime,
    secret_key: Optional[str],
):
    env_secret_key = os.getenv("FLET_SECRET_KEY")
    if env_secret_key:
        secret_key = env_secret_key
    if not secret_key:
        raise Exception(
            "Specify secret_key parameter or set FLET_SECRET_KEY environment variable to enable uploads."
        )
    signing_key = hmac.new(
        secret_key.encode("utf-8"),
        expire_date.isoformat().encode("utf-8"),
        hashlib.sha256,
    ).digest()
    return hmac.new(
        signing_key,
        f"{upload_endpoint_path.strip('/')}{query_string}".encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
