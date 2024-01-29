from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot(
    "MeuChatBot",
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3',
    tagger_language='pt_core_news_sm'  # ou 'en_core_web_sm' para inglês
)

# Resto do seu código de treinamento...


# Treinamento do ChatBot
trainer = ChatterBotCorpusTrainer(chatbot)

# Aqui, você precisará especificar o caminho para os arquivos baixados
# Por exemplo: 'Caminho/para/o/arquivo/portuguese/conversations.yml'
trainer.train("/root/chatbot/")
