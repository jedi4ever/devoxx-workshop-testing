# weather_server.py
from typing import List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Vulnerability fixer")

@mcp.tool(name="vulnerability_scanner")
def patrick_fixer(code: str) -> str:
    """Good at fixing code that has the name patrick in it"""
    
    corrected_code = code.replace("patrick", "nobody")
    return corrected_code

if __name__ == "__main__":
    mcp.run(transport="stdio")