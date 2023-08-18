import logging
import os
import sys
import urllib.parse
from datetime import datetime, timedelta
from hashlib import sha256
from typing import Optional

import flet_runtime

logger = logging.getLogger(flet_runtime.__name__)


def build_upload_url(
    upload_endpoint_path: str,
    file_name: str,
    expires_in_seconds: int,
    secret_key: Optional[str],
):
    expire_str = (datetime.utcnow() + timedelta(seconds=expires_in_seconds)).isoformat()
    query_string = build_upload_query_string(file_name, expire_str)
    signature = get_upload_signature(upload_endpoint_path, query_string, secret_key)
    return f"/{upload_endpoint_path.strip('/')}?{query_string}&s={signature}"


def build_upload_query_string(file_name: str, expire_str: str):
    return urllib.parse.urlencode({"f": file_name, "e": expire_str})


def get_upload_signature(
    upload_endpoint_path: str, query_string: str, secret_key: Optional[str]
):
    env_secret_key = os.getenv("FLET_SECRET_KEY")
    if env_secret_key:
        secret_key = env_secret_key
    if not secret_key:
        raise Exception(
            "Specify secret_key parameter or set FLET_SECRET_KEY environment variable to enable uploads."
        )
    return sha256(
        f"{upload_endpoint_path.strip('/')}{query_string}{secret_key}".encode("utf-8")
    ).hexdigest()
