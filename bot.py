from flask import Flask, request, jsonify
import spacy
from chatterbot import ChatBot

from spacy.cli import download
import requests

download("en_core_web_sm")

class ENGSM:
    ISO_639_1 = 'en_core_web_sm'

app = Flask(__name__)

# Carregar o modelo de linguagem do spaCy para português


chatbot = ChatBot(
    "MeuChatBot",
    tagger_language=ENGSM
)
def enviar_mensagem(telefone, texto):


    url = 'https://api.chatcoreapi.io/message/sendText/chatcore'
    payload = {
        'number': telefone,
        'textMessage': {'text': texto},
        'options': {
            'delay': 0,
            'presence': 'composing',
            'linkPreview': True,
            'quoted': None
        }
    }
    headers = {
        'accept': 'application/json',
        'apikey': 'B6D711FCDE4D4FD5936544120E713976',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.ok

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

    enviar_mensagem(remote_jid, response)
    print("Resposta do ChatterBot:", response) 
    return jsonify({"response": str(response)}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
