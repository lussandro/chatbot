# Use a imagem oficial do Python como base
FROM python:3.8.10

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie os arquivos de código-fonte da sua aplicação para o contêiner
COPY . /app

RUN pip install --upgrade pip
# Instale as dependências do Flask (você pode criar um arquivo requirements.txt)
RUN pip install -r requirements.txt

# Exponha a porta que sua aplicação Flask irá utilizar (geralmente 5000)
EXPOSE 5000

# Comando para iniciar sua aplicação Flask
CMD ["python", "bot.py"]
