import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.dependencies.lead import get_lead_service 

pytest_plugins = [
    "tests.fixtures.collection",
    "tests.fixtures.db",
    "tests.fixtures.lead",
]

@pytest.fixture
def app(lead_service):
    app = create_app()
    
    app.dependency_overrides[get_lead_service] = lambda: lead_service
    
    return app

@pytest.fixture
def client(app):
    with TestClient(app) as client:
        yield client
    
    app.dependency_overrides.clear()
    
@pytest.fixture
def client_no_mock():
    app = create_app()
    
    with TestClient(app) as client:
        yield client