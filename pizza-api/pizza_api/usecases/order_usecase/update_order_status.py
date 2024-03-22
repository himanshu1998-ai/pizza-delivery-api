from pizza_api.repository.interface.order_repo import IOrderRepo
from pizza_api.entity.schemas import OrderModel
from fastapi_jwt_auth import AuthJWT
from fastapi import Depends

class UpdateOrderStatusUsecase:
    def __init__(self, repo: IOrderRepo):
        self.repo = repo
        
    async def execute(self, order_id: int, order:OrderModel, Authorize: AuthJWT = Depends()):
        
        data = await self.repo.update_order_status(order_id=order_id, order=order, Authorize=Authorize)
        
        return data
    