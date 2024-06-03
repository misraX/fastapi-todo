from fastapi import FastAPI

from app.todo.api import routes as todo_routes
from app.user.api import routes as user_routes

app = FastAPI()

app.include_router(user_routes.router)
app.include_router(todo_routes.router)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application"}
