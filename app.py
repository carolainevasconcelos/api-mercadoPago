import hmac
import hashlib
import json

WEBHOOK_SECRET = os.getenv("MERCADOPAGO_WEBHOOK_SECRET")

@app.route('/notificacao', methods=['POST'])
def notificacao():
    request_id = request.headers.get("X-Request-Id")
    signature = request.headers.get("X-Signature")

    if not request_id or not signature:
        print("Webhook: Headers de assinatura (X-Request-Id ou X-Signature) ausentes.")
        return "Headers de assinatura ausentes.", 400

    data = request.json
    topic = data.get('type')
    payment_id = data.get('data', {}).get('id')

    if not topic or not payment_id:
        print(f"Webhook: Payload inválido recebido: {data}")
        return "Payload inválido.", 400

    if not WEBHOOK_SECRET:
        print("ERRO CRÍTICO: Segredo do Webhook (MERCADOPAGO_WEBHOOK_SECRET) não está configurado.")
        return "OK", 200

    parts = signature.split(',')
    ts_part = next((part for part in parts if part.strip().startswith('ts=')), None)
    v1_part = next((part for part in parts if part.strip().startswith('v1=')), None)

    if not ts_part or not v1_part:
        print(f"Webhook: Assinatura com formato inválido: {signature}")
        return "Formato de assinatura inválido.", 400

    ts = ts_part.strip().split('=')[1]
    v1 = v1_part.strip().split('=')[1]
    
    manifest = f"id:{payment_id};request-id:{request_id};ts:{ts};"

    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        msg=manifest.encode(),
        digestmod=hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected_signature, v1):
        print(f"Webhook: Assinatura inválida! Esperado: {expected_signature}, Recebido: {v1}")
        return "Assinatura inválida.", 403

    print(f"Webhook com assinatura validada para o pagamento: {payment_id}")

    if topic == 'payment':
        try:
            sdk = mercadopago.SDK(os.getenv("MERCADOPAGO_ACCESS_TOKEN"))
            payment_info = sdk.payment().get(payment_id)

            if payment_info["status"] == 200:
                payment_data = payment_info["response"]
                
                pagamento_a_atualizar = Pagamentos.query.filter_by(payment_id=str(payment_data['id'])).first()

                if pagamento_a_atualizar:
                    pagamento_a_atualizar.status = payment_data['status']
                    db.session.commit()
                    print(f"Banco de dados atualizado para o pagamento {payment_id} com status '{payment_data['status']}'")

                    if payment_data['status'] == 'approved':
                        print(f"Pagamento {payment_id} foi APROVADO.")
                    else:
                        print(f"Pagamento {payment_id} teve status atualizado para {payment_data['status']}.")

                else:
                    print(f"AVISO: Pagamento com payment_id {payment_id} não encontrado no banco de dados para atualização.")

            else:
                print(f"Erro ao buscar informações do pagamento {payment_id} na API do Mercado Pago.")

        except Exception as e:
            print(f"Erro ao processar o webhook para o pagamento {payment_id}: {e}")
            db.session.rollback() 
    
    return "OK", 200