import spacy
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from spacy.cli import download

download("en_core_web_sm")

class ENGSM:
    ISO_639_1 = 'en_core_web_sm'


chatbot = ChatBot(
    "MeuChatBot",
    tagger_language=ENGSM
)
# Resto do seu código...

trainer = ChatterBotCorpusTrainer(chatbot)

# Aqui, você precisará especificar o caminho para os arquivos baixados
# Por exemplo: 'Caminho/para/o/arquivo/portuguese/conversations.yml'
trainer.train("/root/chatbot/")
