from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_pedido_service
from app.schemas.pedido import PedidoCreate, PedidoResponse, PedidoStatusUpdate
from app.services.pedido_service import PedidoService

router = APIRouter(prefix="/pedidos", tags=["pedidos"])


@router.post("", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
def criar_pedido(
    dados: PedidoCreate,
    service: PedidoService = Depends(get_pedido_service),
) -> PedidoResponse:
    return service.criar(dados)


@router.get("", response_model=list[PedidoResponse])
def listar_pedidos(
    service: PedidoService = Depends(get_pedido_service),
) -> list[PedidoResponse]:
    return service.listar()


@router.get("/{pedido_id}", response_model=PedidoResponse)
def consultar_pedido(
    pedido_id: int,
    service: PedidoService = Depends(get_pedido_service),
) -> PedidoResponse:
    return service.buscar_por_id(pedido_id)


@router.patch("/{pedido_id}/status", response_model=PedidoResponse)
def alterar_status(
    pedido_id: int,
    dados: PedidoStatusUpdate,
    service: PedidoService = Depends(get_pedido_service),
) -> PedidoResponse:
    return service.alterar_status(pedido_id, dados.status)
