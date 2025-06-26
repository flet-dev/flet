from flet.utils.browser import open_in_browser
from flet.utils.classproperty import classproperty
from flet.utils.deprecated import deprecated, deprecated_class, deprecated_warning
from flet.utils.files import (
    cleanup_path,
    copy_tree,
    get_current_script_dir,
    is_within_directory,
    safe_tar_extractall,
    which,
)
from flet.utils.from_dict import from_dict
from flet.utils.hashing import calculate_file_hash, sha1
from flet.utils.json_utils import to_json
from flet.utils.network import get_free_tcp_port, get_local_ip
from flet.utils.object_model import get_param_count, patch_dataclass
from flet.utils.once import Once
from flet.utils.platform_utils import (
    get_arch,
    get_bool_env_var,
    get_platform,
    is_android,
    is_asyncio,
    is_embedded,
    is_ios,
    is_linux,
    is_linux_server,
    is_macos,
    is_mobile,
    is_pyodide,
    is_windows,
)
from flet.utils.slugify import slugify
from flet.utils.strings import random_string
from flet.utils.vector import Vector

__all__ = [
    "open_in_browser",
    "classproperty",
    "deprecated",
    "deprecated_class",
    "deprecated_warning",
    "cleanup_path",
    "copy_tree",
    "get_current_script_dir",
    "is_within_directory",
    "safe_tar_extractall",
    "which",
    "from_dict",
    "calculate_file_hash",
    "sha1",
    "to_json",
    "get_free_tcp_port",
    "get_local_ip",
    "Once",
    "patch_dataclass",
    "get_arch",
    "get_bool_env_var",
    "get_platform",
    "is_android",
    "is_asyncio",
    "is_embedded",
    "is_ios",
    "is_linux",
    "is_linux_server",
    "is_macos",
    "is_mobile",
    "is_pyodide",
    "is_windows",
    "slugify",
    "random_string",
    "Vector",
    "get_param_count",
]
