import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

import pickle
import numpy as np
import tensorflow
from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random

intents = json.loads(open('job_intents.json', encoding='utf-8').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))


def clean_up_sentence(sentence):
    print("clean up sentence")
    sentence_words = nltk.word_tokenize(sentence)
    print(sentence_words)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    print("clean up sentence")
    print(sentence_words)
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    print("bow")
    print(sentence_words)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    print("predict class")
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    print(p)
    res = model.predict(np.array([p]))[0]
    print(res)
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
        
    print(return_list)
    return return_list


def getResponse(ints, intents_json):
    try:
        print("In get response")
        tag = ints[0]['intent']
        print("tag :", tag)
        list_of_intents = intents_json['intents']
        print("before if")
        if (tag != 'noresponse'):     
            for i in list_of_intents:
                print("i['tag']:",i['tag'])
                if(i['tag']== tag):
                    result = random.choice(i['responses'])
                    print(result)           
                    break
            return result
        elif (tag == 'noresponse'):
            return ('Sorry, I dont have answer to this question. You can either rephrase your question or ask me another one. Would you like to add this question in my dictionary?')              
        else:
            return ('Sorry, I dont have answer to this question. You can either rephrase your question or ask me another one. Would you like to add this question in my dictionary?')
    except Exception as e:
        print(e)
        return ('Sorry, I dont have answer to this question. You can either rephrase your question or ask me another one. Would you like to add this question in my dictionary?')
       # return ('Sorry ')


def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res

#-------------------------- trial ----------------------  
'''
def chat():
    print("Start talking with the bot (type quit to stop)!")
    while True:
        message =input("You: ")
        ints=predict_class(message,model)
        res=getResponse(ints,intents)
        print("res : ", res)

chat()
'''