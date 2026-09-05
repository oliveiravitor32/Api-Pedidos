from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.pedido_repository import PedidoRepository
from app.services.pedido_service import PedidoService


def get_pedido_repository(db: Session = Depends(get_db)) -> PedidoRepository:
    return PedidoRepository(db)


def get_pedido_service(
    db: Session = Depends(get_db),
    repository: PedidoRepository = Depends(get_pedido_repository),
) -> PedidoService:
    return PedidoService(db, repository)
