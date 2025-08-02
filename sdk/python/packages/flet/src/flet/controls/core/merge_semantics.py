from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control

__all__ = ["MergeSemantics"]


@control("MergeSemantics")
class MergeSemantics(Control):
    """
    A control that merges the semantics of its descendants.

    Causes all the semantics of the subtree rooted at this node to be merged into one 
    node in the semantics tree.

    Used by accessibility tools, search engines, and other semantic analysis software 
    to determine the meaning of the application.
    """

    content: Optional[Control] = None
    """
    The `Control` to annotate.
    """
