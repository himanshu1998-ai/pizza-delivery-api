from pizza_api.repository.interface.auth_repo import IAuthRepo
from fastapi_jwt_auth import AuthJWT
from fastapi import Depends

class RefreshTokenUsecase:
    async def __init__(self, repo: IAuthRepo):
        self.repo = repo
        
    async def execute(self, Authorize: AuthJWT = Depends()):
        
        data = await self.repo.refresh_token(Authorize=Authorize)
        
        return data
    