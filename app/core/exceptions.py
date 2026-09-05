from app.entities.pedido import StatusPedido


class DominioError(Exception):
    pass


class PedidoNaoEncontrado(DominioError):
    def __init__(self, pedido_id: int) -> None:
        self.pedido_id = pedido_id
        super().__init__(f"Pedido {pedido_id} nao encontrado.")


class TransicaoStatusInvalida(DominioError):
    def __init__(self, atual: StatusPedido, novo: StatusPedido) -> None:
        self.atual = atual
        self.novo = novo
        super().__init__(
            f"Nao e possivel alterar o status de {atual.value} para {novo.value}."
        )
