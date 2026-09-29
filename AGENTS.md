# AGENTS.md

This repository owns configuration layering for UltraRAG-derived MCP servers. It is not an MCP server and must not acquire storage, retrieval, or server behavior of its own.

## Boundaries

- Keep the package independent of FastMCP, of any consuming server, and of every retrieval, storage, and model library.
- Take the registry from the caller. A key table, a `default.toml`, a key vocabulary, and the names a server resolves its paths by all belong to the caller, and nothing here may hold one.
- Keep `Setting.layer` a plain string. A shared enum would put one caller's classification into another.
- Keep the three path helpers taking the caller's own directory and file names. Hardcoding an account directory, a project state directory, or a default file name is the first way this goes wrong.
- Keep one coercion path for every layer, so a value written in a file and the same value written in the environment or after `--set` are read one way and refused one way.
- Never open a corpus, an index, a memory, or any other server's private state, and never import a domain type to describe one.
- Never add a hook a caller must subclass, or a base class a caller must inherit, to get its layer. Two callers with different needs are served by the arguments, not by a new abstract method.
- Retain the UltraRAG credit and independent-project disclaimer in `README.md` and `NOTICE`.

## Public package contract

- `LAYER_DEFAULT`, `LAYER_USER`, `LAYER_PROJECT`, `LAYER_FILE`, `LAYER_ENVIRONMENT`, and `LAYER_COMMAND_LINE` are the layer names, lowest precedence first, and are the strings provenance reports.
- `Setting` is one tunable: `key`, `field`, `kind`, `layer`, `doc`, and the optional `minimum`, `maximum`, `choices`, `env`, `empty`, and `normalize_case`. `Setting.coerce(raw, *, source)` is the single conversion every layer goes through, and every message it raises names the key and the layer.
- `SettingsSources` is where the file layers are: `default_file`, `user_config`, `project_root`, and `project_config`. A layer set to `None` is a layer this caller does not have, and a path that does not exist is a layer nobody wrote.
- `read_config_document(path, *, source)` reads one TOML layer and refuses a symlink, a missing file, malformed TOML, and anything that is not a table.
- `merge_settings(base, overlay, registry, *, source, prefix="")` merges one layer per key and returns the keys it set. A key the registry does not declare is an error, and so is a table where the registry declares a single setting.
- `environment_settings(environ, registry)` returns the environment layer as `key -> (raw value, variable name)`, from the `env` each setting declares rather than from a naming rule this package would own.
- `override_settings(overrides, registry)` parses repeated `key=value` pairs and refuses an undeclared key.
- `resolve_settings(registry, sources, *, config_path, overrides, environ)` returns the values keyed by `field` and the provenance keyed by `key`, and reads nothing relative to the working directory.
- `describe_settings(registry, values, provenance)` prints every key under the section its name begins with, in registry order, with the layer that supplied it.
- `user_config_path(app_name)`, `project_config_path(project_root, relative)`, and `default_config_path(module_file)` resolve the three file layers from names the caller passes.

Changing operation names, payloads, callable names, or public signatures is an API change. Preserve compatibility or release a new major version. A new optional field on `Setting` defaults to what an existing caller already declares, so a pinned server keeps working against a newer commit.

## Validation

Before committing:

```bash
uv lock --check
uv run ruff format --check .
uv run ruff check .
uv run pytest -q
uv run python -m compileall -q src tests
uv build
```

Tests must cover the layer order, a layer naming only what it changes, an undeclared key refused, an out-of-range value refused by name, a string layer and a file layer read identically, an empty string meaning something only where it is declared, a refused symlink, missing file, and malformed document, the printed report, a registry with a vocabulary that is neither server's, and the import boundary this file states.
