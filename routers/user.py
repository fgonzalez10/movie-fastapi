from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import  JSONResponse
from user_jwt import createToken


login_user = APIRouter()


class User(BaseModel):
    email: str
    password: str



@login_user.post('/login', tags=['autentication'])
def login(user: User):
    if user.email == 'fgonzalez@notario.com.mx' and user.password == '123':
        token : str = createToken(user.dict())
        print(token)
        return JSONResponse(content=token)