#autenticacion de usuarios de manera basica
from fastapi import APIRouter, Depends, HTTPException,status
from pydantic import BaseModel
#modulo de autenticacion
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/UserLoginJwt",
    tags=["Users basic authentication"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str 
    email: str
    disabled : bool

#usuario de la base de datos
class UserDB(User):
    password: str

#base de datos usuarios
users_db = {
    "Luiso-o" : {
    "username" : "Luiso-o",
    "full_name": "Luis Trujillo" ,
    "email": "luis@ejemplo.com",
    "disabled" : False,
    "password" : "123456"
    },
    "pepe" : {
    "username" : "pepe2",
    "full_name": "Pepe Mojica" ,
    "email": "pepe@ejemplo.com",
    "disabled" : True,
    "password" : "654321"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def current_user(token: str = Depends(oauth2)):
   user = search_user(token)
   if not user:
       raise HTTPException (
           status_code= status.HTTP_401_UNAUTHORIZED ,
           detail="Credenciales de autenticación inválidas",
            headers={"WWW-Authenticate":"Bearer"})
   
   if user.disabled:
       raise HTTPException (
           status_code= status.HTTP_400_BAD_REQUEST,
           detail="Usuario inactivo")
   
   return user

#operacion de autenticacion
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()): 
    user_db = search_user_db(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    if not form.password == user_db.password:
        raise HTTPException(status_code=400, detail="La contrasena no es correcta")
    
    return {"access_token": user_db.username, "token_type": "bearer"}
    
@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user