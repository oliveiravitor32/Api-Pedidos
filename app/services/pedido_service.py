from decimal import Decimal
from typing import Final

from sqlalchemy.orm import Session

from app.core.exceptions import PedidoNaoEncontrado, TransicaoStatusInvalida
from app.entities.pedido import Pedido, StatusPedido
from app.repositories.pedido_repository import PedidoRepository
from app.schemas.pedido import PedidoCreate

TRANSICOES_PERMITIDAS: Final[dict[StatusPedido, set[StatusPedido]]] = {
    StatusPedido.CRIADO: {StatusPedido.CONFIRMADO, StatusPedido.CANCELADO},
    StatusPedido.CONFIRMADO: {StatusPedido.CANCELADO},
    StatusPedido.CANCELADO: set(),
}

CENTAVOS: Final[Decimal] = Decimal("0.01")


class PedidoService:
    def __init__(self, db: Session, repository: PedidoRepository) -> None:
        self.db = db
        self.repository = repository

    def criar(self, dados: PedidoCreate) -> Pedido:
        pedido = Pedido(
            cliente=dados.cliente,
            produto=dados.produto,
            quantidade=dados.quantidade,
            valor_unitario=dados.valor_unitario,
            valor_total=self._calcular_valor_total(
                dados.quantidade, dados.valor_unitario
            ),
            status=StatusPedido.CRIADO,
        )
        self.repository.add(pedido)
        self.db.commit()
        self.db.refresh(pedido)
        return pedido

    def buscar_por_id(self, pedido_id: int) -> Pedido:
        pedido = self.repository.get_by_id(pedido_id)
        if pedido is None:
            raise PedidoNaoEncontrado(pedido_id)
        return pedido

    def listar(self) -> list[Pedido]:
        return self.repository.list_all()

    def alterar_status(self, pedido_id: int, novo_status: StatusPedido) -> Pedido:
        pedido = self.buscar_por_id(pedido_id)

        if novo_status not in TRANSICOES_PERMITIDAS[pedido.status]:
            raise TransicaoStatusInvalida(pedido.status, novo_status)

        pedido.status = novo_status
        self.db.commit()
        self.db.refresh(pedido)
        return pedido

    @staticmethod
    def _calcular_valor_total(quantidade: int, valor_unitario: Decimal) -> Decimal:
        return (valor_unitario * quantidade).quantize(CENTAVOS)
