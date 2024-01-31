from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Recebendo os dados do webhook
    data = request.json

    # Aqui você pode adicionar o tratamento dos dados recebidos
    print("Dados recebidos:", data)

    # Resposta de sucesso
    return jsonify({"message": "Dados recebidos com sucesso!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5000)
