import time
import random
import redis
import json
import requests
import os
from dotenv import load_dotenv

# Carregue as variáveis de ambiente do arquivo .env
load_dotenv()
instance_name = os.environ.get("INSTANCE_NAME")
def enviar_mensagem(telefone,mensagem):
    url = os.environ.get("API_URL") + instance_name
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
            "text": mensagem
        }
    }
    headers = {
        'accept': 'application/json',
        'apikey': 'B6D711FCDE4D4FD5936544120E713976',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=payload, headers=headers)
    return response

r = redis.Redis(host='95.217.10.252', port=6379, db=0)


def processar_e_enviar_mensagens():
    while True:
        # Verifica se há mensagens na fila
        dados = r.brpop('fila_de_mensagens', timeout=0)
        
        if dados:
            # Converte os dados de volta para um dicionário Python
            mensagem = json.loads(dados[1])
            telefone = mensagem['telefone']
            msg = mensagem['mensagem']
            # Simula o envio da mensagem (aqui você chamaria sua função `enviar_mensagem`)
            print(telefone)
            print(msg)
            enviar_mensagem(telefone, msg)
            print("Mensagem enviada")
            
            # Espera um período de tempo aleatório entre 1 e 60 segundos antes de processar a próxima mensagem
            time.sleep(random.randint(1, 60))

# Iniciar o worker
processar_e_enviar_mensagens()
