from pydantic import BaseModel, Field


class JiraStatus(BaseModel):
    name: str


class JiraFields(BaseModel):
    summary: str | None = None
    status: JiraStatus | None = None


class JiraIssue(BaseModel):
    key: str
    fields: JiraFields = Field(default_factory=JiraFields)


class JiraChangelogItem(BaseModel):
    field: str
    fromString: str | None = None
    toString: str | None = None


class JiraChangelog(BaseModel):
    items: list[JiraChangelogItem] = []


class JiraWebhookPayload(BaseModel):
    webhookEvent: str
    issue: JiraIssue | None = None
    changelog: JiraChangelog | None = None
