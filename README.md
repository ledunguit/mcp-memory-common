# MCP Memory Common

Shared Pydantic models for memory leak orchestration.

This package is intended to be consumed by:

- `MCP-Vul`
- `mcp-memory-static-analysis-server`
- `mcp-dynamic-analysis-server`

The main goal is to ensure that all analyzers and the orchestrator exchange
memory-leak evidence using one stable schema.
