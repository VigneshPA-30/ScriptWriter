from agents.mcp import MCPServerStdio

playwright_srv = MCPServerStdio(
            params={
                "command": "npx",
                "args": [
                    "-y", "@playwright/mcp@latest",
                    "--browser=chromium",
                    "--config", "playwright.mcp.config.json",
                     "--isolated" # note “install”
                ],
            },
            client_session_timeout_seconds=120,
)
