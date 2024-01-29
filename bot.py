from flask import Flask, request, jsonify
import spacy
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__)
nlp = spacy.load('pt_core_news_sm')

chatbot = ChatBot(
    "MeuChatBot",
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3',
    tagger_language='pt'  # Definir o idioma para português
)
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
    app.run(host='0.0.0.0',port=5000, debug=True)