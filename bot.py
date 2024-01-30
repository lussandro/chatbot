from flask import Flask, request, jsonify
import spacy
from chatterbot import ChatBot
import json
from spacy.cli import download
import requests
from time import sleep

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
    sleep(5)
    enviar_mensagem(remote_jid, response, sender)
    print("Resposta do ChatterBot:", response) 
    return jsonify({"response": str(response)}), 200
def enviar_mensagem(telefone, texto, sender):


    url = 'https://api.chatcoreapi.io/message/sendText/'+str(sender)
    payload = {
        'number': telefone,
        'textMessage': {'text': str(texto)},
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
@app.route('/capturagrupos', methods=['GET'])
def captura_grupos(instancia):
    instancia = 'chatcore'

    url = 'https://api.chatcoreapi.io/group/fetchAllGroups/'+ instancia +'?getParticipants=false'
  
    headers = {
        'accept': 'application/json',
        'apikey': 'B6D711FCDE4D4FD5936544120E713976',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        groups_data = response.json()
        
        for group in groups_data:
            print(group)
            
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
