from fastapi import FastAPI
from routers import basic_auth_users,jwt_auth_users

app = FastAPI(
    title = "REST API whit fastAPI and Basic security",
    description= "This is a simple API using fastAPI and auth",
    version="0.0.1",
)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)