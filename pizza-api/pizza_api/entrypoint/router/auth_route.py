from fastapi import APIRouter,status,Depends
from fastapi_jwt_auth import AuthJWT
from repository.impl.auth_store import AuthStore
from usecases.auth_usecase.signup_usecase import SignUpUsecase
from usecases.auth_usecase.login_usecase import LoginUsecase
from usecases.auth_usecase.refresh_token_usecase import RefreshTokenUsecase
from db.database import get_db
from entity.schemas import SignUpModel, LoginModel

auth_router=APIRouter(
    prefix='/auth',
    tags=['auth']

)


@auth_router.post('/signup',
    status_code=status.HTTP_201_CREATED
)
async def signup(user:SignUpModel):
    
    repo = AuthStore(next(get_db()))
    usecase = SignUpUsecase(repo)
    data = await usecase.execute(model=user)
    return data


#login route

@auth_router.post('/login',status_code=200)
async def login(user:LoginModel,Authorize:AuthJWT=Depends()):
    
    repo = AuthStore(next(get_db()))
    usecase = LoginUsecase(repo)
    data = await usecase.execute(model=user, Authorize=Authorize)
    return data


#refreshing tokens

@auth_router.get('/refresh')
async def refresh_token(Authorize:AuthJWT=Depends()):
    
    repo = AuthStore(next(get_db()))
    usecase = RefreshTokenUsecase(repo)
    data = await usecase.execute(Authorize=Authorize)
    return data
