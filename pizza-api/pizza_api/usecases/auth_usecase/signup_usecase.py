from pizza_api.repository.interface.auth_repo import IAuthRepo
from pizza_api.entity.schemas import SignUpModel


class SignUpUsecase:
    def __init__(self, repo: IAuthRepo):
        self.repo = repo
        
    async def execute(self, model:SignUpModel):
        
        data = await self.repo.signup(user=model)
        
        return data
    