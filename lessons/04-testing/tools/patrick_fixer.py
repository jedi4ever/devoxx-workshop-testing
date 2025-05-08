# weather_server.py
from typing import List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Name Anonymizer")

@mcp.tool(name="patrick_scanner")
def fix(code: str) -> str:
    """Good at fixing code that has the name patrick in it"""
    
    corrected_code = code.replace("patrick", "nobody")
    return corrected_code

@mcp.prompt()
def linter_prompt(code: str) -> str:
    """Prompt good for scanning code for names"""
    return "You are an amazing Patrick scanner. Please correct the following code: {code} \n\n" \
           "Please only return the corrected code without any additional text."

if __name__ == "__main__":
    mcp.run(transport="stdio")