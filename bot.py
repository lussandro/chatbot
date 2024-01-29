from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Aqui você recebe os dados do webhook
    data = request.json

    # Exibe os dados recebidos no console do servidor
    print("Dados recebidos:", data)

    # Aqui você pode processar os dados e retornar uma resposta
    # Por enquanto, vamos apenas retornar um status de sucesso
    return jsonify({"status": "Recebido com sucesso"}), 200

if __name__ == '__main__':
    # Inicia o servidor na porta 5000
    app.run(host='0.0.0.0',port=5000, debug=True)
