from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.pedido import Pedido


class PedidoRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def add(self, pedido: Pedido) -> Pedido:
        self.db.add(pedido)
        self.db.flush()
        return pedido

    def get_by_id(self, pedido_id: int) -> Pedido | None:
        return self.db.get(Pedido, pedido_id)

    def list_all(self) -> list[Pedido]:
        statement = select(Pedido).order_by(Pedido.id)
        return list(self.db.scalars(statement).all())
