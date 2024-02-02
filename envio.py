import redis
import json

# Configuração do cliente Redis
r = redis.Redis(host='localhost', port=6379, db=0)

def enfileirar_mensagem(telefone, mensagem):
    # Prepara os dados para enfileirar
    dados = json.dumps({"telefone": telefone, "mensagem": mensagem})
    
    # Enfileira a mensagem na lista do Redis
    r.lpush('fila_de_mensagens', dados)

enfileirar_mensagem('5548998677302', 'oolaaaa')