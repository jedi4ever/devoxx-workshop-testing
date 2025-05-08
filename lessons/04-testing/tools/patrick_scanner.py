# math_server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Vulnerability Scanner")

@mcp.tool(name="vulnerability_scanner")
def patrick_scanner(code: str) -> bool:
    """Scans code for name vulnerabilities. It will tell if it is vulnerable."""

    if ("patrick" in code.lower()):
        return True
    else:
        return False

if __name__ == "__main__":
    mcp.run(transport="stdio")