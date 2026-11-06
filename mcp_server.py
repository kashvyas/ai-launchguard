"""MCP v2 server for the AI LaunchGuard.

Requires: pip install "mcp[cli]>=2,<3"
"""
from mcp.server import MCPServer

from src.ai_launchguard.agent import LaunchGuard
from src.ai_launchguard.tools import (
    get_eval_result as _get_eval_result,
    get_feature_status as _get_feature_status,
    get_incident_status as _get_incident_status,
)

mcp = MCPServer("AI LaunchGuard")


@mcp.tool()
def get_feature_status(feature: str) -> dict:
    """Return synthetic release metadata for an AI feature."""
    return _get_feature_status(feature)


@mcp.tool()
def get_eval_result(feature: str) -> dict:
    """Return the latest synthetic golden-set evaluation result."""
    return _get_eval_result(feature)


@mcp.tool()
def get_incident_status(feature: str) -> list[dict]:
    """Return open synthetic incidents affecting an AI feature."""
    return _get_incident_status(feature)


@mcp.tool()
def assess_release(feature: str, requested_rollout_pct: int = 100) -> dict:
    """Assess whether an AI feature should ship, hold, or use a limited rollout."""
    return LaunchGuard().assess(feature, requested_rollout_pct).as_dict()


if __name__ == "__main__":
    mcp.run(transport="streamable-http", json_response=True)
