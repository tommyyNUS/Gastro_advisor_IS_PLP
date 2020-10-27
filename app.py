import sys
from flask import Flask, request
import requests
import telegram
from constants import bot_token, bot_user_name,URL, GOOGLE_MAPS_API_KEY
import googlemaps
from datetime import datetime
from google.cloud import speech
from os import path, getcwd, environ

#Global variables
global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)
environ["GOOGLE_APPLICATION_CREDENTIALS"] = "secrets.json"
client = speech.SpeechClient()

#Initialize Chatbot
from chatbot.intent import check_intent,detect_intent
from chatbot.config import initialize
from chatbot.train_corpus import train_data

import spacy
import en_core_web_md

print("Initializing...")
chatbot = initialize()

#Check for Mode
global MODE
if (len(sys.argv) == 2): 
    if (sys.argv[1]=="-debug"): MODE = "DEBUG"
    elif (sys.argv[1]=="-train"): MODE = "TRAIN"
else: MODE = "TELEGRAM"

#Set Mode
if (MODE == "DEBUG"):
    nlp = spacy.load("en_core_web_md", disable=["ner"])
    print("Hello, you are in debug mode, how can i help you?")
    while 1:
        request = input("User: ")

        intent_detected,intent,obj,location,graded_aspect = detect_intent(nlp,request)
        if (intent_detected == 1): 
            response,dataframe_output = check_intent(intent,obj,location,graded_aspect)
            print(str(dataframe_output)) #this is the pandas dataframe output
        else: response = str(chatbot.get_response(request))

        print("Bot: ", response)
        if (intent=="ExitApp"): sys.exit()

elif (MODE == "TRAIN"): 
    train_data(chatbot)
    sys.exit()

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
            audio_file_object = bot.get_file(update.message.voice.file_id)
            audio_file_object.download('file.ogg')
            mypath = path.join(getcwd(), 'file.ogg')  
            
            #To process audio_file into text...
            # Loads the audio into memory
            ogg_audio = open(mypath, "rb")
            with ogg_audio as audio_file:
                content = audio_file.read()
                audio = speech.RecognitionAudio(content=content)
                
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
                sample_rate_hertz=48000,
                language_code="en-US"
                )
            
            # Detects speech in the audio file
            response = client.recognize(config=config, audio=audio)

            for result in response.results:
                print("Transcript: {}".format(result.alternatives[0].transcript))
                text = result.alternatives[0].transcript
    
    #Get response for restaurant recommendations
    intent_detected,intent,obj,location,graded_aspect = detect_intent(nlp,text)
    
    if (intent_detected == 1): 
        response,dataframe_output = check_intent(intent,obj,location,graded_aspect)
        print(str(dataframe_output)) #this is the pandas dataframe output

        #print(dataframe_output.columns)
        #Loop through each entry in dataframe
        i=1
        for idx, row in dataframe_output.iterrows():
            full_address = row['rest_name'] + ", "+row['rest_address']
            print("Full address: "+full_address)
            
            place_json = getVenueDetails(full_address, row['rest_name'])
            
    
            if place_json is not None:
                print("--- Google JSON details ---")
                print(place_json)
                print()
            
                #Get various JSON details
                website = ""
                phoneNo = ""
                googReviewScore = ""
                openingHours_array = []
                address = ""
                photo_refs=[]
                openingHours = ""
                resName = place_json['result']['name']
                if 'international_phone_number' in place_json['result']: 
                    phoneNo = place_json['result']['international_phone_number']
            
                if 'website' in place_json['result']:
                    website = place_json['result']['website']
                if website == "":
                    if 'url' in place_json['result']:
                        website = place_json['result']['url']
            
                if 'rating' in place_json['result']:
                    googReviewScore = place_json['result']['rating']
                
                lat = place_json['result']['geometry']['location']['lat']
                long = place_json['result']['geometry']['location']['lng']
            
                if 'opening_hours' in place_json['result']: 
                    openingHours_array = place_json['result']['opening_hours']['weekday_text']
                    openingHours = ""
                    if len(openingHours_array) > 0:
                        for item in openingHours_array:
                            openingHours = openingHours + item+"\n"
                        
                if 'formatted_address' in place_json['result']:
                    address = place_json['result']['formatted_address']
                if 'photos' in place_json['result']:
                    photo_refs = place_json['result']['photos']
            
                print("Restaurant name: "+resName)        
                print("Phone Number: "+phoneNo)
                print("Website: "+website)
                print("Long: "+str(long)+", Lat: "+str(lat))        
                print("Opening hours\n")
                print(openingHours)
                print("Address: "+address)
            
                #Adding our ratings
                rest_overall_rating = str(round(float(row['w_rest_rating'])*5, 1))
                foodRating = str(round(float(row['rest_food_rating'])*5, 1))
                serviceRating = str(round(float(row['rest_srvc_rating'])*5, 1))
                priceRating = str(round(float(row['rest_prce_rating'])*5, 1))
                ambienceRating = str(round(float(row['rest_ambi_rating'])*5, 1))
             
                #Prepare message to send back to user
                #1. Text message
                bot_message = str(i)+". "+str(resName)+"\n"
                if phoneNo != "":
                    bot_message = bot_message + "Phone: "+str(phoneNo)+"\n"
                if website != "":
                    bot_message = bot_message + "Website: "+str(website)+"\n"
        
                bot_message = bot_message + "Google Review Score: "+str(googReviewScore)+"\n"
                bot_message = bot_message + "Gastrotomi Score: "+str(rest_overall_rating)+"\n"            
                bot_message = bot_message + "\n--- Gastrotomi Ratings ---\n"+"Food: "+str(foodRating)+"\n"+"Price: "+str(priceRating)+"\n"+"Service: "+str(serviceRating)+"\n"+"Ambience: "+str(ambienceRating)+"\n"
            
                if openingHours != "":
                    bot_message = bot_message + "\nOpening Hours: \n"+str(openingHours)
            
                sendTelegramMessage(chat_id, bot_message)
            
                #2. Location
                sendTelegramVenue(chat_id, lat, long, resName, address)
            
                #3. Photos
                photos = getVenuePhotos(photo_refs)
                sendTelegramMediaGroup(chat_id, photos)
                i+=1
        
        return 'ok'

    else: 
        response = str(chatbot.get_response(text))
        bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id)
        return 'ok'

def getVenueDetails(address, rest_name):
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
    place_json = gmaps.find_place(input_type='textquery', input=address)
    places = place_json['candidates']
    placeFound = False
    place_ids = []
    gmapsPlaces = []
    place_id = ""
    
    if len(places) > 0:
        for item in places:
            print("appending "+str(item['place_id']))
            place_ids.append(item['place_id'])
    
        if len(places) > 5:
            for idx, placeID in enumerate(place_ids):
                place = gmaps.place(placeID)
                gmapsPlaces.append(place)
                if idx == 5:
                    break
        else:
            for placeID in place_ids:
                place = gmaps.place(placeID)
                print("Appending place: "+str(place['result']['name']))
                gmapsPlaces.append(place)
                print("Length of google places: "+str(len(gmapsPlaces)))    
        for gmapPlace in gmapsPlaces:
            print("Comparing "+rest_name+", with "+gmapPlace['result']['name'])
            if rest_name.lower() in gmapPlace['result']['name'].lower():
                print("Place found for "+rest_name)
                return gmapPlace
            
        if placeFound is False:
            print("Place not found for "+rest_name)
            return gmapsPlaces[0]

def getVenuePhotos(photo_refs):
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
    photos = []
    for idx, ref in enumerate(photo_refs):
        if idx == 5:
            break
        photo_ref = ref['photo_reference']
        photo_raw = gmaps.places_photo(photo_reference=photo_ref, max_width=300, max_height=300)
        f = open("placeImage"+str(idx)+".jpg", "wb")
        
        for chunk in photo_raw:
            if chunk:
                f.write(chunk)
        f.close()
                
        photos.append("placeImage"+str(idx)+".jpg")
    
    return photos

def sendTelegramMessage(chat_id, bot_message):
    try:
        response = bot.sendMessage(chat_id=chat_id, text=bot_message, disable_web_page_preview=True, parse_mode="html")
    except Exception as ex:
        print("Telegram text error...")
        print(ex)    

def sendTelegramVenue(chat_id, lat, long, resName, address):
    try:
        response = bot.sendVenue(chat_id=chat_id, latitude=lat, longitude=long, title=resName,address=address, disable_notification=True)
    except Exception as ex:
        print("Telegram venue error...")
        print(ex)

def sendTelegramMediaGroup(chat_id, photos):
    imgArray = []
    try:
        if len(photos) > 5:
            for i in range(0,5):
                photo = telegram.InputMediaPhoto(media=open(photos[i], 'rb'),caption=None)
                imgArray.append(photo)
        else:
            for i in range(0,len(photos)):
                photo = telegram.InputMediaPhoto(media=open(photos[i], 'rb'),caption=None)
                imgArray.append(photo)
        response = bot.sendMediaGroup(chat_id=chat_id, media=imgArray, disable_notification=True)
    except Exception as ex:
        print("Telegram group photo error...")
        print(ex)
        
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
