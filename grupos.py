import requests
import json
from time import sleep
# Parte 1: Obter os IDs dos grupos
url_fetch = 'https://api.chatcoreapi.io/group/fetchAllGroups/chatcore?getParticipants=false'
headers_fetch = {'apikey': '1A3E9771-93E6-41A1-B068-E113E07DD185'}

response = requests.get(url_fetch, headers=headers_fetch)
if response.status_code == 200:
    groups_data = response.json()
    group_ids = [group["id"] for group in groups_data]
    
else:
    print("Erro ao buscar os grupos")
    group_ids = []


def enviar_mensagem(telefone):


    url = 'https://api.chatcoreapi.io/message/sendText/chatcore'
    payload = {
    "number": telefone,
    "options": {
        "delay": 1200,
        "presence": "composing",
        "mentions": {
            "everyOne": True
        }
    },

    "textMessage": {
        "text": "A noite é uma criança!!!"
    }
}
    headers = {
        'accept': 'application/json',
        'apikey': 'B6D711FCDE4D4FD5936544120E713976',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=payload, headers=headers)

    return response

for group_id in group_ids:
    enviar_mensagem(group_id)
    print("Aguardando 3 s")
    print(group_id)
    sleep(3)
    print(response)
    