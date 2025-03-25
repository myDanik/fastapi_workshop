import pytest
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from ..services.auth import AuthService
from ..models.auth import UserCreate
from ..tables import User as UserTable

@pytest.mark.asyncio
async def test_register_user(session):
    user_data = UserCreate(
        email="test@example.com",
        username="testuser",
        password="Testpass123!"
    )
    auth_service = AuthService(session)
    token = auth_service.register_user(user_data)
    
    assert token.access_token
    assert token.token_type == "bearer"
    
    user = session.query(UserTable).filter(UserTable.email == user_data.email).first()
    assert user is not None
    assert user.username == user_data.username

@pytest.mark.asyncio
async def test_register_duplicate_email(session):
    user_data = UserCreate(
        email="duplicate@example.com",
        username="user1",
        password="Testpass123!"
    )
    auth_service = AuthService(session)
    auth_service.register_user(user_data)
    
    with pytest.raises(IntegrityError):
        auth_service.register_user(user_data)

@pytest.mark.asyncio
async def test_authenticate_user_valid(session):
    user_data = UserCreate(
        email="auth@example.com",
        username="auth_user",
        password="ValidPass123!"
    )
    auth_service = AuthService(session)
    auth_service.register_user(user_data)
    
    token = auth_service.authenticate_user("auth_user", "ValidPass123!")
    assert token.access_token

@pytest.mark.asyncio
async def test_authenticate_user_invalid(session):
    auth_service = AuthService(session)
    with pytest.raises(HTTPException) as exc:
        auth_service.authenticate_user("wrong_user", "wrong_pass")
    assert exc.value.status_code == 401