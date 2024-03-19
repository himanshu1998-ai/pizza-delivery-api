from abc import ABC, abstractmethod
from pizza_api.entity.schemas import SignUpModel, LoginModel

class IAuthRepo(ABC):
    @abstractmethod
    async def signup(user:SignUpModel):
        """
        ## Create a user
        This requires the following
        ```
                username:int
                email:str
                password:str
                is_staff:bool
                is_active:bool

        ```
    
        """
    
    @abstractmethod
    async def login(user:LoginModel):
        """     
        ## Login a user
        This requires
            ```
                username:str
                password:str
            ```
        and returns a token pair `access` and `refresh`
        """
        
    @abstractmethod
    async def refresh_token():
        """
    ## Create a fresh token
    This creates a fresh token. It requires an refresh token.
        """
    
    