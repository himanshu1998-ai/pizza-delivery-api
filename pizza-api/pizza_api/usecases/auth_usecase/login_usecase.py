from pizza_api.repository.interface.auth_repo import IAuthRepo
from pizza_api.entity.schemas import LoginModel
from fastapi_jwt_auth import AuthJWT
from fastapi import Depends

class LoginUsecase:
    async def __init__(self, repo: IAuthRepo):
        self.repo = repo
        
    async def execute(self, model:LoginModel, Authorize: AuthJWT = Depends()):
        
        data = await self.repo.login(user=model, Authorize=Authorize)
        
        return data
    