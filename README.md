# config-ultra-rag-mcp

Layered, file-backed settings for document-oriented and memory-oriented MCP servers built around UltraRAG.

The library owns one thing: the stack of configuration layers a server resolves before it does any work. A server declares which tunables it has, ships a `default.toml` with their values, and gets the overrides that apply, with the layer each value came from.

This package is configuration machinery, not an MCP server and not a knowledge base. Installing it alone exposes no tools, ingests nothing, and reads no corpus.

The `mcp` in the name identifies the ecosystem it is designed to consume; it does not mean this package implements an MCP server.

## The layers

Later layers win **per key**, so a layer names only what it changes and everything else is inherited:

```text
default.toml  <  user config  <  project config  <  --config  <  environment  <  --set
```

A value written in a file and the same value written in the environment arrive as different Python types — a TOML integer and a string — and both go through one coercion, so they are read the same way and refused the same way. A key the caller's registry does not declare is an error in every layer, so a typo is refused rather than ignored. Every effective value reports the layer that supplied it, so a `--print-config` says where a number came from rather than only what it is.

## How a server uses it

Pin the dependency by commit:

```toml
dependencies = [
  "config-ultra-rag-mcp @ git+https://github.com/AhmedKishki/config-ultra-rag-mcp.git@COMMIT",
]
```

Declare the registry:

```python
from config_ultra_rag_mcp import Setting, SettingsSources, resolve_settings

SETTINGS = (
    Setting(
        key="runtime.log_level",
        field="log_level",
        kind=str,
        layer="runtime",
        doc="Verbosity of this process's own logging.",
        choices=("debug", "info", "warn", "error"),
        normalize_case=True,
        env="EXAMPLE_LOG_LEVEL",
    ),
)
```

Resolve the layers, and build the server's own settings object from the values:

```python
values, provenance = resolve_settings(
    SETTINGS,
    SettingsSources(
        default_file=default_config_path(__file__),
        user_config=user_config_path("example-ultra-rag-mcp"),
        project_root=project_root,
        project_config=project_config_path(
            project_root, Path(".example-rag/config.toml")
        ),
    ),
    config_path=config_path,
    overrides=overrides,
)
settings = EffectiveSettings.from_values(values)
```

Everything domain-shaped stays with the server: the registry, the `default.toml` that ships beside it, the `EffectiveSettings` dataclass its own code reads, the path names it resolves, and the error type its own callers catch. Two servers that classify their settings differently share this machinery without either one imposing its classification on the other, because `layer` is a plain string the caller supplies.

## What it provides

- one registry type, with type, bounds, choices, an environment variable name, and an empty-string meaning where a setting declares one;
- a layer stack that merges per key, refuses an undeclared key, and records where each value came from;
- one coercion path shared by every layer;
- three path helpers that take the caller's own account, project, and package names;
- a printed report that groups keys by section and names the layer that supplied each; and
- one dependency, `platformdirs`, and no dependency on FastMCP, UltraRAG internals, or any retrieval or storage library.

## Development

```bash
git clone https://github.com/AhmedKishki/config-ultra-rag-mcp.git
cd config-ultra-rag-mcp
uv sync --frozen
uv run pytest -q
uv run ruff check .
```

## UltraRAG credit

This independent companion library is designed for MCP servers built around [`OpenBMB/UltraRAG`](https://github.com/OpenBMB/UltraRAG). UltraRAG is a joint project of THUNLP, NEUIR, OpenBMB, AI9stars, and its contributors and is licensed under Apache-2.0. This repository is not an official UltraRAG release and does not imply endorsement. See [`NOTICE`](NOTICE).
