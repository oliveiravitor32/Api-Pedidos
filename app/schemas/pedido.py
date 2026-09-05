from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.entities.pedido import StatusPedido


class PedidoCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    cliente: str = Field(min_length=1, max_length=120)
    produto: str = Field(min_length=1, max_length=120)
    quantidade: int = Field(gt=0)
    valor_unitario: Decimal = Field(gt=0, max_digits=12, decimal_places=2)


class PedidoStatusUpdate(BaseModel):
    status: StatusPedido


class PedidoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cliente: str
    produto: str
    quantidade: int
    valor_unitario: Decimal
    valor_total: Decimal
    status: StatusPedido
    data_criacao: datetime
