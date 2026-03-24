import httpx

from app.core.config import settings
from app.providers.jira import JiraProvider
from app.schemas.jira.webhook_payload import JiraWebhookPayload
from app.utils.parser import parse_jira_description
from app.strategies import get_strategy


class JiraService:
    def __init__(self, provider: JiraProvider):
        self.provider = provider

    async def process_webhook(self, payload: JiraWebhookPayload) -> dict:
        if payload.webhookEvent not in ("jira:issue_updated", "jira:issue_created"):
            return {"status": "ignored"}

        if not payload.issue:
            return {"status": "ignored"}

        if settings.use_n8n:
            return await self._forward_to_n8n(payload)

        return await self._handle(payload)

    async def _handle(self, payload: JiraWebhookPayload) -> dict:
        status_change = (
            payload.changelog
            and next(
                (item for item in payload.changelog.items if item.field == "status"),
                None,
            )
        )

        if not status_change:
            return {"status": "ignored"}

        strategy = get_strategy(status_change.toString)
        if not strategy:
            return {"status": "ignored"}

        issue_fields = await self._get_issue_fields(payload.issue.key)
        if not issue_fields:
            return {"status": "ignored"}

        summary, description = issue_fields
        return await strategy.run(payload.issue.key, summary, description)

    async def _forward_to_n8n(self, payload: JiraWebhookPayload) -> dict:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                settings.n8n_webhook_url,
                json=payload.model_dump(),
            )
        return {"status": "forwarded_to_n8n", "n8n_status": response.status_code}

    async def _get_issue_fields(self, issue_key: str) -> tuple[str, str] | None:
        issue = await self.provider.get_issue(issue_key)
        if not issue:
            return None
        fields = issue["fields"]
        description = parse_jira_description(fields.get("description") or {})
        return fields["summary"], description
