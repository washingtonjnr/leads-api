from typing import Annotated
from fastapi import APIRouter, Depends

from app.services.lead import LeadService
from app.schemas.lead.lead_response import LeadResponse
from app.schemas.lead.lead_request import LeadCreateSchema
from app.schemas.pagination_response import PaginatedResponse

from app.dependencies.lead import get_lead_service
from app.dependencies.pagination import get_pagination

router = APIRouter(prefix="/leads", tags=["Leads"])

@router.get(
    "",
    response_model=PaginatedResponse[LeadResponse],
    summary="Lista de leads criados",
    description="Endpoint responsável por realizar consultas e listar os leads criados no sistema com paginação.",
)
async def list_leads(
    pagination: Annotated[LeadService, Depends(get_pagination)] = None,
    service: Annotated[LeadService, Depends(get_lead_service)] = None
):
    return await service.get_paginated(page=pagination.page, size=pagination.size)


@router.get(
    "/{id}",
    response_model=LeadResponse,
    summary="Lead por ID",
    description="Endpoint responsável por realizar consultas e listar os leads criados no sistema com paginação.",
)
async def get_lead(
    id: str,
    service: Annotated[LeadService, Depends(get_lead_service)] = None
):
    return await service.get_by_external_id(id)  

@router.post(
    "",
    response_model=LeadResponse,
    status_code=201,
    summary="Criar lead",
    description="Cria um novo lead no sistema.",
)
async def create_lead(
    data: LeadCreateSchema,
    service: Annotated[LeadService, Depends(get_lead_service)]
):
    return await service.create(data)