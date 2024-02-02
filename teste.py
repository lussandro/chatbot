import os
from dotenv import load_dotenv

# Carregue as variáveis de ambiente do arquivo .env
load_dotenv()

# Acesse as variáveis de ambiente usando 'os.environ'
api_key = os.environ.get("API_KEY")
debug = os.environ.get("DEBUG")
database_url = os.environ.get("DATABASE_URL")

# Exemplo de uso das variáveis de ambiente
if debug == "True":
    print("Modo de depuração ativado")

print(f"API Key: {api_key}")
print(f"Database URL: {database_url}")
