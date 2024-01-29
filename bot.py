from flask import Flask, request, jsonify
import spacy
from chatterbot import ChatBot
from spacy.cli import download

download("en_core_web_sm")

class ENGSM:
    ISO_639_1 = 'en_core_web_sm'

app = Flask(__name__)

# Carregar o modelo de linguagem do spaCy para português


chatbot = ChatBot(
    "MeuChatBot",
    tagger_language=ENGSM
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
    print("Resposta do ChatterBot:", response) 
    return jsonify({"response": str(response)}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
