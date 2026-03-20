def parse_jira_description(doc: dict) -> str:
    def parse_content(content: list) -> str:
        result = ""
        for node in content:
            node_type = node.get("type")

            if node_type == "text":
                text = node.get("text", "")
                marks = [m["type"] for m in node.get("marks", [])]
                if "strong" in marks:
                    text = f"**{text}**"
                if "em" in marks:
                    text = f"_{text}_"
                if "strike" in marks:
                    text = f"~~{text}~~"
                if "code" in marks:
                    text = f"`{text}`"
                if "underline" in marks:
                    text = f"<u>{text}</u>"
                result += text

            elif node_type == "hardBreak":
                result += "\n"

            elif node_type == "paragraph":
                inner = parse_content(node.get("content", []))
                if inner.strip():
                    result += inner + "\n"

            elif node_type == "heading":
                level = node.get("attrs", {}).get("level", 1)
                prefix = "#" * level
                result += f"{prefix} {parse_content(node.get('content', [])).strip()}\n"

            elif node_type == "bulletList":
                for item in node.get("content", []):
                    result += "• " + parse_content(item.get("content", [])).strip() + "\n"

            elif node_type == "orderedList":
                for i, item in enumerate(node.get("content", []), start=1):
                    result += f"{i}. " + parse_content(item.get("content", [])).strip() + "\n"

            elif node_type == "listItem":
                result += parse_content(node.get("content", []))

            elif node_type == "codeBlock":
                lang = node.get("attrs", {}).get("language", "")
                code = parse_content(node.get("content", [])).strip()
                result += f"```{lang}\n{code}\n```\n"

            elif node_type == "blockquote":
                inner = parse_content(node.get("content", [])).strip()
                result += "\n".join(f"> {line}" for line in inner.splitlines()) + "\n"

            elif node_type == "rule":
                result += "---\n"

        return result

    if not doc:
        return ""

    return parse_content(doc.get("content", [])).strip()
