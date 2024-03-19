from ...entity.schemas import OrderModel
from pizza_api.repository.interface.order_repo import IOrderRepo
from pizza_api.entity.schemas import OrderModel, OrderStatusModel
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from pizza_api.db.database import get_db
from fastapi_jwt_auth import AuthJWT
from pizza_api.db.models import User, Order
from fastapi.encoders import jsonable_encoder


class OrderStore(IOrderRepo):
    async def __init__(self, db: Session = Depends(get_db)):
        self.session = db
        
    async def place_an_order(self, order:OrderModel, Authorize: AuthJWT = Depends()):
        try:
            Authorize.jwt_required()

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Token"
            )

        current_user=Authorize.get_jwt_subject()

        user=self.session.query(User).filter(User.username==current_user).first()


        new_order=Order(
            pizza_size=order.pizza_size,
            quantity=order.quantity
        )

        new_order.user=user

        self.session.add(new_order)

        self.session.commit()


        response={
            "pizza_size":new_order.pizza_size,
            "quantity":new_order.quantity,
            "id":new_order.id,
            "order_status":new_order.order_status
        }

        return jsonable_encoder(response)
    
    async def list_all_order(self, Authorize: AuthJWT = Depends()):
        try:
            Authorize.jwt_required()
            
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Token"
            )
        
        current_user = Authorize.get_jwt_subject()
        
        user = self.session.query(User).filter(User.username == current_user).first()
        
        if user.is_staff:
            orders = self.session.query(Order).all()
            
            return jsonable_encoder(orders)
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not a superuser"
        ) 
    
    async def get_order_by_id(self, order_id: int, Authorize: AuthJWT = Depends()):
        try:
            Authorize.jwt_required()
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Token"
            )
        current_user = Authorize.get_jwt_subject()
        
        user = self.session.query(User).filter(User.username == current_user).first()
        
        return jsonable_encoder(user)
    
    async def get_specific_order(self, order_id: int, Authorize: AuthJWT = Depends()):
        try:
            Authorize.jwt_required()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Token"
            )
        current_user = Authorize.get_jwt_subject()
        
        user = self.session.query(User).filter(User.username == current_user).first()
        
        orders = user.orders
        
        for order in orders:
            if order.id == order_id:
                return jsonable_encoder(order)
            
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="No order with such id"
        )
        
    async def get_user_orders(self, Authorize: AuthJWT):
        try:
            Authorize.jwt_required()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Token"
            )

        current_user=Authorize.get_jwt_subject()
        
        user = self.session.query(User).filter(User.username == current_user).first()
        
        return jsonable_encoder(user.orders)
    
    async def update_order(self, order_id: int, order: OrderModel, Authorize: AuthJWT = Depends()):
        try:
            Authorize.jwt_required()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Token"
            )
        order_to_update=self.session.query(Order).filter(Order.id == order_id).first()
        
        order_to_update.quantity=order.quantity
        order_to_update.pizza_size=order.pizza_size

        self.session.commit()


        response={
                    "id":order_to_update.id,
                    "quantity":order_to_update.quantity,
                    "pizza_size":order_to_update.pizza_size,
                    "order_status":order_to_update.order_status,
                }

        return jsonable_encoder(response)
    
    async def update_order_status(self, order_id:int, order:OrderStatusModel, Authorize:AuthJWT=Depends()):
    
        try:
            Authorize.jwt_required()

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token")

        current_user=Authorize.get_jwt_subject()

        user=self.session.query(User).filter(User.username == current_user).first()

        if user.is_staff:
            order_to_update=self.session.query(Order).filter(Order.id==order_id).first()

            order_to_update.order_status=order.order_status

            self.session.commit()

            response={
                    "id":order_to_update.id,
                    "quantity":order_to_update.quantity,
                    "pizza_size":order_to_update.pizza_size,
                    "order_status":order_to_update.order_status,
                }

            return jsonable_encoder(response)
        
    async def delete_an_order(self, order_id: int, Authorize:AuthJWT=Depends()):
        try:
            Authorize.jwt_required()

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token")

        order_to_delete = self.session.query(Order).filter(Order.id == order_id).first()
        
        self.session.delete(order_to_delete)
        
        return jsonable_encoder(order_to_delete)
        