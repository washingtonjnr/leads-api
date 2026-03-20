from app.agents import get_agent

def build_prompt(title: str, description: str) -> str:
    try:
        with open("docs/ARCHITECTURE.md", "r") as f:
            architecture = f.read()
        arch_section = f"\n## Project Architecture\n{architecture}\n"
    except FileNotFoundError:
        arch_section = ""

    return f"""
        You are a software engineer executing a task from a Jira ticket.
        {arch_section}
        ## Task Title
        {title}

        ## Task Description
        {description}

        Read the codebase, understand the context, and implement the requested changes.
    """.strip()


async def build_task(title: str, description: str) -> dict:
    agent = get_agent()
    
    return await agent.build_task(build_prompt(title, description))
