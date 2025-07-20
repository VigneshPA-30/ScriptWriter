from agents.lifecycle import RunHooksBase # or AssistantAgent, depending on your setup
import asyncio

class DelayHook(RunHooksBase):
    async def on_tool_start(self, context, agent, tool):
        print("Tool call paused for 500ms")
        print(50*"#")
        await asyncio.sleep(0.5)


complete_automatic = True
user_niche = "Best AI Startups"