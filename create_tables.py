from app import app
from database import db
from models import Produto, Plano, Pagamento, Subscricao

with app.app_context():
    print("Criando tabelas no banco de dados...")
    db.create_all()
    print("Tabelas criadas com sucesso!")