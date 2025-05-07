# weather_server.py
from typing import List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Linter", settings={"port": 3000})

@mcp.tool()
async def correct(code: str) -> str:
    """A linter good at correcting patrick code syntax"""
    
    corrected_code = code.replace("patttrick", "patrick")
    return corrected_code

@mcp.prompt()
async def linter_prompt(code: str) -> str:
    """Prompt good for linting code"""
    return "You are an amazing Patrick linter. Please correct the following code: {code} \n\n" \
           "Please only return the corrected code without any additional text."

if __name__ == "__main__":
    mcp.run(transport="sse")