from database import Base, engine
from models import Pagamento  # importante para registrar a tabela

Base.metadata.create_all(bind=engine)