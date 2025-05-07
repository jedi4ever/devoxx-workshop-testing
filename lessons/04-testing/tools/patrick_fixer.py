# weather_server.py
from typing import List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Code Fixer")

@mcp.tool(name="anonimize_names")
def fix(code: str) -> str:
    """Good at anonymizing names in code to nobody"""
    
    corrected_code = code.replace("patrick", "nobody")
    return corrected_code

@mcp.prompt()
def linter_prompt(code: str) -> str:
    """Prompt good for linting code"""
    return "You are an amazing Patrick linter. Please correct the following code: {code} \n\n" \
           "Please only return the corrected code without any additional text."

if __name__ == "__main__":
    mcp.run(transport="stdio")