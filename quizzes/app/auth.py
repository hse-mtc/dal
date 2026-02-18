from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
import httpx
from settings import settings


class Principal(BaseModel):
    user_id: int
    permissions: list[str]
    is_superuser: bool

bearer_scheme = HTTPBearer(auto_error=True)

async def get_principal(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> Principal:
    """
    Get principal from authorization header by verifying token with Django service.
    """
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme",
        )

    token = credentials.credentials
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.auth_base_url.rstrip('/')}/api/auth/user/",
                headers={"Authorization": f"Bearer {token}"},
            )
            
            if response.status_code == 401:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired token",
                )
            elif response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Auth service is unavailable",
                )
            
            user_data = response.json()
            return Principal(
                user_id=user_data["id"],
                permissions=[perm["codename"] for perm in user_data["all_permissions"]],
                is_superuser=user_data["is_superuser"]
            )
    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to auth service",
        )


def require_permission(permission: str):
    """
    Dependency that requires a specific permission.
    """
    async def check_permission(principal: Principal = Depends(get_principal)):
        if not principal.is_superuser and not any(perm == permission for perm in principal.permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission {permission} is required",
            )
        return principal
    
    return check_permission
