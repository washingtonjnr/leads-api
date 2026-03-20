import json
import hmac
import hashlib
from typing import Annotated

from fastapi import APIRouter, Depends, Request, HTTPException, status

from app.dependencies.jira import get_jira_service
from app.schemas.jira.webhook_payload import JiraWebhookPayload
from app.services.jira import JiraService

from app.core.config import settings

router = APIRouter(prefix="/webhook", tags=["Jira"])

def verify_signature(secret: str, body: bytes, signature: str) -> bool:
    expected = hmac.new(
        key=secret.encode("utf-8"),
        msg=body,
        digestmod=hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected, signature)

@router.post("/jira")
async def jira_webhook(
    request: Request,
    service: Annotated[JiraService, Depends(get_jira_service)],
):
    body = await request.body()
    payload = JiraWebhookPayload(**json.loads(body))

    signature = request.headers.get("X-Hub-Signature")
    
    if not signature:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing signature")

    _, received_hash = signature.split("=")
    
    is_valid_hash = verify_signature(settings.jira_webhook_secret, body, received_hash)
    
    if not is_valid_hash:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature")
    
    return await service.process_webhook(payload)
