from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot(
    "MeuChatBot",
    tagger_language="en_core_web_sm"  # Usar o nome completo do modelo spaCy
)


# Treinamento do ChatBot
trainer = ChatterBotCorpusTrainer(chatbot)

# Aqui, você precisará especificar o caminho para os arquivos baixados
# Por exemplo: 'Caminho/para/o/arquivo/portuguese/conversations.yml'
trainer.train("/root/chatbot/")
