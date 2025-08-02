from contextvars import ContextVar
from typing import TYPE_CHECKING, Optional

from flet.utils.classproperty import classproperty

if TYPE_CHECKING:
    from flet.controls.page import Page

_context_page = ContextVar("flet_session_page", default=None)


class context:
    @classproperty
    def page(cls) -> Optional["Page"]:
        return _context_page.get()
