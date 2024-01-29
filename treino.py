from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Criação do ChatBot
chatbot = ChatBot("MeuChatBot")

# Treinamento do ChatBot
trainer = ChatterBotCorpusTrainer(chatbot)

# Aqui, você precisará especificar o caminho para os arquivos baixados
# Por exemplo: 'Caminho/para/o/arquivo/portuguese/conversations.yml'
trainer.train("Caminho/para/o/diretório/portuguese/")
