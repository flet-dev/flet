import os
from datetime import datetime
from typing import Optional

from anyio import open_file
from fastapi import Request
from flet_runtime.uploads import build_upload_query_string, get_upload_signature


class FletUpload:
    def __init__(self, upload_dir: str, max_upload_size: Optional[int] = None) -> None:
        self.__upload_dir = os.path.realpath(upload_dir)
        self.__max_upload_size = max_upload_size

    async def handle(self, request: Request):
        file_name = request.query_params["f"]
        expire_str = request.query_params["e"]
        signature = request.query_params["s"]
        print(request.url.path)

        if not file_name or not expire_str or not signature:
            raise Exception("All parameters must be provided")

        # verify signature
        query_string = build_upload_query_string(file_name, expire_str)
        if get_upload_signature(request.url.path, query_string) != signature:
            raise Exception("Invalid signature")

        # check expiration date
        expires = datetime.fromisoformat(expire_str)
        if datetime.utcnow() >= expires:
            raise Exception("Upload URL has expired")

        # build/validate dest path
        joined_path = os.path.join(self.__upload_dir, file_name)
        full_path = os.path.realpath(joined_path)
        if os.path.commonpath([full_path, self.__upload_dir]) != self.__upload_dir:
            raise Exception("Upload path is outside of upload directory")

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
