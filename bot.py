from flask import Flask, request, jsonify
import spacy
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__)
chatbot = ChatBot("MeuChatBot")
@app.route('/webhook', methods=['POST'])
def webhook():
    # Recebe os dados do webhook
    data = request.json
    #print("Dados recebidos:", data)

    # Extrai os dados específicos
    remote_jid = data['data']['key']['remoteJid'].split('@')[0]
    push_name = data['data']['pushName']
    message = data['data']['message']['conversation']
    sender = data['sender'].split('@')[0]

    response = chatbot.get_response(message)
    
    return jsonify({"response": str(response)}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)