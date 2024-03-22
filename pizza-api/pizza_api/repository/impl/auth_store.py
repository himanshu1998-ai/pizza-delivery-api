from pizza_api.entity.schemas import LoginModel
from pizza_api.entity.schemas import SignUpModel
from pizza_api.repository.interface.auth_repo import IAuthRepo
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from pizza_api.db.database import get_db
from fastapi_jwt_auth import AuthJWT
from pizza_api.db.models import User
from fastapi.encoders import jsonable_encoder
from werkzeug.security import generate_password_hash , check_password_hash


class AuthStore(IAuthRepo):
    def __init__(self, db: Session = Depends(get_db)):
        self.session = db
        
    async def signup(self, user: SignUpModel) -> User|HTTPException:
        db_email= self.session.query(User).filter(User.email==user.email).first()

        if db_email is not None:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with the email already exists"
            )

        db_username= self.session.query(User).filter(User.username==user.username).first()

        if db_username is not None:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with the username already exists"
            )

        new_user= User(
            username=user.username,
            email=user.email,
            password=generate_password_hash(user.password),
            is_active=user.is_active,
            is_staff=user.is_staff
        )

        self.session.add(new_user)

        self.session.commit()

        return new_user
    
    async def login(self, user: LoginModel, Authorize:AuthJWT=Depends()):
        db_user=self.session.query(User).filter(User.username==user.username).first()

        if db_user and check_password_hash(db_user.password, user.password):
            access_token=Authorize.create_access_token(subject=db_user.username)
            refresh_token=Authorize.create_refresh_token(subject=db_user.username)

            response={
                "access":access_token,
                "refresh":refresh_token
            }

            return jsonable_encoder(response)

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Username Or Password"
        )

    async def refresh_token(Authorize:AuthJWT=Depends()):
        try:
            Authorize.jwt_refresh_token_required()

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Please provide a valid refresh token"
            ) 

        current_user=Authorize.get_jwt_subject()

        
        access_token=Authorize.create_access_token(subject=current_user)

        return jsonable_encoder({"access":access_token})