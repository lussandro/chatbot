from flask import Flask, request, jsonify, render_template, redirect, url_for, render_template_string
from werkzeug.serving import make_server
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests, json, random, time, redis, threading
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contatos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

respostas_ativas = False


class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(80), unique=True, nullable=False)
    nome = db.Column(db.String(120), nullable=False)
    instancia = db.Column(db.String(120), nullable=True)

class Grupo(db.Model):
    id = db.Column(db.String(120), primary_key=True)
    subject = db.Column(db.String(120), nullable=False)

class Config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    msg_count = db.Column(db.Integer, default=0)  
    msg_sent = db.Column(db.Integer, default=1)
    msg_group = db.Column(db.Integer, default=1)
    msg_old = db.Column(db.String(120), nullable=True)
    instancia = db.Column(db.String(120), nullable=True)
    url_api = db.Column(db.String(120), nullable=True)
    apikey = db.Column(db.String(120), nullable=True)

class Bot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    numero = db.Column(db.String(15), unique=True, nullable=False)

load_dotenv()

r = redis.Redis(host='95.217.10.252', port=6379, db=0)
def carregar_frases():
    with open('frases.txt', 'r', encoding='utf-8') as arquivo:
        frases = arquivo.readlines()
    return [frase.strip() for frase in frases]

def carregar_bots():
    with open('bots.txt', 'r', encoding='utf-8') as arquivo:
        bots = arquivo.readlines()
    return [bot.strip() for bot in bots]



def enviar_mensagem(telefone,mensagem):
    
    dados = json.dumps({"telefone": telefone, "mensagem": mensagem})
    
  
    r.lpush('fila_de_mensagens', dados)    

@app.route('/control', methods=['GET'])
def control():
    global respostas_ativas
    if not respostas_ativas:
        respostas_ativas = True
        print("Respostas do webhook ativadas por 20 minutos.")
       
        timer = threading.Timer(1200, desativar_respostas)
        timer.start()
        return render_template('maturacao.html')
    else:
        return render_template('maturacao.html')


def reset_thread():
    global server_thread
    server_thread = None

@app.route('/')
def index():
    instancia = os.environ.get("INSTANCE_NAME")
    apikey = os.environ.get("API_KEY")
    url = os.environ.get("API_URL")
    total_grupos = Grupo.query.count()
    total_contatos = Contato.query.count()
    with open('bots.txt', 'r') as arquivo:
        total_bots = sum(1 for linha in arquivo)

    config = Config.query.first()
    msg_count = config.msg_count if config else 0
    msg_sent = config.msg_sent if config else 0
    msg_group = config.msg_group if config else 0
    return render_template('index.html', total_grupos=total_grupos, total_contatos=total_contatos, msg_count=msg_count, total_bots=total_bots, msg_sent=msg_sent, msg_group=msg_group, instancia=instancia, apikey=apikey, url=url)

@app.route('/obter-qrcode')
#@login_required
def obter_qrcode():
    instancia = os.environ.get("INSTANCE_NAME")  # Captura o parâmetro de consulta
    api_key = os.environ.get("API_KEY")
    api_url = os.environ.get("API_URL") + '/instance/connect/' + instancia
    headers = {'apikey': api_key}
    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()  # Irá lançar um erro HTTPError se o status não for 200
        data = response.json()
        qrcode_base64 = data.get('base64')
        if qrcode_base64:
            return render_template('qrcode.html', qrcode_base64=qrcode_base64)
        else:
            return render_template('error.html', message="Não foi possível obter o QR Code.")
    except requests.exceptions.RequestException as e:
        # Trate os erros de requisição como achar necessário
        return render_template('error.html', message=str(e))
# @app.route('/iniciar-maturacao', methods=['GET'])
# def iniciar_maturacao():
#     bots = carregar_bots()
#     for bot in bots:
#         enviar_mensagem(bot, "olá, tudo bem?")  # Substituir pela mensagem desejada
#         intervalo = random.randint(1, 27)
#         time.sleep(intervalo)  # Espera um intervalo aleatório entre 1 a 27 segundos
#     return jsonify({"status": "Mensagens enviadas com sucesso para todos os bots!"}), 200

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
        response = requests.put('https://api.chatcoreapi.io/chat/updateProfilePicture/teste3', headers=headers, json=data)

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
    
    if respostas_ativas:
        data = request.json
        print(data)

        remote_jid = data['data']['key']['remoteJid'].replace('@s.whatsapp.net', '')
        message = data['data']['message'].get('conversation')
        push_name = data['data']['pushName']
        sender = data['sender'].replace('@s.whatsapp.net', '')
        grupo = data.get('data', {}).get('key', {}).get('remoteJid', '')
        if '@g.us' in grupo:
            config = Config.query.first()
            if  config is None:
                config = Config(msg_group = 1)
                db.session.add(config)
            else:
                config.msg_group += 1
            db.session.commit()

        if message:
            config = Config.query.first()
            frases = carregar_frases()
            mensagem = random.choice(frases)
            enviar_mensagem(remote_jid, mensagem)
            
            if not config:
                config = Config(msg_count=1)
                config = Config(msg_sent=1)
                
                db.session.add(config)
            else:
                config.msg_count += 1
                config.msg_sent += 1
                
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
    else:
        return jsonify({"status": "inactive", "message": "Webhook inativo. Dados recebidos, mas não processados."}), 200

def desativar_respostas():
    global respostas_ativas
    respostas_ativas = False
    print("Respostas desativadas.")


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
