from fastapi import APIRouter, Response, Depends

from app.business_logic.users.auth import hash_password, authenticate_user, create_access_token
from app.business_logic.users.dao import UsersDAO
from app.business_logic.users.dependencies import get_user
from app.business_logic.users.models import User
from app.business_logic.users.schemas import UserRegistrationDTO, UserLoginDTO, UserPublicDTO
from app.config import get_registration_secret
from app.exceptions import UserAlreadyExistsException, ForbiddenException, IncorrectEmailOrPasswordException

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/register')
async def register_user(user_data: UserRegistrationDTO) -> dict:
    if not user_data.registration_secret == get_registration_secret():
        raise ForbiddenException
    user = await UsersDAO.find_one(email=user_data.email)
    if user:
        raise UserAlreadyExistsException
    user_info = user_data.model_dump()
    user_info['password'] = hash_password(user_data.password)
    del user_info['registration_secret']
    await UsersDAO.add(**user_info)
    return {'message': 'Пользователь успешно зарегистрирован'}


@router.post('/login')
async def login_user(response: Response, user_data: UserLoginDTO) -> dict:
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie(key='access_token', value=access_token, httponly=True)
    return {'ok': True, 'access_token': access_token,
            'message': 'Авторизация прошла успешно'}


@router.get('/me')
async def get_me(user_data: User = Depends(get_user)):
    return UserPublicDTO(**user_data.__dict__)


@router.post('/logout')
async def logout(response: Response):
    response.delete_cookie('access_token')
    return {'message': 'Пользователь успешно вышел из системы'}