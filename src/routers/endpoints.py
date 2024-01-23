from fastapi import FastAPI

from routers import semester_router, user_router

PREFIX = "/api/v1"


def create_endpoints(app: FastAPI):
    app.include_router(user_router.router, prefix=PREFIX)
    app.include_router(semester_router.router, prefix=PREFIX)
