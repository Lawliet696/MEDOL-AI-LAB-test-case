from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from datetime import timedelta

from app.models.user import User
from app.backend.db_depends import get_db
from app.schemas.User import CreateUserSchema
from app.services import auth_services
from app.services.auth_services import bcrypt_context
from app.settings import settings

router = APIRouter(tags=['Auth'])


@router.post('/register',
             summary='Register',
             description='Регистрация нового пользователя',
             status_code=status.HTTP_201_CREATED)
async def register(db: Annotated[AsyncSession, Depends(get_db)], user: CreateUserSchema):
    try:
        await db.execute(insert(User).values(username=user.username,
                                             hashed_password=bcrypt_context.hash(user.password)))
        await db.commit()
        return {
            'status_code': status.HTTP_201_CREATED,
            'detail': 'User has been created'
        }

    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User is already registered'
        )


@router.post('/login',
             summary='Login',
             description='Аутентификация пользователя, возвращает access-токен с указанным в настройках ttl',
             status_code=status.HTTP_200_OK)
async def login(db: Annotated[AsyncSession, Depends(get_db)], login_user: CreateUserSchema):
    user = await auth_services.authenticate_user(db, login_user.username, login_user.password)
    token = await auth_services.create_access_token(user.username, user.id, user.is_admin, user.is_patient,
                                                    user.is_doctor, expires_delta=timedelta(minutes=settings.token_ttl))

    return {
        'access_token': token
    }


@router.get('/me',
            summary='Get user info',
            description='Возвращает информацию о пользователе из JWT токена',
            status_code=status.HTTP_200_OK)
async def get_current_user_info(get_current_user: Annotated[dict, Depends(auth_services.get_current_user)]):
    return get_current_user
