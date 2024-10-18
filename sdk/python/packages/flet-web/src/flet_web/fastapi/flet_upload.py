import logging
import os
from datetime import datetime, timezone
from typing import Optional

import flet_web.fastapi as flet_fastapi
from anyio import open_file
from fastapi import Request
from flet_web.uploads import build_upload_query_string, get_upload_signature

logger = logging.getLogger(flet_fastapi.__name__)


class FletUpload:
    """
    Flet app uploads handler.

    Parameters:

    * `upload_dir` (str) - an absolute path to a directory with uploaded files.
    * `max_upload_size` (str, int) - maximum size of a single upload, bytes. Unlimited if `None`.
    * `secret_key` (str, optional) - secret key to sign and verify upload requests.
    """

    def __init__(
        self,
        upload_dir: str,
        max_upload_size: Optional[int] = None,
        secret_key: Optional[str] = None,
    ) -> None:
        self.__upload_dir = os.path.realpath(upload_dir)
        self.__max_upload_size = max_upload_size

        env_max_upload_size = os.getenv("FLET_MAX_UPLOAD_SIZE")
        if env_max_upload_size:
            self.__max_upload_size = int(env_max_upload_size)

        self.__secret_key = secret_key

        env_upload_secret_key = os.getenv("FLET_SECRET_KEY")
        if env_upload_secret_key:
            self.__secret_key = env_upload_secret_key

        logger.info(f"Upload path configured: {self.__upload_dir}")

    """
    Handle file upload.

    Upload must be an non-encoded (raw) file in the requst body.
    """

    async def handle(self, request: Request):
        file_name = request.query_params["f"]
        expire_str = request.query_params["e"]
        signature = request.query_params["s"]

        if not file_name or not expire_str or not signature:
            raise Exception("Invalid request")

        expire_date = datetime.fromisoformat(expire_str)

        # verify signature
        query_string = build_upload_query_string(file_name, expire_date)
        if (
            get_upload_signature(
                request.url.path, query_string, expire_date, self.__secret_key
            )
            != signature
        ):
            raise Exception("Invalid request")

        # check expiration date
        if datetime.now(timezone.utc) >= expire_date:
            raise Exception("Invalid request")

        # build/validate dest path
        joined_path = os.path.join(self.__upload_dir, file_name)
        full_path = os.path.realpath(joined_path)
        if os.path.commonpath([full_path, self.__upload_dir]) != self.__upload_dir:
            raise Exception("Invalid request")

        # create directory if not exists
        dest_dir = os.path.dirname(full_path)
        os.makedirs(dest_dir, exist_ok=True)

        # upload file
        size = 0
        async with await open_file(full_path, "wb") as f:
            async for chunk in request.stream():
                size += len(chunk)
                if self.__max_upload_size and size > self.__max_upload_size:
                    raise Exception(
                        f"Max upload size reached: {self.__max_upload_size}"
                    )
                await f.write(chunk)
