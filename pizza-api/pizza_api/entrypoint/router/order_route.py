from fastapi import APIRouter,Depends,status
from fastapi_jwt_auth import AuthJWT
from pizza_api.db.database import get_db
from pizza_api.repository.impl.order_store import OrderStore
from pizza_api.entity.schemas import OrderModel, OrderStatusModel
from pizza_api.usecases.order_usecase.place_order_usecase import PlaceOrderUsecase
from pizza_api.usecases.order_usecase.list_all_usecase import ListAllOrderUsecase
from pizza_api.usecases.order_usecase.get_order_by_id_usecase import GetOrderByIdOrderUsecase
from pizza_api.usecases.order_usecase.get_specific_order_usecase import GetSpecificOrderUsecase
from pizza_api.usecases.order_usecase.get_user_orders_usecase import GetUserOrderUsecase
from pizza_api.usecases.order_usecase.update_order_usecase import UpdateOrderUsecase
from pizza_api.usecases.order_usecase.update_order_status import UpdateOrderStatusUsecase
from pizza_api.usecases.order_usecase.delete_order_usecase import DeleteOrderUsecase







order_router=APIRouter(
    prefix="/orders",
    tags=['orders']
)


@order_router.post('/order',status_code=status.HTTP_201_CREATED)
async def place_an_order(order:OrderModel,Authorize:AuthJWT=Depends()):
    """
            ## Placing an Order
            This requires the following
            - quantity : integer
            - pizza_size: str

        """
    repo = OrderStore(next(get_db()))
    usecase = PlaceOrderUsecase(repo)
    data = await usecase.execute(order=order, Authorize=Authorize)
    return data


    
@order_router.get('/orders')
async def list_all_orders(Authorize:AuthJWT=Depends()):
    """
           ## List all orders
           This lists all  orders made. It can be accessed by superusers


       """
    repo = OrderStore(next(get_db()))
    usecase = ListAllOrderUsecase(repo)
    data = await usecase.execute(Authorize=Authorize)
    return data


@order_router.get('/orders/{id}')
async def get_order_by_id(order_id:int, Authorize: AuthJWT=Depends()):
    """
            ## Get an order by its ID
            This gets an order by its ID and is only accessed by a superuser


        """
    repo = OrderStore(next(get_db()))
    usecase = GetOrderByIdOrderUsecase(repo)
    data = await usecase.execute(order_id=order_id, Authorize=Authorize)
    return data


@order_router.get('/user/orders')
async def get_user_orders(Authorize:AuthJWT=Depends()):
    """
            ## Get a current user's orders
            This lists the orders made by the currently logged in users

        """
    repo = OrderStore(next(get_db()))
    usecase = GetUserOrderUsecase(repo)
    data = await usecase.execute(Authorize=Authorize)
    return data

@order_router.get('/user/order/{id}/')
async def get_specific_order(order_id:int,Authorize:AuthJWT=Depends()):
    """
            ## Get a specific order by the currently logged in user
            This returns an order by ID for the currently logged in user

        """
    repo = OrderStore(next(get_db()))
    usecase = GetSpecificOrderUsecase(repo)
    data = await usecase.execute(order_id=order_id, Authorize=Authorize)
    return data

@order_router.put('/order/update/{id}/')
async def update_order(order_id:int,order:OrderModel,Authorize:AuthJWT=Depends()):
    """
            ## Updating an order
            This udates an order and requires the following fields
            - quantity : integer
            - pizza_size: str

        """
    repo = OrderStore(next(get_db()))
    usecase = UpdateOrderUsecase(repo)
    data = await usecase.execute(order_id=order_id, Authorize=Authorize)
    return data

@order_router.patch('/order/update/{id}/')
async def update_order_status(order_id:int,
        order:OrderStatusModel,
        Authorize:AuthJWT=Depends()):
    """
            ## Update an order's status
            This is for updating an order's status and requires ` order_status ` in str format
        """
    repo = OrderStore(next(get_db()))
    usecase = UpdateOrderStatusUsecase(repo)
    data = await usecase.execute(order_id=order_id, order=order, Authorize=Authorize)
    return data


@order_router.delete('/order/delete/{id}/',status_code=status.HTTP_204_NO_CONTENT)
async def delete_an_order(order_id:int,Authorize:AuthJWT=Depends()):
    """
            ## Delete an Order
            This deletes an order by its ID
        """

    repo = OrderStore(next(get_db()))
    usecase = DeleteOrderUsecase(repo)
    data = await usecase.execute(order_id=order_id, Authorize=Authorize)
    return data
