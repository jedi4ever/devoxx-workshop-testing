# math_server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Security Scanner")

@mcp.tool(name="security_vulnerability_scanner")
def vulnerable(code: str) -> bool:
    """Scans code for vulnerabilities"""

    if ("patrick" in code.lower()):
        return True
    else:
        return False
    
@mcp.prompt()
def scanner_prompt(code: str) -> str:
    """Prompt for scanning the code"""
    return "You are an amazing security scanner. Please scan the following code for security vulnerabilities: {code} \n\n" \

if __name__ == "__main__":
    mcp.run(transport="stdio")