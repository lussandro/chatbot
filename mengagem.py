import requests
import random
import time

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
            "text": "Oieee, fazendo qoue de bom?"
        }
    }
    headers = {
        'accept': 'application/json',
        'apikey': 'B6D711FCDE4D4FD5936544120E713976',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=payload, headers=headers)
    return response

# Lê os números do arquivo contatos.txt
try:
    with open('contatos.txt', 'r') as arquivo:
        contatos = arquivo.read().splitlines()
except FileNotFoundError:
    print("Arquivo contatos.txt não encontrado.")
    contatos = []

# Envia mensagens para os contatos
for telefone in contatos:
    resposta = enviar_mensagem(telefone)
    print(f"Mensagem enviada para {telefone}, resposta: {resposta.status_code}")
    
    # Delay aleatório entre 0 e 17 segundos
    tempo_espera = random.randint(1, 37)
    print(f"Aguardando {tempo_espera} segundos...")
    time.sleep(tempo_espera)

print("Todas as mensagens foram enviadas.")
