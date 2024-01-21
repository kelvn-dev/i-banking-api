import contextlib
import warnings
from typing import Generator

from fastapi import HTTPException
from loguru import logger
from sqlalchemy import MetaData, create_engine, schema
from sqlalchemy.exc import NoResultFound, SAWarning
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from sqlalchemy_utils.functions import create_database, database_exists

from config.setting import settings

# db_connection_url = f'postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}'
db_connection_url = settings.db_uri

engine = create_engine(
    url=db_connection_url,
    echo=False,
    connect_args={
        "options": f"-csearch_path={settings.DB_SCHEMA}",
        "options": "-c timezone=utc",
    },
)

# Difference between flush and commit: https://www.youtube.com/watch?v=1atze8xe9wg&ab_channel=HowtoFixYourComputer
Session = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, expire_on_commit=False
)

# inherit from this class to create each of the database models
Base = declarative_base(metadata=MetaData(schema=f"{settings.db_schema}"))


def create_db():
    logger.debug("Creating Database")
    if not database_exists(db_connection_url):
        create_database(db_connection_url)


def create_schema():
    logger.debug("Creating Schema")
    if not engine.dialect.has_schema(engine, f"{settings.db_schema}"):
        engine.execute(schema.CreateSchema(f"{settings.db_schema}"))


def create_tables():
    logger.debug("Creating Tables")
    Base.metadata.create_all(bind=engine, checkfirst=True)


def drop_tables():
    logger.debug("Dropping Tables")
    Base.metadata.drop_all(bind=engine, checkfirst=True)


# For foreign key problem in future, refer to this solution https://gist.github.com/absent1706/3ccc1722ea3ca23a5cf54821dbc813fb
def truncate_db():
    logger.debug("Truncating Tables")
    tables = Base.metadata.sorted_tables

    with contextlib.closing(engine.connect()) as ctx:
        transaction = ctx.begin()
        ctx.execute(
            "TRUNCATE TABLE {} RESTART IDENTITY CASCADE".format(
                ",".join(table.name for table in tables)
            )
        )
        transaction.commit()


# create a database session for each request - close it after finishing the request
def get_session() -> Generator:
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=SAWarning)
            session = Session()
            yield session
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=e._message())
    finally:
        session.close()
