from flet_core.utils.classproperty import classproperty
from flet_core.utils.deprecated import deprecated
from flet_core.utils.files import (
    copy_tree,
    is_within_directory,
    safe_tar_extractall,
    which,
)
from flet_core.utils.hashing import calculate_file_hash, sha1
from flet_core.utils.once import Once
from flet_core.utils.platform_utils import (
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
from flet_core.utils.slugify import slugify
from flet_core.utils.strings import random_string
from flet_core.utils.vector import Vector
