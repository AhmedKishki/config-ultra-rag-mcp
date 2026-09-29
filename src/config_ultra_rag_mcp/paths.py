"""Where each layer lives, named by the caller.

Two servers sharing this machinery do not agree on any of the three names: an
account directory of `research-ultra-rag-mcp` and a project file under
`.research-rag/config.toml` are not the ones `memory-ultra-rag-mcp` uses, and a
default file that ships inside one package is domain data that must stay in that
package. Every helper therefore takes the name it resolves, and this module
knows no server's own.
"""

from __future__ import annotations

from pathlib import Path

import platformdirs

#: The file name every account and project overlay is called.
CONFIG_FILENAME = "config.toml"

#: The file name the packaged defaults are called, in the caller's package.
DEFAULT_CONFIG_FILENAME = "default.toml"


def user_config_path(app_name: str) -> Path:
    """Return the account-wide overlay path for this platform.

    `app_name` is the caller's own account directory name, because two servers
    on one machine keep two accounts' configurations apart and neither may name
    the other's.
    """

    return platformdirs.user_config_path(app_name) / CONFIG_FILENAME


def project_config_path(project_root: str | Path, relative: str | Path) -> Path:
    """Return the project overlay, placed by the caller's own state directory.

    `relative` is the caller's path inside its project, such as
    `.memory-rag/config.toml`, so the overlay travels with the project it
    configures.
    """

    return Path(project_root) / relative


def default_config_path(module_file: str | Path) -> Path:
    """Return the packaged default file beside the caller's own module.

    `module_file` is that module's `__file__`. The default file is the caller's
    data and ships inside the caller's package, never in this one.
    """

    return Path(module_file).with_name(DEFAULT_CONFIG_FILENAME)
