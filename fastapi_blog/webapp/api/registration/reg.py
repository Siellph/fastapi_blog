from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.registration.router import reg_router
from webapp.crud.user import create_user, get_user_by_email
from webapp.db.postgres import get_session
from webapp.schema.login.user import UserLoginResponse
from webapp.schema.registration.reg import UserRegistration
from webapp.utils.auth.jwt import jwt_auth
from webapp.utils.auth.password import hash_password


@reg_router.post('/register', response_model=UserLoginResponse, status_code=status.HTTP_201_CREATED)
async def register(
    body: UserRegistration,
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    # Проверка, существует ли уже пользователь с таким email
    existing_user = await get_user_by_email(session, body.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email уже используется')

    # Хеширование пароля
    hashed_password = hash_password(body.password)

    # Создание нового пользователя
    user = await create_user(session, body.username, body.email, hashed_password)

    # Создание токена доступа для нового пользователя
    return ORJSONResponse(
        {
            'access_token': jwt_auth.create_token(user.id),
        },
        status_code=status.HTTP_201_CREATED,
    )
