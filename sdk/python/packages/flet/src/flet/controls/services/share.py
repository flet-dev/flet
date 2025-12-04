from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from flet.controls.base_control import control
from flet.controls.services.service import Service
from flet.controls.transform import Offset
from flet.utils.from_dict import from_dict

__all__ = [
    "CupertinoActivityType",
    "Share",
    "ShareFile",
    "ShareResult",
    "ShareResultStatus",
]


class ShareResultStatus(Enum):
    SUCCESS = "success"
    DISMISSED = "dismissed"
    UNAVAILABLE = "unavailable"


class CupertinoActivityType(Enum):
    POST_TO_FACEBOOK = "postToFacebook"
    POST_TO_TWITTER = "postToTwitter"
    POST_TO_WEIBO = "postToWeibo"
    MESSAGE = "message"
    MAIL = "mail"
    PRINT = "print"
    COPY_TO_PASTEBOARD = "copyToPasteboard"
    ASSIGN_TO_CONTACT = "assignToContact"
    SAVE_TO_CAMERA_ROLL = "saveToCameraRoll"
    ADD_TO_READING_LIST = "addToReadingList"
    POST_TO_FLICKR = "postToFlickr"
    POST_TO_VIMEO = "postToVimeo"
    POST_TO_TENCENT_WEIBO = "postToTencentWeibo"
    AIR_DROP = "airDrop"
    OPEN_IN_IBOOKS = "openInIBooks"
    MARKUP_AS_PDF = "markupAsPDF"
    SHARE_PLAY = "sharePlay"
    COLLABORATION_INVITE_WITH_LINK = "collaborationInviteWithLink"
    COLLABORATION_COPY_LINK = "collaborationCopyLink"
    ADD_TO_HOME_SCREEN = "addToHomeScreen"


@dataclass
class ShareResult:
    status: ShareResultStatus
    raw: str


@dataclass
class ShareFile:
    path: Optional[str] = None
    data: Optional[bytes] = None
    mime_type: Optional[str] = None
    name: Optional[str] = None

    def __post_init__(self):
        if self.path is None and self.data is None:
            raise ValueError("Either 'path' or 'data' must be provided.")

    @staticmethod
    def from_path(path: str, *, name: Optional[str] = None) -> "ShareFile":
        return ShareFile(path=path, name=name)

    @staticmethod
    def from_bytes(
        data: bytes, *, mime_type: Optional[str] = None, name: Optional[str] = None
    ) -> "ShareFile":
        return ShareFile(data=data, mime_type=mime_type, name=name)


@control("Share")
class Share(Service):
    """
    Shares text, links, or files using the platform share sheet.
    """

    async def share_text(
        self,
        text: str,
        *,
        title: Optional[str] = None,
        subject: Optional[str] = None,
        preview_thumbnail: Optional[ShareFile] = None,
        share_position_origin: Optional[Offset] = None,
        download_fallback_enabled: bool = True,
        mail_to_fallback_enabled: bool = True,
        excluded_cupertino_activities: Optional[Iterable[CupertinoActivityType]] = None,
    ) -> ShareResult:
        result = await self._invoke_method(
            "share_text",
            _share_args(
                text=text,
                title=title,
                subject=subject,
                preview_thumbnail=preview_thumbnail,
                share_position_origin=share_position_origin,
                download_fallback_enabled=download_fallback_enabled,
                mail_to_fallback_enabled=mail_to_fallback_enabled,
                excluded_cupertino_activities=excluded_cupertino_activities,
            ),
        )
        return from_dict(ShareResult, result)

    async def share_uri(
        self,
        uri: str,
        *,
        share_position_origin: Optional[Offset] = None,
        excluded_cupertino_activities: Optional[Iterable[CupertinoActivityType]] = None,
    ) -> ShareResult:
        result = await self._invoke_method(
            "share_uri",
            _share_args(
                uri=uri,
                share_position_origin=share_position_origin,
                excluded_cupertino_activities=excluded_cupertino_activities,
            ),
        )
        return from_dict(ShareResult, result)

    async def share_files(
        self,
        files: list[ShareFile],
        *,
        title: Optional[str] = None,
        text: Optional[str] = None,
        subject: Optional[str] = None,
        preview_thumbnail: Optional[ShareFile] = None,
        share_position_origin: Optional[Offset] = None,
        download_fallback_enabled: bool = True,
        mail_to_fallback_enabled: bool = True,
        excluded_cupertino_activities: Optional[Iterable[CupertinoActivityType]] = None,
    ) -> ShareResult:
        if not files:
            raise ValueError("files cannot be empty.")

        result = await self._invoke_method(
            "share_files",
            _share_args(
                files=files,
                title=title,
                text=text,
                subject=subject,
                preview_thumbnail=preview_thumbnail,
                share_position_origin=share_position_origin,
                download_fallback_enabled=download_fallback_enabled,
                mail_to_fallback_enabled=mail_to_fallback_enabled,
                excluded_cupertino_activities=excluded_cupertino_activities,
            ),
        )
        return from_dict(ShareResult, result)


def _share_args(
    *,
    text: Optional[str] = None,
    uri: Optional[str] = None,
    title: Optional[str] = None,
    subject: Optional[str] = None,
    files: Optional[list[ShareFile]] = None,
    preview_thumbnail: Optional[ShareFile] = None,
    share_position_origin: Optional[Offset] = None,
    download_fallback_enabled: bool = True,
    mail_to_fallback_enabled: bool = True,
    excluded_cupertino_activities: Optional[Iterable[CupertinoActivityType]] = None,
):
    args: dict = {}
    if text is not None:
        args["text"] = text
    if uri is not None:
        args["uri"] = uri
    if title is not None:
        args["title"] = title
    if subject is not None:
        args["subject"] = subject
    if files is not None:
        args["files"] = files
    if preview_thumbnail is not None:
        args["preview_thumbnail"] = preview_thumbnail
    if share_position_origin is not None:
        args["share_position_origin"] = {
            "x": share_position_origin.x,
            "y": share_position_origin.y,
        }
    args["download_fallback_enabled"] = download_fallback_enabled
    args["mail_to_fallback_enabled"] = mail_to_fallback_enabled

    if excluded_cupertino_activities:
        args["excluded_cupertino_activities"] = [
            a.value for a in excluded_cupertino_activities
        ]

    return args
