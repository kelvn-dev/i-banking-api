from fastapi import FastAPI

from routes import user_route

PREFIX = "/api/v1"


def create_endpoints(app: FastAPI):
    app.include_router(user_route.router)
