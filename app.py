import sys
from flask import Flask, request
import requests
import telegram
from constants import bot_token, bot_user_name,URL

#Global variables
global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

#Initialize Chatbot
from chatbot.intent import check_intent,detect_intent
from chatbot.config import initialize
from chatbot.train_corpus import train_data

import spacy
import en_core_web_md

print("Initializing...")
chatbot = initialize()

#Check for Mode
#global MODE
#if (len(sys.argv) == 2): 
#    if (sys.argv[1]=="-debug"): MODE = "DEBUG"
#    elif (sys.argv[1]=="-train"): MODE = "TRAIN"
#else: MODE = "TELEGRAM"

#Set Mode
#if (MODE == "DEBUG"):
#    nlp = spacy.load("en_core_web_md", disable=["ner"])
#    print("Hello, you are in debug mode, how can i help you?")
#    while 1:
#        request = input("User: ")

#        intent_detected,intent,obj,location,graded_aspect = detect_intent(nlp,request)
#        if (intent_detected == 1): response = check_intent(intent,obj,location,graded_aspect)
#        else: response = chatbot.get_response(request)

#        print("Bot: ", response)
#        if (intent=="ExitApp"): sys.exit()

#elif (MODE == "TRAIN"): 
#    train_data(chatbot)
#    sys.exit()

nlp = spacy.load("en_core_web_md", disable=["ner"])
chatbot = initialize()
print("Chatbot Ready.")


app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    text = ""
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    print(update.message)
    
    if update.message.text != None:
        text = update.message.text.encode('utf-8').decode()
    if update.message.voice != None:
        if update.message.voice.file_id != None:
            file_id = update.message.voice.file_id
            audio_file_object = bot.get_file(file_id)
            file_path = audio_file_object['file_path']
            audio_file = requests.get(file_path).content
            #with open('output.wav', 'wb') as out:
            #    out.write(audio_file)
            #To process audio_file into text...
    
    #Get response for restaurant recommendations
    intent_detected,intent,obj,location,graded_aspect = detect_intent(nlp,text)

    if (intent_detected == 1): response = str(check_intent(intent,obj,location,graded_aspect))
    else: response = str(chatbot.get_response(text))
	
    #Prepare message to send back to user
    bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id)

    return 'ok'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/')
def index():
    return 'I am running flask server locally...'

if __name__ == '__main__':
    app.run(threaded=True)
