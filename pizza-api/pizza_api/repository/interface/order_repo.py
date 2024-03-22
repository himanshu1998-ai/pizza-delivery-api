from abc import ABC, abstractmethod
from pizza_api.entity.schemas import OrderModel, OrderStatusModel

class IOrderRepo(ABC):
    
    @abstractmethod
    async def place_an_order(self, order:OrderModel):
        """
        ## Placing an Order
        This requires the following
        - quantity : integer
        - pizza_size: str
    
        """
    
    @abstractmethod
    async def list_all_order(self):
        """
        ## List all orders
        This lists all  orders made. It can be accessed by superusers
        
    
        """
    
    @abstractmethod
    async def get_order_by_id(self, order_id: int):
        """
        ## Get an order by its ID
        This gets an order by its ID and is only accessed by a superuser
        

        """
    
    @abstractmethod
    async def get_user_orders(self):
        """
        ## Get a current user's orders
        This lists the orders made by the currently logged in users
    
        """
    
    @abstractmethod
    async def get_specific_order(self, order_id: int):
        """
        ## Get a specific order by the currently logged in user
        This returns an order by ID for the currently logged in user
    
        """
    
    @abstractmethod
    async def update_order(self, order_id: int, order:OrderModel):
        """
        ## Updating an order
        This udates an order and requires the following fields
        - quantity : integer
        - pizza_size: str
    
        """
    
    @abstractmethod
    async def update_order_status(self, order_id: int, order:OrderStatusModel):
        """
        ## Update an order's status
        This is for updating an order's status and requires ` order_status ` in str format
        """
    
    
    @abstractmethod
    async def delete_an_order(self, order_id: int):
         """
        ## Delete an Order
        This deletes an order by its ID
         """
    