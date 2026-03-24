from app.agents import get_agent

from app.strategies.base import BaseStrategy

def _build_review_prompt(issue_key: str, summary: str, description: str) -> str:
    return (
        f"You are doing a code review for a Jira task that is under analysis.\n\n"
        f"## Issue: {issue_key}\n"
        f"## Title: {summary}\n\n"
        f"## Description:\n{description}\n\n"
        f"Review the relevant code in this codebase for this task. Check for:\n"
        f"- Bugs or logic errors\n"
        f"- Security vulnerabilities\n"
        f"- Code quality and readability\n"
        f"- Missing edge cases\n"
        f"- Suggestions for improvement\n\n"
        f"Be specific and actionable."
    )

class CodeReviewStrategy(BaseStrategy):
    async def run(self, issue_key: str, summary: str, description: str) -> dict:
        agent = get_agent()
        
        await agent.build_task(_build_review_prompt(issue_key, summary, description))
        
        return {"status": "review_dispatched", "issue": issue_key}
