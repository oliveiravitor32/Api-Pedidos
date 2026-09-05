import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.config import settings
from app.controllers import health_controller, pedido_controller
from app.core.exceptions import PedidoNaoEncontrado, TransicaoStatusInvalida
from app.database.connection import init_database

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)


@app.exception_handler(PedidoNaoEncontrado)
async def pedido_nao_encontrado_handler(
    request: Request, exc: PedidoNaoEncontrado
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


@app.exception_handler(TransicaoStatusInvalida)
async def transicao_status_invalida_handler(
    request: Request, exc: TransicaoStatusInvalida
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )


app.include_router(health_controller.router)
app.include_router(pedido_controller.router)
