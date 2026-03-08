import inspect
import warnings
from types import ModuleType

from flet.utils.deprecated import deprecated_warning


def test_deprecated_warning_points_to_user_code_through_flet_frames():
    """
    Ensure stacklevel skips internal `flet.*` frames and targets user call site.
    """

    flet_internal = ModuleType("flet.fake_internal")
    flet_internal.deprecated_warning = deprecated_warning
    exec(
        (
            "def emit_warning():\n"
            "    deprecated_warning(\n"
            "        name='Sample.old_value',\n"
            "        reason='Use new_value instead.',\n"
            "        version='0.80.0',\n"
            "    )\n"
        ),
        flet_internal.__dict__,
    )

    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always", DeprecationWarning)
        expected_line = inspect.currentframe().f_lineno + 1
        flet_internal.emit_warning()

    assert len(captured) == 1
    warning = captured[0]
    assert warning.filename == __file__
    assert warning.lineno == expected_line
