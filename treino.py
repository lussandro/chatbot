import spacy
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Carregar o modelo de linguagem do spaCy para português
nlp = spacy.load('pt_core_news_sm')

chatbot = ChatBot(
    "MeuChatBot",
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3',
    tagger_language=nlp  # Definir o idioma para português
)

# Resto do seu código...

trainer = ChatterBotCorpusTrainer(chatbot)

# Aqui, você precisará especificar o caminho para os arquivos baixados
# Por exemplo: 'Caminho/para/o/arquivo/portuguese/conversations.yml'
trainer.train("/root/chatbot/")
