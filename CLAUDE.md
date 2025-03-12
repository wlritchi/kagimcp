# CLAUDE.md - Project Guidelines

## Build & Dev Commands
- Setup: `uv venv && source .venv/bin/activate && uv sync`
- Run locally: `uv run kagimcp`
- Debug: `npx @modelcontextprotocol/inspector uvx kagimcp`
- Set log level: `FASTMCP_LOG_LEVEL="ERROR" uvx kagimcp`
- Test: `uv run pytest` or `uv run pytest -v`
- Linting: `uv run ruff check .`
- Type checking: `uv run mypy src tests`

## Code Style
- Use PEP 8 style conventions
- Imports: Standard library first, then third-party, then local
- Use type hints for function parameters and return values
- Use descriptive variable names in snake_case
- Function/method names: snake_case
- Class names: PascalCase
- Exception handling: Always provide informative error messages
- Documentation: Use docstrings for classes and functions
- Line length: 88 characters max (matches Black defaults)
- Text formatting: Use f-strings for string formatting
- Exception handling: Use try/except blocks with specific exceptions

## Structure
- MCP server using FastMCP with Kagi integration
- Two main tools:
  1. `search`: Web search using Kagi Search API (requires special access)
  2. `summarize`: FastGPT summaries (available to all Kagi users)
- Environment variables:
  - `KAGI_API_KEY`: Required for all functionality
  - `KAGI_ENABLE_SEARCH`: Toggle search feature (default: true)
  - `KAGI_ENABLE_FASTGPT`: Toggle FastGPT feature (default: true)
  - `FASTMCP_LOG_LEVEL`: Control logging verbosity