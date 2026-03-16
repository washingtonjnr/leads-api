from fastapi import HTTPException, status
from typing import Type

from app.models.lead import Lead
from app.services.base import BaseService
from app.repositories.lead import LeadRepository

from app.providers.dummyjson import DummyJSONProvider

from app.schemas.lead.lead_response import LeadResponse
from app.schemas.lead.lead_request import LeadCreateSchema

class LeadService(BaseService[Lead, LeadResponse]):
    def __init__(self, repository: LeadRepository, dummy_provider: DummyJSONProvider):
        super().__init__(repository)
        self.dummy_provider = dummy_provider
    
    @property
    def response_class(self) -> Type[LeadResponse]:
        return LeadResponse
    
    async def create(self, data: LeadCreateSchema) -> LeadResponse:
        is_existing = await self.repository.get_by_email(data.email)
        
        if is_existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        lead = await self.repository.create(data)

        if lead.id:
            dummy_user = await self.dummy_provider.get_user(user_id=lead.id)
            
            if dummy_user and dummy_user.birthDate:
                data_dict = {"birth_date": dummy_user.birthDate}

                lead = await self.repository.update(str(lead.id), data_dict)

        return self._to_response(lead)