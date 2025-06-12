# carolainevasconcelos/api-mercadopago/api-mercadoPago-1f8088de44293b8b947d9ea67374db42823ee341/models.py

from database import db
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
import uuid

# Seu modelo 'Produto' existente
class Produto(db.Model):
    id_produto = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    descricao = db.Column(db.String(255))
    valor = db.Column(db.Float)

# --- NOVOS MODELOS ---

class Plano(db.Model):
    __tablename__ = 'planos'
    id_plano = db.Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    descricao = db.Column(db.String(255), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    subscricoes = relationship("Subscricao", back_populates="plano")

class Pagamento(db.Model):
    __tablename__ = 'pagamentos'
    id_transacao = db.Column(db.String(255), primary_key=True)
    status = db.Column(db.String(50), nullable=False)
    metodo_pagamento = db.Column(db.String(50))
    valor = db.Column(db.Float, nullable=False)
    data_pagamento = db.Column(db.DateTime, nullable=False)
    comprador_nome = db.Column(db.String(255))
    comprador_email = db.Column(db.String(255))
    
    # Chave estrangeira para a subscrição
    id_subscricao = db.Column(CHAR(36), db.ForeignKey('subscricoes.id_subscricao'))
    subscricao = relationship("Subscricao", back_populates="pagamentos")

class Subscricao(db.Model):
    __tablename__ = 'subscricoes'
    id_subscricao = db.Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    ativo = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, server_default=db.func.now())
    data_expiracao = db.Column(db.DateTime, nullable=True)
    
    # Chave estrangeira para o plano
    id_plano = db.Column(CHAR(36), db.ForeignKey('planos.id_plano'))
    plano = relationship("Plano", back_populates="subscricoes")
    
    # Relacionamento com pagamentos
    pagamentos = relationship("Pagamento", back_populates="subscricao", cascade="all, delete-orphan")