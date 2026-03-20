import httpx
from typing import Any

from app.core.config import settings

class JiraProvider:
    def __init__(self):
        self.base_url = settings.jira_url
        self.timeout = settings.jira_timeout
        self.auth = (settings.jira_email, settings.jira_api_token)

    async def get_issue(self, issue_key: str) -> dict[str, Any] | None:
        try:
            url = f"{self.base_url}/rest/api/3/issue/{issue_key}"

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, auth=self.auth)
                
                response.raise_for_status()
                
                return response.json()
        except Exception as e:
            print(f"[jira] error fetching issue {issue_key}: {e}")
            
            return None
