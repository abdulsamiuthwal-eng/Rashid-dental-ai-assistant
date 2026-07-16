from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from backend.app.core.security import authenticate_user

router = APIRouter()


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, description="Clinic admin username")
    password: str = Field(min_length=1, description="Clinic admin password")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/auth/token", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(body: LoginRequest):
    try:
        token = authenticate_user(body.username, body.password)
        return TokenResponse(access_token=token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
