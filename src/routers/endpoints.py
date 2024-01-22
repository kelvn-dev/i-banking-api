from fastapi import FastAPI

from routers import user_router

PREFIX = "/api/v1"


def create_endpoints(app: FastAPI):
    app.include_router(user_router.router)
