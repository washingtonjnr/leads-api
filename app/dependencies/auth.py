from app.services.auth import AuthService

from app.repositories.user import UserRepository
from app.repositories.refresh_token import RefreshTokenRepository

from app.core.database import get_database

def get_auth_service() -> AuthService:
    db = get_database()
    
    user_repo = UserRepository(db)
    token_repo = RefreshTokenRepository(db)
    
    return AuthService(user_repo, token_repo)
