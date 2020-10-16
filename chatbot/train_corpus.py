from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer

def train_data(chatbot):

    trainer = ChatterBotCorpusTrainer(chatbot)

    #standard library
    trainer.train("chatterbot.corpus.english.greetings")
    trainer.train("chatterbot.corpus.english.conversations")
    trainer.train("chatterbot.corpus.english.humor")
    trainer.train("chatterbot.corpus.english.botprofile")
    trainer.train("chatterbot.corpus.english.ai")
    trainer.train("chatterbot.corpus.english.emotion")

    trainer = ListTrainer(chatbot)

    #library addons
    thank_addons = ["Thank You","You're Welcome","Thanks","You're Welcome"]
    hello_addons = ["Hello there","Hello, how are you?","I'm fine","That's good to hear!","I am fine","That's good to hear!","I'm doing well","That's good to hear!","I am doing well","That's good to hear!"]
    joke_addons = ["ha ha", "hahaha","haha", "hahaha", "hahaha", "lol","rofl", "lmao", "lmao","hahaha"]
    task_addons = ["what is your function","i recommend the best food to people!","what do you do","i recommend the best food to people!"]

    trainer.train(thank_addons)
    trainer.train(hello_addons)
    trainer.train(joke_addons)
    trainer.train(task_addons)