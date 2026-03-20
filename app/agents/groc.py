import glob as glob_module
import json

from groq import AsyncGroq

from app.agents.base import BaseAgent

_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the full contents of a file by path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file"},
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "edit_file",
            "description": "Replace an exact string in a file with a new string.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path":       {"type": "string", "description": "Path to the file"},
                    "old_string": {"type": "string", "description": "Exact text to replace"},
                    "new_string": {"type": "string", "description": "Replacement text"},
                },
                "required": ["path", "old_string", "new_string"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "glob_files",
            "description": "Find files matching a glob pattern.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "Glob pattern, e.g. 'app/**/*.py'"},
                },
                "required": ["pattern"],
            },
        },
    },
]

def _read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def _edit_file(path: str, old_string: str, new_string: str) -> str:
    content = _read_file(path)
    
    if old_string not in content:
        return f"ERROR: string not found in {path}"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.replace(old_string, new_string, 1))
        
    return f"OK: edited {path}"

def _glob_files(pattern: str) -> str:
    matches = glob_module.glob(pattern, recursive=True)
    
    return "\n".join(matches) if matches else "No files found"

_TOOL_HANDLERS = {
    "read_file":  lambda args: _read_file(args["path"]),
    "edit_file":  lambda args: _edit_file(args["path"], args["old_string"], args["new_string"]),
    "glob_files": lambda args: _glob_files(args["pattern"]),
}

class GroqAgent(BaseAgent):
    def __init__(self):
        self.client = AsyncGroq()
        self.model = "meta-llama/llama-4-scout-17b-16e-instruct"

    async def build_task(self, prompt: str) -> dict:
        messages: list = [{"role": "user", "content": prompt}]

        while True:
            response = await self.client.chat.completions.create(
                model=self.model,
                tools=_TOOLS,
                tool_choice="auto",
                parallel_tool_calls=False,
                messages=messages,
            )

            message = response.choices[0].message
            messages.append(message)

            tool_calls = message.tool_calls or []

            if not tool_calls:
                if message.content:
                    print(message.content)
                break

            for tool_call in tool_calls:
                args = json.loads(tool_call.function.arguments)
                result = _TOOL_HANDLERS[tool_call.function.name](args)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                })

        return {}