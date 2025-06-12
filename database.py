# Arquivo: database.py (Versão Correta para o Projeto)

from flask_sqlalchemy import SQLAlchemy

# Cria a instância do SQLAlchemy.
# É esta variável 'db' que os outros arquivos (main.py, models.py)
# estão esperando para importar.
db = SQLAlchemy()