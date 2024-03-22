from pizza_api.repository.interface.order_repo import IOrderRepo
from pizza_api.entity.schemas import OrderModel
from fastapi_jwt_auth import AuthJWT
from fastapi import Depends

class PlaceOrderUsecase:
    def __init__(self, repo: IOrderRepo):
        self.repo = repo
        
    async def execute(self, order:OrderModel, Authorize: AuthJWT = Depends()):
        data = await self.repo.place_an_order(order=order, Authorize=Authorize)
        return data
    