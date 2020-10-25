from datetime import datetime
from database.restaurant_query import get_restaurant

def check_intent(intent,obj,location,graded_aspect):
    if (intent == "GetTime"): 
        dt=datetime.now().strftime('%A %Y-%m-%d %H:%M:%S %p')
        response = f'Currently, it is {dt}'
        return response,""
    elif (intent == "ExitApp"): 
        response = 'Bye! Have a nice day!'
        return response,""
    elif (intent == "GetFood"): 
        response = f'Looking for {obj} restaurants with the best {graded_aspect} in the {location} of Singapore?' 
        return response,get_restaurant(obj,location,graded_aspect)

def detect_intent(model,request):
    request = request.lower()

    for x in ["bye","byebye","good bye","goodbye","see you","cya","ciao","exit"]: 
        if (request == x):
            intent = "ExitApp"
            print("Intent Detected - ", intent)
            intent_detected = 1

            return intent_detected,intent,"","",""

    subj,pred,obj,location,graded_aspect = extract_triple (model,request)

    if (~(detect_keyword(["recommendation","recommend"],pred) ^ detect_keyword(["u","you"],subj))): predicate_grammar = True 
    elif (~(detect_keyword(["recommendation"],pred) ^ detect_keyword(["i"],subj))): predicate_grammar = True 
    else: predicate_grammar = False

    get_time_condition = detect_keyword(["time","day","date"],obj)
    get_food_condition = detect_keyword(["eat","recommend","find","get","crave","want","wan","hungry","suggest","have","serve","look","recommendation","recommendations"],pred)
    if get_time_condition: 
        intent = "GetTime"
        intent_detected = 1
    elif get_food_condition and predicate_grammar:
        intent = "GetFood"
        intent_detected = 1
    else:
        intent = "None"     
        intent_detected = 0

    print("Intent Detected - ", intent)   

    if (len(location)==0): location = "whole"
    if (len(obj)==0): obj = "any"
    
    return intent_detected,intent,obj,location,graded_aspect

def remove_stopwords(textarray):
    for stopwords in ["a ","the ","good ","best ","delicious ","some ","marvellous ","fantastic ","decent ","nice "," side","very "," food"," restaurant"," restaurants"," cuisine","any ",","," any ","what "]: 
        textarray[:] = [x.replace(stopwords,"") for x in textarray]
    textarray[:] = [x.replace("town","central") for x in textarray]

    for stopwords in ["place","me","you","restaurant","singapore","something","food","foods","eat","listen"]:
        if stopwords in textarray: textarray.remove(stopwords)

    return textarray

def get_location(obj):
    location = []
    wordlist = ["north","south","east","west","northeast","north east","north-east","central"]
    for x in wordlist:
        if x in obj:
            obj.remove(x)
            location.append(x)
    return obj,location

def get_graded_aspect(obj):
    graded_aspect = ["food"] #food is by default
    wordlist_ambience = ["ambience","music","environment","peaceful","quiet","cozy"]
    wordlist_service = ["service","kind staff","gentle staff","friendly","friendly staff","homely","welcoming","kind staffs","gentle staffs","friendly staffs"]
    wordlist_price = ["price","cheapest","cheap","inexpensive"]
    if (len(obj) != 0):
        for x in wordlist_ambience:
            if x in obj:
                obj.remove(x)
                graded_aspect.append("ambience")
            elif any((obj[y[0]].find(f'{x} ') != -1) for y in enumerate(obj)):
                obj[:] = [y.replace(f'{x} ',"") for y in obj]
                graded_aspect.append("ambience")    
        for x in wordlist_service:
            if x in obj:
                obj.remove(x)
                graded_aspect.append("service")
            elif any((obj[y[0]].find(f'{x} ') != -1) for y in enumerate(obj)):
                obj[:] = [y.replace(f'{x} ',"") for y in obj]
                graded_aspect.append("service")      
        for x in wordlist_price:
            if x in obj:
                obj.remove(x)
                graded_aspect.append("price")    
            elif any((obj[y[0]].find(f'{x} ') != -1) for y in enumerate(obj)):
                obj[:] = [y.replace(f'{x} ',"") for y in obj]
                graded_aspect.append("price")  
        return obj,graded_aspect
    else: return obj,["food"]

def reassign_triple(source,target,wordlist):
    for x in wordlist: 
        if x in source: 
            source.remove(x)
            target.append("recommendation")
    return source,target

def extract_triple(model,sentence):
    subj,pred,obj=[],[],[]
    location=[]

    #Special Food Rules
    sentence,found_special_food = detect_specialfood(sentence,obj)

    doc = model(sentence)

    #Account for NGram where N > 1
    for noun_phrase in list(doc.noun_chunks):
        noun_phrase.merge(noun_phrase.root.tag_, noun_phrase.root.lemma_, noun_phrase.root.ent_type_)
    #print([(X.text,X.idx,X.pos_,X.dep_,X.tag_) for X in doc])

    for X in doc: 
        if (X.dep_ == 'nsubj' or X.pos_ == 'PRON' or X.pos_ == 'DET'): subj.append(X.text)
        if (X.pos_ == 'VERB' or X.dep_ == 'acomp'): pred.append(X.lemma_)
        if (X.dep_ == 'dobj' or X.dep_ == 'pobj' or X.dep_ == 'compound' or X.dep_ == 'conj' or X.dep_ == 'attr' or X.dep_ == 'nsubj'
            and X.pos_=='NOUN' or X.tag_ == 'NNS'): obj.append(X.text) 
    #print (subj,pred,obj)
    #subject,predicate,object
    obj,pred = reassign_triple(remove_stopwords(obj),pred,["recomndations","recomndation","recommendations","recommendation","suggestions","suggestion"," recomndations"," recomndation"," recommendations"," recommendation"," suggestions"," suggestion"])
    obj,location = get_location(obj)

    #lemmatize all objects before search
    exclusion=["fries","fried","steamed","salted","mashed","suckling","scrambled","grilled","smoked","roasted","poached","braised","starred"]
    for x in obj: 
        lemma = ""
        doc2=model(x)
        for y in enumerate(doc2): 
            if (y[0] == 0): 
                if (detect_keyword(exclusion,y[1].text)==0): lemma = y[1].lemma_
                else: lemma = y[1].text
            else: 
                if (detect_keyword(exclusion,y[1].text)==0): lemma = lemma + " " + y[1].lemma_
                else: lemma = lemma + " " + y[1].text
        obj[:] = [z.replace(x,lemma) for z in obj]

    #put back food with special name (don't want to lemmatize)
    if len(found_special_food) != 0: 
        for x in found_special_food: obj.append(x) 
    obj,graded_aspect = get_graded_aspect(obj)


    print ("Triples Extracted: ",subj,pred,obj)

    return (subj,pred,obj,location,graded_aspect)

def detect_keyword(searchterms,item):
    array = []
    for x in searchterms: array.append(x in item)
    return any(array)

def detect_specialfood(sentence,obj):
    replacefoodname = [["french fries","fries"],["fish and chips","fish"],["fish and chip","fish"]]
    specialfoodlist = ["bak kut teh","fish head curry","curry fish head","cod fish","cod","chendol","satays","otak","sushi","fast food","fries","ramen","salted egg yolk","salted egg"]
    found = [] 
    for x in replacefoodname:
        if (sentence.find(x[0]) != -1): sentence = sentence.replace(x[0],x[1])

    for x in specialfoodlist:
        if (sentence.find(x) != -1): 
            sentence = sentence.replace(x,"food")
            found.append(x)
    return sentence,found