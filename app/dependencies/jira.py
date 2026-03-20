from app.providers.jira import JiraProvider
from app.services.jira import JiraService

def get_jira_service() -> JiraService:
    return JiraService(JiraProvider())
