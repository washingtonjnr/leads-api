from app.agents import get_agent

from app.strategies.base import BaseStrategy

def _build_prompt(title: str, description: str) -> str:
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

class ImplementTaskStrategy(BaseStrategy):
    async def run(self, issue_key: str, summary: str, description: str) -> dict:
        agent = get_agent()
        
        await agent.build_task(_build_prompt(summary, description))
        
        return {"status": "job_dispatched", "issue": issue_key}
