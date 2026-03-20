from app.providers.jira import JiraProvider
from app.schemas.jira.webhook_payload import JiraWebhookPayload

from app.utils.parser import parse_jira_description

TODO_COLUMN = "To-do"

class JiraService:
    def __init__(self, provider: JiraProvider):
        self.provider = provider

    async def process_webhook(self, payload: JiraWebhookPayload) -> dict:
        if payload.webhookEvent not in ("jira:issue_updated", "jira:issue_created"):
            return { "status": "ignored" }

        if not payload.issue:
            return { "status": "ignored" }

        moved_to_todo = (
            payload.changelog
            and any(
                item.field == "status" and item.toString == TODO_COLUMN
                for item in payload.changelog.items
            )
        )

        if not moved_to_todo:
            return { "status": "not_todo" } 

        await self._process_card(payload.issue.key)

        return {"status": "job_dispatched", "issue": payload.issue.key}

    async def _process_card(self, issue_key: str) -> None:
        issue = await self.provider.get_issue(issue_key)

        if not issue:
            return

        fields = issue["fields"]
        description = parse_jira_description(fields.get("description") or {})

        print(f"[jira] summary: {fields['summary']}")
        print(f"[jira] description:\n{description}")

        