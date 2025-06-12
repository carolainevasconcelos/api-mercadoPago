# Arquivo: api_v2.py (Versão Verificada)

from flask import Blueprint, request, jsonify
from database import db
from models import Plano, Subscricao
# Não precisamos mais do Pagamento aqui por enquanto

api_v2_blueprint = Blueprint('api_v2', __name__, url_prefix='/api/v2')

@api_v2_blueprint.route('/planos', methods=['GET'])
def get_planos():
    planos = Plano.query.all()
    return jsonify([{'id_plano': p.id_plano, 'descricao': p.descricao} for p in planos])

# Adicione outras rotas de API aqui no futuro, se precisar