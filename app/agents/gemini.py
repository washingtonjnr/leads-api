import glob as glob_module

from google import genai
from google.genai import types

from app.agents.base import BaseAgent

_TOOLS = types.Tool(function_declarations=[
    types.FunctionDeclaration(
        name="read_file",
        description="Read the full contents of a file by path.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "path": types.Schema(type=types.Type.STRING, description="Path to the file"),
            },
            required=["path"],
        ),
    ),
    types.FunctionDeclaration(
        name="edit_file",
        description="Replace an exact string in a file with a new string.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "path":       types.Schema(type=types.Type.STRING, description="Path to the file"),
                "old_string": types.Schema(type=types.Type.STRING, description="Exact text to replace"),
                "new_string": types.Schema(type=types.Type.STRING, description="Replacement text"),
            },
            required=["path", "old_string", "new_string"],
        ),
    ),
    types.FunctionDeclaration(
        name="glob_files",
        description="Find files matching a glob pattern.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "pattern": types.Schema(type=types.Type.STRING, description="Glob pattern, e.g. 'app/**/*.py'"),
            },
            required=["pattern"],
        ),
    ),
])


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


class GeminiAgent(BaseAgent):
    def __init__(self):
        self.client = genai.Client()

    async def build_task(self, prompt: str) -> dict:
        contents: list = [prompt]

        while True:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=contents,
                config=types.GenerateContentConfig(tools=[_TOOLS]),
            )

            candidate = response.candidates[0]
            contents.append(candidate.content)

            tool_calls = [p for p in candidate.content.parts if p.function_call]

            if not tool_calls:
                for part in candidate.content.parts:
                    if part.text:
                        print(part.text)
                break

            tool_responses = []
            for part in tool_calls:
                fc = part.function_call
                
                result = _TOOL_HANDLERS[fc.name](dict(fc.args))
                tool_responses.append(
                    types.Part(function_response=types.FunctionResponse(
                        name=fc.name,
                        response={"result": result},
                    ))
                )

            contents.append(types.Content(role="user", parts=tool_responses))

        return {}
