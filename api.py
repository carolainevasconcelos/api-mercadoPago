from flask import Blueprint, jsonify
from models import Produto

api_blueprint = Blueprint('api', __name__, url_prefix='/api')

@api_blueprint.route('/produtos', methods=['GET'])
def get_produtos():
    """Retorna uma lista de todos os produtos."""
    try:
        produtos = Produto.query.all()
        lista_produtos = [
            {
                'id_produto': p.id_produto,
                'titulo': p.titulo,
                'descricao': p.descricao,
                'valor': p.valor
            }
            for p in produtos
        ]
        return jsonify(lista_produtos)
    except Exception as e:
        return jsonify({'error': 'Erro ao buscar produtos'}), 500