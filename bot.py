from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Recebendo os dados do webhook
    data = request.json
    
    # Extraindo os valores específicos
    remote_jid = data['data']['key']['remoteJid']
    message = data['data']['message']['conversation']
    sender = data['sender']

    # Imprimindo os valores
    print("remoteJid:", remote_jid)
    print("message:", message)
    print("sender:", sender)

    # Armazenando os valores (aqui você pode adicionar seu código de armazenamento)

    # Resposta de sucesso
    return jsonify({"message": "Dados recebidos e processados com sucesso!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5000)
