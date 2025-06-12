# Arquivo: app.py (VERSÃO COMPLETA E CORRIGIDA)

import os
import mercadopago
from flask import Flask, render_template, redirect
from dotenv import load_dotenv

# Meus outros arquivos
from database import db
from models import Produto, Plano, Pagamento, Subscricao
from api_v2 import api_v2_blueprint

# Carrega as variáveis do arquivo .env
load_dotenv()

# --- CONFIGURAÇÃO DA APLICAÇÃO ---
app = Flask(__name__)

# Pega a URL do banco de dados do arquivo .env
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados com a aplicação
db.init_app(app)

# Registra as rotas da nossa API (planos, pagamentos, etc.)
app.register_blueprint(api_v2_blueprint)

# --- ROTAS PRINCIPAIS ---

@app.route("/")
def homepage():
    """Renderiza a página inicial."""
    return render_template("homepage.html")

@app.route("/pagar")
def pagar():
    """Cria a preferência de pagamento e redireciona o usuário."""
    
    # Pega o Access Token do arquivo .env
    access_token = os.getenv("MERCADOPAGO_ACCESS_TOKEN")

    # Verifica se o token foi carregado
    if not access_token:
        return "Erro: MERCADOPAGO_ACCESS_TOKEN não encontrado no arquivo .env", 500

    sdk = mercadopago.SDK(access_token)

    # Dados da preferência de pagamento
    preference_data = {
        "items": [
            {
                "title": "Assinatura VIP",
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": 150.00
            }
        ],
        "back_urls": {
            "success": "http://127.0.0.1:5000/concluido",
            "failure": "http://127.0.0.1:5000/falha",
        }
    }

    try:
        # Tenta criar a preferência
        preference_response = sdk.preference().create(preference_data)
        
        # Verifica se a resposta foi bem-sucedida E se contém o link
        if preference_response["status"] == 201 and "init_point" in preference_response["response"]:
            init_point = preference_response["response"]["init_point"]
            return redirect(init_point)
        else:
            # Se deu erro, imprime a resposta do MP no console
            print("--- ERRO DO MERCADO PAGO ---")
            print(preference_response)
            return "Erro ao criar preferência. Verifique o console do terminal para mais detalhes.", 500

    except Exception as e:
        # Se qualquer outro erro acontecer
        print(f"--- ERRO INESPERADO NO CÓDIGO ---")
        print(e)
        return "Um erro inesperado ocorreu. Verifique o console do terminal.", 500


@app.route("/concluido")
def concluido():
    return "<h1>Pagamento Concluído com Sucesso!</h1>"

@app.route("/falha")
def falha():
    return "<h1>O Pagamento Falhou.</h1>"


# Este bloco só é executado quando rodamos 'python app.py' diretamente
if __name__ == '__main__':
    app.run(debug=True)