import logging
import os
import sys
import urllib.parse
from datetime import datetime, timedelta
from hashlib import sha256

import flet_runtime

logger = logging.getLogger(flet_runtime.__name__)


def build_upload_url(
    upload_endpoint_path: str, file_name: str, expires_in_seconds: int
):
    expire_str = (datetime.utcnow() + timedelta(seconds=expires_in_seconds)).isoformat()
    query_string = build_upload_query_string(file_name, expire_str)
    signature = get_upload_signature(upload_endpoint_path, query_string)
    return f"/{upload_endpoint_path.strip('/')}?{query_string}&s={signature}"


def build_upload_query_string(file_name: str, expire_str: str):
    return urllib.parse.urlencode({"f": file_name, "e": expire_str})


def get_upload_signature(upload_endpoint_path: str, query_string: str):
    master_key = os.getenv("FLET_MASTER_KEY", "")
    if master_key == "":
        logger.error("Set FLET_MASTER_KEY environment variable to use hashing.")
        sys.exit(1)
    return sha256(
        f"{upload_endpoint_path.strip('/')}{query_string}{master_key}".encode("utf-8")
    ).hexdigest()
