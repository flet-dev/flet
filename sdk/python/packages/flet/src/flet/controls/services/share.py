from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from flet.controls.base_control import control
from flet.controls.services.service import Service
from flet.controls.transform import Offset
from flet.utils.from_dict import from_dict

__all__ = [
    "Share",
    "ShareCupertinoActivityType",
    "ShareFile",
    "ShareResult",
    "ShareResultStatus",
]


class ShareResultStatus(Enum):
    """Outcome of a share operation."""

    SUCCESS = "success"
    """The user selected an action."""

    DISMISSED = "dismissed"
    """The user dismissed the share sheet."""

    UNAVAILABLE = "unavailable"
    """Platform cannot report a definite result."""


class ShareCupertinoActivityType(Enum):
    """iOS/macOS activity types that can be excluded from the share sheet."""

    POST_TO_FACEBOOK = "postToFacebook"
    """Share to Facebook."""

    POST_TO_TWITTER = "postToTwitter"
    """Share to Twitter."""

    POST_TO_WEIBO = "postToWeibo"
    """Share to Weibo."""

    MESSAGE = "message"
    """Share via Messages."""

    MAIL = "mail"
    """Share via Mail."""

    PRINT = "print"
    """Send to printer."""

    COPY_TO_PASTEBOARD = "copyToPasteboard"
    """Copy to clipboard."""

    ASSIGN_TO_CONTACT = "assignToContact"
    """Assign to contact."""

    SAVE_TO_CAMERA_ROLL = "saveToCameraRoll"
    """Save to camera roll."""

    ADD_TO_READING_LIST = "addToReadingList"
    """Add to reading list."""

    POST_TO_FLICKR = "postToFlickr"
    """Post to Flickr."""

    POST_TO_VIMEO = "postToVimeo"
    """Post to Vimeo."""

    POST_TO_TENCENT_WEIBO = "postToTencentWeibo"
    """Post to Tencent Weibo."""

    AIR_DROP = "airDrop"
    """AirDrop."""

    OPEN_IN_IBOOKS = "openInIBooks"
    """Open in iBooks."""

    MARKUP_AS_PDF = "markupAsPDF"
    """Markup as PDF."""

    SHARE_PLAY = "sharePlay"
    """SharePlay."""

    COLLABORATION_INVITE_WITH_LINK = "collaborationInviteWithLink"
    """Collaboration invite with link."""

    COLLABORATION_COPY_LINK = "collaborationCopyLink"
    """Collaboration copy link."""

    ADD_TO_HOME_SCREEN = "addToHomeScreen"
    """Add to home screen."""


@dataclass
class ShareResult:
    """Result returned from the native share sheet."""

    status: ShareResultStatus
    """The outcome of the share operation."""
    raw: str
    """The raw string result from the platform."""


@dataclass
class ShareFile:
    """Represents a file to share, either from disk or in-memory bytes."""

    path: Optional[str] = None
    """Filesystem path to the file to share."""

    data: Optional[bytes] = None
    """Raw bytes of the file to share."""

    mime_type: Optional[str] = None
    """MIME type of the file."""

    name: Optional[str] = None
    """Optional name of the file."""

    def __post_init__(self):
        if self.path is None and self.data is None:
            raise ValueError("Either 'path' or 'data' must be provided.")

    @staticmethod
    def from_path(path: str, *, name: Optional[str] = None) -> "ShareFile":
        """
        Create ShareFile from a filesystem path.

        Args:
            path: Filesystem path to the file.
            name: Optional name of the file.
        """
        return ShareFile(path=path, name=name)

    @staticmethod
    def from_bytes(
        data: bytes, *, mime_type: Optional[str] = None, name: Optional[str] = None
    ) -> "ShareFile":
        """
        Create ShareFile from raw bytes.

        Args:
            data: Raw bytes of the file.
            mime_type: Optional MIME type of the file.
            name: Optional name of the file.
        """
        return ShareFile(data=data, mime_type=mime_type, name=name)


@dataclass
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
        excluded_cupertino_activities: Optional[
            Iterable[ShareCupertinoActivityType]
        ] = None,
    ) -> ShareResult:
        """
        Share plain text with optional subject, title, and thumbnail.

        Args:
            text: The text to share.
            title: Optional title for the share sheet.
            subject: Optional subject for the shared text.
            preview_thumbnail: Optional thumbnail file to show in the share sheet.
            share_position_origin: Optional position origin for the share sheet.
            download_fallback_enabled: Whether to enable download fallback.
            mail_to_fallback_enabled: Whether to enable mailto fallback.
            excluded_cupertino_activities: Optional list of iOS/macOS activities
                to exclude.
        """

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
        excluded_cupertino_activities: Optional[
            Iterable[ShareCupertinoActivityType]
        ] = None,
    ) -> ShareResult:
        """
        Share a link/URI.

        Args:
            uri: The URI to share.
            share_position_origin: Optional position origin for the share sheet.
            excluded_cupertino_activities: Optional list of iOS/macOS activities
                to exclude.
        """

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
        excluded_cupertino_activities: Optional[
            Iterable[ShareCupertinoActivityType]
        ] = None,
    ) -> ShareResult:
        """
        Share one or more files with optional text/metadata.

        Args:
            files: List of ShareFile instances to share.
            title: Optional title for the share sheet.
            text: Optional text to accompany the files.
            subject: Optional subject for the shared files.
            preview_thumbnail: Optional thumbnail file to show in the share sheet.
            share_position_origin: Optional position origin for the share sheet.
            download_fallback_enabled: Whether to enable download fallback.
            mail_to_fallback_enabled: Whether to enable mailto fallback.
            excluded_cupertino_activities: Optional list of iOS/macOS activities
                to exclude.
        """

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
    excluded_cupertino_activities: Optional[
        Iterable[ShareCupertinoActivityType]
    ] = None,
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
