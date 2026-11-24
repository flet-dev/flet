---
title: "Flet MCP server"
---

`flet-mcp` is an [MCP (Model Context Protocol)](https://modelcontextprotocol.io) server
that gives LLM agents and AI coding assistants accurate, version-specific knowledge about
Flet. Instead of relying on the model's training data — which drifts out of date and leads
to hallucinated controls, properties, and enum members — the agent can look up the real
Flet API, search example projects, find icons, and inspect CLI options on demand.

This is useful both inside AI-powered editors (Claude Desktop, Cursor, VS Code, ...) and
when building your own agents that generate or refactor Flet code.

## Installation

```bash
pip install flet-mcp
```

This registers a `flet mcp` command (the `flet` CLI must be installed, which it is in any
normal Flet project). The package ships with a pre-built API index, so no extra build step
is required to start using it.

## Running the server

Start the server over the default `stdio` transport (used by most desktop AI clients):

```bash
flet mcp
```

Or expose it over HTTP:

```bash
flet mcp --transport streamable-http --port 8000
```

## Configuring an AI client

Most MCP-aware clients are configured with a small JSON snippet. For example, in Claude
Desktop's `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "flet": {
      "command": "flet",
      "args": ["mcp"]
    }
  }
}
```

Cursor, VS Code, and other clients use the same `command` / `args` shape in their
respective MCP settings.

## Tool groups

Tools are organized into groups that you toggle with `FLET_MCP_ENABLE_*` environment
variables read at server startup. The defaults focus on the hallucination-reduction
starter set — **API** and **icons** are on, everything else is off:

| Group | Variable | Default | Tools |
|---|---|---|---|
| API | `FLET_MCP_ENABLE_API` | on | `list_controls`, `get_api`, `get_enum`, `search_enum_members`, `enum_has_member` |
| Icons | `FLET_MCP_ENABLE_ICONS` | on | `find_icon` |
| Examples | `FLET_MCP_ENABLE_EXAMPLES` | off | `search_examples`, `get_example` |
| CLI | `FLET_MCP_ENABLE_CLI` | off | `get_cli_help` |

Accepted truthy values are `1`, `true`, and `yes` (case-insensitive). To enable the
example search tools, for instance:

```bash
FLET_MCP_ENABLE_EXAMPLES=1 flet mcp
```

The active groups are also surfaced in the server's startup instructions, so clients that
forward those instructions to the model keep its guidance in sync with what is actually
registered.

:::note[Documentation search]
A documentation search group (`search_docs` / `get_doc`) is planned but not yet enabled —
it is being reworked to index the current Docusaurus-based docs site.
:::

## What the tools do

| Tool | Description |
|------|-------------|
| `get_api` | The primary verifier. Look up any Flet symbol by name — control, service, dataclass type (`ButtonStyle`, `Padding`, ...), event, or enum. A "not found" result is definitive for the installed Flet version. Async methods are flagged `"async": true`, and every entry carries a `"package"` field naming the pip package it lives in (`"flet"` for core, otherwise an extension like `"flet-audio"`). |
| `list_controls` | Browse available controls and services, with optional category/kind filtering. |
| `get_enum` | Get an enum's members. |
| `search_enum_members` | Search large enums (`Icons`, `CupertinoIcons`) by substring. |
| `enum_has_member` | Verify a specific enum member exists before using it. |
| `find_icon` | Search Material and Cupertino icons by keyword, with synonym matching (e.g. "user" finds `account_circle`). |
| `search_examples` | Search Flet example projects by keyword, optionally filtered by platform. |
| `get_example` | Fetch the full source and metadata for an example returned by `search_examples`. |
| `get_cli_help` | Get structured help for the `flet` CLI commands and their options. |

## Using Flet MCP from your own agent

The server is also importable as a [FastMCP](https://gofastmcp.com) instance, so a custom
agent can consume it directly.

With [Pydantic AI](https://ai.pydantic.dev):

```python
from pydantic_ai import Agent
from pydantic_ai.toolsets import MCPToolset
from flet_mcp import mcp

agent = Agent("anthropic:claude-sonnet-4-6", toolsets=[MCPToolset(mcp)])
result = agent.run_sync("Create a Flet app with a login form")
```

Or in-process via a FastMCP client — no subprocess, no transport. Set the
`FLET_MCP_ENABLE_*` variables before importing `flet_mcp` so the desired tool groups
register; the client deserializes structured results onto `.data`:

```python
import asyncio
from fastmcp import Client
from flet_mcp import mcp

async def main():
    async with Client(mcp) as client:
        api = (await client.call_tool("get_api", {"name": "TextField"})).data
        print(api["kind"], api["package"], len(api["properties"]))

asyncio.run(main())
```
