from injector import Injector, Module, provider, singleton

from app.core.database import get_database

from app.providers.dummyjson import DummyJSONProvider
from app.repositories.lead import LeadRepository
from app.services.lead import LeadService

class AppModule(Module):
    @singleton
    @provider
    def provide_database(self):
        return get_database()

    @singleton
    @provider
    def provide_lead_repository(self, db):
        return LeadRepository(db)

    @singleton
    @provider
    def provide_dummyjson_provider(self):
        return DummyJSONProvider()
    
    @singleton
    @provider
    def provide_lead_service(self, repo: LeadRepository, dummy_provider: DummyJSONProvider):
        return LeadService(repo, dummy_provider)

container = Injector([AppModule()])