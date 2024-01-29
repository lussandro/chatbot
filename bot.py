from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Recebe os dados do webhook
    data = request.json
    print("Dados recebidos:", data)

    # Extrai os dados específicos
    remote_jid = data['data']['key']['remoteJid'].split('@')[0]
    push_name = data['data']['pushName']
    message = data['data']['message']['conversation']
    sender = data['sender'].split('@')[0]

    # Retorna os dados extraídos
    extracted_data = {
        "remote_jid": remote_jid,
        "push_name": push_name,
        "message": message,
        "sender": sender
    }

    return jsonify(extracted_data), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)