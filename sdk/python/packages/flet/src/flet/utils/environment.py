import os
from collections.abc import Mapping
from typing import Optional

# Variables through which a host interpreter's configuration reaches any Python
# started underneath it. `PYTHONNOUSERSITE` is absent on purpose: user
# site-packages is opt-out, so it has to be *set* rather than removed.
_HOST_PYTHON_CONFIG_VARS = ("PYTHONPATH", "PYTHONHOME", "PYTHONEXECUTABLE")


def without_host_python_config(
    env: Optional[Mapping[str, str]] = None,
) -> dict[str, str]:
    """
    Copy `env` (defaults to `os.environ`) with this process's Python
    configuration removed, for handing to a child that embeds its own
    interpreter.

    An embedded interpreter reads `PYTHONPATH`/`PYTHONHOME` at initialization,
    so anything the host has on them - notably the debugger and
    `sitecustomize` paths an IDE injects, PyCharm being the usual source -
    lands on the child's `sys.path` and is imported at its startup, where those
    modules do not belong and typically kill it. `PYTHONEXECUTABLE` is dropped
    for the same reason: macOS framework builds use it to seed
    `sys.executable`, and the host's value points at the host's interpreter.

    `PYTHONNOUSERSITE` is set rather than removed, because user site-packages
    is opt-out: leaving it unset lets a host `~/.local/lib/pythonX.Y/site-packages`
    whose version happens to match the embedded interpreter's leak in the same
    way.

    Every other variable is preserved.
    """
    result = dict(os.environ if env is None else env)
    for name in _HOST_PYTHON_CONFIG_VARS:
        result.pop(name, None)
    result["PYTHONNOUSERSITE"] = "1"
    return result
