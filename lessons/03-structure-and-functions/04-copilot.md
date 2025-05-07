# Github Copilot
## Agent mode
- Now there is an `agent` mode in addition to `ask` or `edit`.

![Agent mode](copilot/agent-mode.png)


More info at :
<https://code.visualstudio.com/blogs/2025/02/24/introducing-copilot-agent-mode>

We can also enable the agent thinking mode via:
`github.copilot.chat.agent.thinkingTool`


## MCP
- You can also enable MCP services now.
- You need to select `agent` mode for this.

In the settings:
- `chat.mcp.discovery.enabled: true`
- `chat.mcp.enabled : true`

![MCP commands](copilot/mcp-palette.png)


- The configuration is saved at `.vscode\mcp.json` 
- Here's  an example configuration : one using Docker and the other using javascript.

```
{
    "servers": {
        "puppeteer-docker": {
            "command": "docker",
            "args": [
                "run",
                "-i",
                "--rm",
                "--init",
                "-e",
                "DOCKER_CONTAINER=true",
                "mcp/puppeteer"
            ]
        },
        "playwright": {
            "command": "npx",
            "env": {
                "BROWSER": "firefox",
                "headless": "true"
            },
            "args": [
                "@playwright/mcp@latest",
                "--headless"
            ]
        }
    }
}
```

## Yolo mode
To blindly accept all tools information : 
`chat.tools.autoApprove : true`

Use at your risk | fun !