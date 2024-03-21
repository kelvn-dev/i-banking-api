from fastapi import FastAPI

from routers import (
    s3_router,
    student_router,
    transaction_router,
    tuition_router,
    user_router,
)

PREFIX = "/api/v1"


def create_endpoints(app: FastAPI):
    app.include_router(user_router.router, prefix=PREFIX)
    app.include_router(student_router.router, prefix=PREFIX)
    app.include_router(tuition_router.router, prefix=PREFIX)
    app.include_router(transaction_router.router, prefix=PREFIX)
    app.include_router(s3_router.router, prefix=PREFIX)
