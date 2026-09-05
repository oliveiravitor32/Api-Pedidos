import logging
import time

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

logger = logging.getLogger(__name__)

engine = create_engine(
    settings.database_url,
    echo=settings.db_echo,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


def wait_for_database() -> None:
    attempts = settings.db_connect_retries
    delay = settings.db_connect_retry_delay

    for attempt in range(1, attempts + 1):
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            logger.info("Conexao com o banco estabelecida.")
            return
        except OperationalError:
            if attempt == attempts:
                logger.error("Banco indisponivel apos %s tentativas.", attempts)
                raise
            logger.warning(
                "Banco indisponivel (tentativa %s/%s). Nova tentativa em %ss.",
                attempt,
                attempts,
                delay,
            )
            time.sleep(delay)


def create_tables() -> None:
    from app import entities  # noqa: F401

    Base.metadata.create_all(bind=engine)
    logger.info("Schema do banco verificado.")


def init_database() -> None:
    wait_for_database()
    create_tables()
