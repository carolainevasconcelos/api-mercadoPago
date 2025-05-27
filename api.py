from flask import Flask, render_template, redirect
import mercadopago
from models import Pagamento
from database import SessionLocal
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/pagar")
def pagar():
    sdk = mercadopago.SDK("APP_USR-8241943679467799-050815-c96878b9ed2ac44140fa9512483a8ea7-2427207497")

    preference_data = {
        "items": [
            {
                "title": "Produto Teste",
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": 100.0
            }
        ],
        "back_urls": {
            "success": "http://localhost:5000/concluido",
            "failure": "http://localhost:5000/pendente",
            "pending": "http://localhost:5000/pendente"
        }
        # "auto_return": "approved"  # ❌ Removido para evitar erro com URL local
    }

    preference_response = sdk.preference().create(preference_data)

    print("Resposta da API Mercado Pago:")
    print(preference_response)

    if "init_point" in preference_response.get("response", {}):
        init_point = preference_response["response"]["init_point"]
        return redirect(init_point)
    else:
        return "Erro ao criar preferência: verifique o terminal para mais detalhes."

@app.route("/concluido")
def concluido():
    session = SessionLocal()
    try:
        novo_pagamento = Pagamento(
            usuario_id=1,
            valor=100.0,
            moeda='BRL',
            status='aprovado',
            metodo_pagamento='mercado_pago',
            data_pagamento=datetime.now(),
            descricao='Produto Teste',
            mercadopago_id='simulado_id_123',
            confirmado=True
        )
        session.add(novo_pagamento)
        session.commit()
    except Exception as e:
        session.rollback()
        print("Erro ao salvar pagamento:", e)
        return "Erro ao salvar pagamento", 500
    finally:
        session.close()
    return render_template("concluido.html")


@app.route("/pendente")
def pendente():
    return render_template("pendente.html")

def atualizar_pagamento_no_banco(payment_id, status):
    # Aqui você faz a lógica de atualização no banco de dados
    pass

if __name__ == "__main__":
    app.run(debug=True)
