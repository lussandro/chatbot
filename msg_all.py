import requests

# Função para obter os IDs dos grupos
def obter_ids_grupos():
    url = 'https://api.chatcoreapi.io/group/fetchAllGroups/chatcore?getParticipants=false'
    headers = {'apikey': '1A3E9771-93E6-41A1-B068-E113E07DD185'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        dados_api = response.json()
        return [grupo['id'] for grupo in dados_api]
    else:
        print(f"Falha ao chamar a API de grupos: Código de status {response.status_code}")
        return []

# Função para obter os participantes de um grupo
def obter_participantes_grupo(id_grupo):
    url = f'https://api.chatcoreapi.io/group/participants/chatcore?groupJid={id_grupo}'
    headers = {'apikey': '1A3E9771-93E6-41A1-B068-E113E07DD185'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        participantes = response.json()
        return [part['id'].replace('@s.whatsapp.net', '') for part in participantes.get('participants', [])]
    else:
        print(f"Falha ao obter participantes do grupo {id_grupo}: Código de status {response.status_code}")
        return []

# Obter IDs dos grupos
ids_grupos = obter_ids_grupos()

# Se houver IDs de grupos, obter participantes
if ids_grupos:
    # Lista para armazenar todos os contatos
    contatos = []

    # Obter contatos de cada grupo
    for id_grupo in ids_grupos:
        participantes = obter_participantes_grupo(id_grupo)
        contatos.extend(participantes)

    # Salvando os contatos no arquivo contatos.txt
    with open('contatos.txt', 'w') as arquivo_contatos:
        for contato in contatos:
            arquivo_contatos.write(contato + '\n')

    print("Contatos salvos no arquivo contatos.txt")
else:
    print("Nenhum ID de grupo foi encontrado.")
