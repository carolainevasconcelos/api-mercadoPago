from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from database import Base

class Pagamento(Base):
    __tablename__ = 'pagamentos'
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, index=True)
    valor = Column(Float, nullable=False)
    moeda = Column(String(10), default='BRL')
    status = Column(String(50), nullable=False)
    metodo_pagamento = Column(String(50))
    data_pagamento = Column(DateTime)
    descricao = Column(String(255))
    mercadopago_id = Column(String(100), unique=True, index=True)
    confirmado = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Pagamento(id={self.id}, valor={self.valor}, status={self.status}, confirmado={self.confirmado})>"