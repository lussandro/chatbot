from flask import Flask, request, jsonify
import spacy
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__)

# Carregar o modelo de linguagem do spaCy para português
nlp = spacy.blank('pt')

chatbot = ChatBot(
    "MeuChatBot",
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3'
    # Removendo a configuração do idioma e o tagger
)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Recebe os dados do webhook
    data = request.json

    # Extrai os dados específicos
    remote_jid = data['data']['key']['remoteJid'].split('@')[0]
    push_name = data['data']['pushName']
    message = data['data']['message']['conversation']
    sender = data['sender'].split('@')[0]

    response = chatbot.get_response(message)
    
    return jsonify({"response": str(response)}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
