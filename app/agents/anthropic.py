from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage, AssistantMessage

from app.agents.base import BaseAgent

class AnthropicAgent(BaseAgent):
    async def build_task(self, prompt: str) -> dict:
        async for message in query(
            prompt=prompt,
            options=ClaudeAgentOptions(
                allowed_tools=["Read", "Edit", "Glob"],
                permission_mode="acceptEdits",
            ),
        ):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if hasattr(block, "text"):
                        print(block.text)
                    elif hasattr(block, "name"):
                        print(f"Tool: {block.name}")
            elif isinstance(message, ResultMessage):
                print(f"Done: {message.subtype}")

        return {}
