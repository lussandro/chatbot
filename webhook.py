from flask import Flask, request
import threading
import time
from werkzeug.serving import make_server

app = Flask(__name__)

webhook_server = None
server_thread = None

# Duração de execução do servidor webhook em segundos (20 minutos = 1200 segundos)
RUN_TIME = 1200

class WebhookServer(threading.Thread):
    def __init__(self):
        super().__init__()
        self.srv = make_server('localhost', 5001, self.create_app())
        self.ctx = self.srv.app.app_context()
        self.ctx.push()

    def create_app(self):
        webhook_app = Flask(__name__)

        @webhook_app.route('/webhook', methods=['POST'])
        def webhook():
            data = request.json
            print("Dados recebidos:", data)
            return "Webhook received", 200

        return webhook_app

    def run(self):
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()

def start_webhook_server_for_limited_time():
    global webhook_server
    webhook_server = WebhookServer()
    webhook_server.start()
    # Espera pelo tempo definido antes de parar o servidor
    time.sleep(RUN_TIME)
    webhook_server.shutdown()

@app.route('/control')
def control():
    global server_thread
    if server_thread is None or not server_thread.is_alive():
        # Inicia o servidor webhook por um período limitado em um novo thread
        server_thread = threading.Thread(target=start_webhook_server_for_limited_time)
        server_thread.start()
        return "Webhook server activated for 20 minutes."
    else:
        return "Webhook server is already running."

def reset_thread():
    global server_thread
    server_thread = None

if __name__ == '__main__':
    app.run(port=5000, debug=True)
