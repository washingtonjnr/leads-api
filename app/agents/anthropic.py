import glob as glob_module

from anthropic import AsyncAnthropic

from app.agents.base import BaseAgent

_TOOLS = [
    {
        "name": "read_file",
        "description": "Read the full contents of a file by path.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to the file"},
            },
            "required": ["path"],
        },
    },
    {
        "name": "edit_file",
        "description": "Replace an exact string in a file with a new string.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path":       {"type": "string", "description": "Path to the file"},
                "old_string": {"type": "string", "description": "Exact text to replace"},
                "new_string": {"type": "string", "description": "Replacement text"},
            },
            "required": ["path", "old_string", "new_string"],
        },
    },
    {
        "name": "glob_files",
        "description": "Find files matching a glob pattern.",
        "input_schema": {
            "type": "object",
            "properties": {
                "pattern": {"type": "string", "description": "Glob pattern, e.g. 'app/**/*.py'"},
            },
            "required": ["pattern"],
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

class AnthropicAgent(BaseAgent):
    def __init__(self):
        self.client = AsyncAnthropic()

    async def build_task(self, prompt: str) -> dict:
        messages = [{ "role": "user", "content": prompt }]

        while True:
            response = await self.client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=8096,
                tools=_TOOLS,
                messages=messages,
            )

            messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason != "tool_use":
                for block in response.content:
                    if hasattr(block, "text"):
                        print(block.text)
                break

            tool_results = []
            
            for block in response.content:
                if block.type != "tool_use":
                    continue
                
                result = _TOOL_HANDLERS[block.name](block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })

            messages.append({ "role": "user", "content": tool_results })

        return {}
