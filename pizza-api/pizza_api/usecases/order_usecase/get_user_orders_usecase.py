from pizza_api.repository.interface.order_repo import IOrderRepo
from fastapi_jwt_auth import AuthJWT
from fastapi import Depends

class GetUserOrderUsecase:
    async def __init__(self, repo: IOrderRepo):
        self.repo = repo
        
    async def execute(self, Authorize: AuthJWT = Depends()):
        
        data = await self.repo.get_user_orders(Authorize=Authorize)
        
        return data
    