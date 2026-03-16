from app.services.lead import LeadService
from app.repositories.lead import LeadRepository

from app.core.database import get_database
from app.dependencies.dummy import get_dummy_provider

def get_lead_repository():
    db = get_database()
    return LeadRepository(db)

def get_lead_service():
    repo = get_lead_repository()
    provider = get_dummy_provider() 
    
    return LeadService(repo, provider)