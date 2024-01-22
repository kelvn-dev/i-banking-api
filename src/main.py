from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

from config.database import create_db, create_schema, create_tables
from config.setting import settings
from routers.endpoints import create_endpoints
from security.user_session import get_current_user

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=86400,
)


@app.get("/api/messages/public")
def public():
    return {"text": "This is a public message."}


create_endpoints(app)


@app.on_event("startup")
def app_startup():
    create_db()
    create_schema()
    create_tables()
    pass


@app.on_event("shutdown")
def app_shutdown():
    pass
