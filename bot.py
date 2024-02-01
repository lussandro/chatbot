from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contatos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

webhook_logs = []

class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(80), unique=True, nullable=False)
    nome = db.Column(db.String(120), nullable=False)
    instancia = db.Column(db.String(120), nullable=False)

class Grupo(db.Model):
    id = db.Column(db.String(120), primary_key=True)
    subject = db.Column(db.String(120), nullable=False)

class Config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    msg_count = db.Column(db.Integer, default=0)  
    msg_sent = db.Column(db.Integer, default=0)

class Bot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    numero = db.Column(db.String(15), unique=True, nullable=False)

def carregar_frases():
    with open('frases.txt', 'r', encoding='utf-8') as arquivo:
        frases = arquivo.readlines()
    return [frase.strip() for frase in frases]

def enviar_mensagem(telefone,mensagem):
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
@app.route('/')
def index():
    total_grupos = Grupo.query.count()
    total_contatos = Contato.query.count()
    total_bots = Bot.query.count()
    config = Config.query.first()
    msg_count = config.msg_count if config else 0
    return render_template('index.html', total_grupos=total_grupos, total_contatos=total_contatos, msg_count=msg_count, total_bots=total_bots)

@app.route('/update_picture', methods=['POST'])
def update_picture():
    if request.method == 'POST':
        # Obter a URL da imagem do formulário
        new_picture_url = request.form.get('new_picture_url')

        # Configurar os cabeçalhos da solicitação
        headers = {
            'Content-Type': 'application/json',
            'apikey': '3mntbabbkufosmai26dwlm'
        }

        # Construir os dados da solicitação
        data = {
            'picture': new_picture_url
        }

        # Fazer a chamada PUT para atualizar a imagem do bot
        response = requests.put('https://api.chatcoreapi.io/chat/updateProfilePicture/chatwoot', headers=headers, json=data)

        # Verificar se a solicitação foi bem-sucedida
        if response.status_code == 200:
            # Imagem do bot atualizada com sucesso
            return "Imagem do bot atualizada com sucesso!"
        else:
            # Houve um erro na solicitação
            return "Erro ao atualizar a imagem do bot. Código de status: " + str(response.status_code)

        # Redirecionar de volta para a página principal após a atualização
    return redirect(url_for('index'))
@app.route('/add-bot', methods=['POST'])
def add_bot():
    nome = request.form['nome']
    numero = request.form['numero']
    # Validação simples do número para garantir que segue o formato desejado
    if not (numero.isdigit() and len(numero) == 13 and numero.startswith("55")):
        return jsonify({"error": "Número inválido. Use o formato 55XXXXXXXXXXX."}), 400

    # Verifica se o bot já existe
    existing_bot = Bot.query.filter_by(numero=numero).first()
    if existing_bot:
        return jsonify({"error": "Um bot com este número já existe."}), 400
    
    new_bot = Bot(nome=nome, numero=numero)
    db.session.add(new_bot)
    db.session.commit()
    return jsonify({"message": "Bot adicionado com sucesso!"}), 201

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print(data)

    remote_jid = data['data']['key']['remoteJid'].replace('@s.whatsapp.net', '')
    message = data['data']['message'].get('conversation')
    push_name = data['data']['pushName']
    sender = data['sender'].replace('@s.whatsapp.net', '')
        
    if message:
        config = Config.query.first()
        frases = carregar_frases()
        mensagem = random.choice(frases)
        enviar_mensagem(remote_jid, mensagem)
        if not config:
            config = Config(msg_count=1)
            db.session.add(config)
        else:
            config.msg_count += 1
        db.session.commit()

    # Tratamento de contatos
    contato_existente = Contato.query.filter_by(numero=remote_jid).first()
    if not contato_existente:
        novo_contato = Contato(numero=remote_jid, nome=push_name, instancia=sender)
        db.session.add(novo_contato)
    else:
       print("Contato já existe:", contato_existente.numero, contato_existente.nome, contato_existente.instancia)

    db.session.commit()
    return jsonify({"message": "Dados recebidos e processados com sucesso!"}), 200


@app.route('/fetch-groups', methods=['GET'])
def fetch_groups():
    response = requests.get('https://api.chatcoreapi.io/group/fetchAllGroups/chatwoot?getParticipants=false',
                            headers={'apikey': '3mntbabbkufosmai26dwlm'})
    
    if response.status_code == 200:
        groups = response.json()
        for group in groups:
            # Verifica se o grupo já existe no banco de dados
            if not Grupo.query.get(group['id']):
                novo_grupo = Grupo(id=group['id'], subject=group['subject'])
                db.session.add(novo_grupo)
        
        db.session.commit()
        return jsonify({"message": "Grupos atualizados com sucesso!"}), 200
        
    else:
        return jsonify({"error": "Falha ao buscar grupos"}), response.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5000)
