"""Configuration layering for UltraRAG-derived MCP servers.

A caller declares a registry of settings, ships a packaged `default.toml`, and
resolves the layers that override it:

    default.toml  <  user config  <  project config  <  --config  <  environment  <  --set

Each later layer wins **per key** and names only what it changes, so a layer may
set one key and leave the rest inherited from the layer below. Every effective
value reports the layer that supplied it, so a caller can print where a number
came from rather than only what it is.

Three rules follow from the registry a caller passes in:

* a key the registry does not declare is an error in every layer, so a typo is
  refused rather than ignored;
* one coercion path serves every layer, so a number written in a file and the
  same number written in the environment or after `--set` are read the same way
  and fail the same way; and
* the vocabulary is the caller's. `Setting.layer` is a plain string, the path
  helpers take the caller's own directory names, and the registry itself is the
  caller's, so two servers that classify settings differently can share this
  machinery without either one imposing its own classification on the other.

This package holds the layering and nothing else: no registry of its own, no
default file, no domain type, and no caller to subclass.
"""

from config_ultra_rag_mcp.paths import (
    default_config_path,
    project_config_path,
    user_config_path,
)
from config_ultra_rag_mcp.settings import (
    LAYER_COMMAND_LINE,
    LAYER_DEFAULT,
    LAYER_ENVIRONMENT,
    LAYER_FILE,
    LAYER_PROJECT,
    LAYER_USER,
    Setting,
    SettingsError,
    SettingsSources,
    describe_settings,
    environment_settings,
    merge_settings,
    override_settings,
    read_config_document,
    resolve_settings,
)

__all__ = [
    "LAYER_COMMAND_LINE",
    "LAYER_DEFAULT",
    "LAYER_ENVIRONMENT",
    "LAYER_FILE",
    "LAYER_PROJECT",
    "LAYER_USER",
    "Setting",
    "SettingsError",
    "SettingsSources",
    "default_config_path",
    "describe_settings",
    "environment_settings",
    "merge_settings",
    "override_settings",
    "project_config_path",
    "read_config_document",
    "resolve_settings",
    "user_config_path",
]
