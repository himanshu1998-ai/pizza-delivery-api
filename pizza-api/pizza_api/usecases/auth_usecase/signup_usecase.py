from pizza_api.repository.interface.auth_repo import IAuthRepo
from pizza_api.entity.schemas import SignUpModel
from fastapi_jwt_auth import AuthJWT
from fastapi import Depends

class SignUpUsecase:
    async def __init__(self, repo: IAuthRepo):
        self.repo = repo
        
    async def execute(self, model:SignUpModel, Authorize: AuthJWT = Depends()):
        
        data = await self.repo.signup(user=model, Authorize=Authorize)
        
        return data
    