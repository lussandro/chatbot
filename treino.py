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


trainer = ChatterBotCorpusTrainer(chatbot)


trainer.train("/root/chatbot/yml/greetings.yml")
