# math_server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Name Scanner")

@mcp.tool(name="name scanner")
def vulnerable(code: str) -> bool:
    """Scans code for name patrick"""

    if ("patrick" in code.lower()):
        return True
    else:
        return False
    
@mcp.prompt()
def scanner_prompt(code: str) -> str:
    """Prompt for scanning the code"""
    return "You are an amazing name scanner. Please scan the following code for names: {code} \n\n" \

if __name__ == "__main__":
    mcp.run(transport="stdio")