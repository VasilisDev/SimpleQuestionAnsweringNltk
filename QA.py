
"""
@author:Vasileios Tsakiris
"""

import os
import sys
import random
import time
import nltk
import string
import re
from nltk.stem import PorterStemmer
ps = PorterStemmer()
from nltk.corpus import wordnet


BOTNAME = "CrazyBot"

CONTRACTION_MAP = {
"don't": "do not",
}

#keywords list
MISUND_RESPONSES = ["Sorry sir ,i cannot understand you.","Sorry?","I am not so clever at this point.Sorry about that!"]
HOWRU_RESP = ["i am good thanks.And you?","I am fine.What about you?","Well,you?"]
GREETINGS = ["hi","hello","hey"]
MENU = ["pizza","eggs","greek souvlaki","chicken","burger"]
GREET_RESPONSES = ["Hey!","Hi!","Hi there!","Hello","What's up?","Hey friend",]
HOWRU = ["how are you","how r u","how are you doing","how are you doing today","how is your day going"]
HOWRU_RESP_HAPPY = ["fine","well","good","me too"]
GOODBYE = ["bye","goodbye","bye bye","see ya","sweet dreams","good night"]
REQ_MENU = ["menu"]
REQ_FINAL = ["ok","yes","yeah","sure","want"]
REQ_FINAL_MINUS = ["no","nope", "do not"]
ADDR = ["str","street","road"]
GOODBYE_RESP = ["Goodbye","Bye bye!","Bye!","See you","See you later","Ciao"]


#check if the sentence contains a keyword from one of the matched list above
def check_membership_howru(user_msg, user_kwds):

        user_msg = preprocess(user_msg)

        for msg in user_kwds:
            if msg in user_msg:
                return True
                break
            else:
                return False
#ready to tokenize the text
def tokenize_text(text):
    tokens = nltk.word_tokenize(text)
    tokens = [token.strip() for token in tokens]
    return tokens
#remove special characters set true to the keep_apostrophes if you words with apostrophes
def remove_characters_before_tokenization(sentence,keep_apostrophes=False):
     sentence = sentence.strip()
     if keep_apostrophes:
         PATTERN = r'[?|$|&|*|%|@|(|)|~]' # add other characters here to remove them
         filtered_sentence = re.sub(PATTERN, r'', sentence)
     else:
         PATTERN = r'[^a-zA-Z0-9 ]' # only extract alpha-numeric characters
         filtered_sentence = re.sub(PATTERN, r'', sentence)
     return filtered_sentence
#expand contraction from the object CONTRACTION_MAP
def expand_contractions(sentence, contraction_mapping):

    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())),
                                      flags=re.IGNORECASE|re.DOTALL)
    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match)\
                                if contraction_mapping.get(match)\
                                else contraction_mapping.get(match.lower())
        expanded_contraction = first_char+expanded_contraction[1:]
        return expanded_contraction

    expanded_sentence = contractions_pattern.sub(expand_match, sentence)
    return expanded_sentence

#function for remove repeated keywords
def remove_repeated_characters(tokens):
    repeat_pattern = re.compile(r'(\w*)(\w)\2(\w*)')
    match_substitution = r'\1\2\3'
    def replace(old_word):
        if wordnet.synsets(old_word):
            return old_word
        new_word = repeat_pattern.sub(match_substitution, old_word)
        return replace(new_word) if new_word != old_word else new_word

    correct_tokens = [replace(word) for word in tokens]
    return correct_tokens
#preprocession before check if the word is member
def preprocess(user_msg):

    #remove punctuation
    user_msg = remove_characters_before_tokenization(user_msg,keep_apostrophes=True)
    #expanf contraction for clearer meaning of the sentence and find the keyword easier
    user_msg = expand_contractions(user_msg,CONTRACTION_MAP)
    #tokenize the sentence first
    user_msg = nltk.sent_tokenize(user_msg)
    user_msg = user_msg[0]
    user_msg = "".join(user_msg)
    #convert the whole message to lowercase
    user_msg = user_msg.lower()
    return user_msg

#check if the input string contains a keyword from a list
def check_membership(user_msg, user_kwds):

    user_msg = preprocess(user_msg)
    user_msg=tokenize_text(user_msg)
    user_msg = remove_repeated_characters(user_msg)
    user_msg =' '.join(user_msg)
    user_msg_lemma= ps.stem(''.join(user_msg))

    for msg in user_kwds:
        if len(msg.split()) == 1 :
            user_msg_lst_lemma = tokenize_text(user_msg_lemma)
            if msg in user_msg_lst_lemma:
                return True
                break
        elif msg in user_msg_lemma:
            return True
            break
    return False


def addspace():

    if len(YOURNAME) < len(BOTNAME):
        space = " " * (len(BOTNAME) - len(YOURNAME))
        return {"user_msg": space, "r": ""}
    elif len(YOURNAME) > len(BOTNAME):
        space = " " * (len(YOURNAME) - len(BOTNAME))
        return {"user_msg": "", "r": space}
    return {"user_msg": "", "r": ""}

def convert(s):
    # initialization of string to ""
    new = ""
    # traverse in the string
    for x in s:
        new += x + '\n\t   '
    # return string
    return new

def respond(response):

    print(BOTNAME + " {}>  ...".format(addspace()["r"]))
    time.sleep(1)
    print(BOTNAME + " {}>  {}".format(addspace()["r"], response))

if __name__ == "__main__":
    print("===========================================================\n")
    print("\tWelcome to e-ordering\n")
    print("============================================================")
    YOURNAME = input("What's your name?\n")

    GREETING = respond("Hey {}, what's up? I am CrazyBot, welcome to the chat!\
    \n\t   I' am grateful that you chose our restaurant to order!".format(YOURNAME))

    prev_reply = ["", "", ""]

    while True:

        user_msg = input("{} {}>  ".format(YOURNAME, addspace()["user_msg"]))


        if check_membership_howru(user_msg, HOWRU):
            response = random.choice(HOWRU_RESP)
            respond(response)
        elif check_membership(user_msg, GREETINGS):
            response = random.choice(GREET_RESPONSES)
            respond(response)
        elif check_membership(user_msg, GOODBYE):
            response = random.choice(GOODBYE_RESP)
            respond(response)
            sys.exit()
        elif check_membership(user_msg, REQ_MENU):
            response = convert(MENU)
            respond(response)
        elif check_membership(user_msg, MENU):
            response = "Hm nice choice! Do you want some bread sir?"
            respond(response)
        elif check_membership(user_msg, REQ_FINAL):
            response = "Ok sir!To close the ordering tell me your address."
            respond(response)
        elif check_membership(user_msg, REQ_FINAL_MINUS):
            response = "Ok sir no problem!To close the ordering tell me your address."
            respond(response)
        elif check_membership(user_msg, ADDR):
            response = "Great!Your order will be at "+ str(user_msg) +" in "+ str(random.randint(10, 30)) +" minutes"
            respond(response)
            time.sleep(1)
            sys.exit()
        elif check_membership(user_msg, HOWRU_RESP_HAPPY):
            response = "That's cool.I am happy for that bro!"
            respond(response)
        else:
            while True:
                response = random.choice(MISUND_RESPONSES)
                if response not in prev_reply:
                    break
            prev_reply[0], prev_reply[1], prev_reply[2] = prev_reply[1],\
                                                    prev_reply[2], response
            respond(response)
