from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contatos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(80), unique=True, nullable=False)
    nome = db.Column(db.String(120), nullable=False)
    instancia = db.Column(db.String(120), nullable=False)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Dados recebidos:", data)

    remote_jid = data['data']['key']['remoteJid'].replace('@s.whatsapp.net', '')
    message = data['data']['message']['conversation']
    push_name = data['data']['pushName']
    sender = data['sender']

    # Verificando se o contato já existe
    contato_existente = Contato.query.filter_by(numero=remote_jid).first()
    if not contato_existente:
        novo_contato = Contato(numero=remote_jid, nome=push_name, instancia=sender)
        db.session.add(novo_contato)
        db.session.commit()
        print("Contato adicionado:", novo_contato.numero, novo_contato.nome, novo_contato.instancia)
    else:
        print("Contato já existe:", contato_existente.numero, contato_existente.nome, contato_existente.instancia)

    return jsonify({"message": "Dados recebidos e processados com sucesso!"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
