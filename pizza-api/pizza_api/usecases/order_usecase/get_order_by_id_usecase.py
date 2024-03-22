from pizza_api.repository.interface.order_repo import IOrderRepo
from fastapi_jwt_auth import AuthJWT
from fastapi import Depends

class GetOrderByIdOrderUsecase:
    def __init__(self, repo: IOrderRepo):
        self.repo = repo
        
    async def execute(self, order_id: int, Authorize: AuthJWT = Depends()):
        
        data = await self.repo.get_order_by_id(order_id=order_id, Authorize=Authorize)
        
        return data
    