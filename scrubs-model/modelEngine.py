# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 18:51:54 2020

@author: Jose
"""

import numpy as np
import pandas as pd
import re
import pickle
import nltk
from nltk.corpus import stopwords
from sklearn.datasets import load_files
nltk.download('stopwords')
import json

# create corpus
scripts = load_files('S02',encoding = 'utf-8',decode_error='ignore', shuffle=False)
X = scripts.data

with open('model.pickle', 'rb') as f:
    classifier = pickle.load(f)
    
with open('vectorizer.pickle', 'rb') as f:
    tfidf = pickle.load(f)    

sample = []
for script in X:    
    text = re.sub(r'<.*?>','',script.lower())
    text = re.sub(r'\[(.*?)\]',' ',text)
    text = re.sub(r'.*:',' ',text)
    text = re.sub(r'\W','  ',text)
    text = re.sub(r'\s[a-z]\s',' ',text)
    text = re.sub(r'\s+', ' ', text)
    sample.append(text)

sample = tfidf.transform(sample).toarray()
sentiments = classifier.predict(sample)
sentiments_string = ['positive' if x==1 else 'negative' for x in sentiments ]

with open('episodes_2.json', 'r') as f:
    episodes = json.load(f)

episode_names = []
for x in episodes['names']:
    name = re.sub(r'_',' ', x)
    episode_names.append(name)

results = pd.DataFrame(episode_names)
results['sentiment'] = sentiments_string


# Script Dialog Character Extraction
characterList = ["jd", "elliot", "turk", "carla", "drcox", "drkelso", "janitor", "keith", "jordan", "doug", "laverne", "ted", "todd"]
Characters = pd.DataFrame()
for script in X:    
    #text = re.sub(r'<.*?>','',script.lower())
    text = script.lower().splitlines()
    ep_chars = []
    characterVector = pd.DataFrame(columns = characterList)
    
    for line in text:
        #tag_content = re.findall(r'(<b>.*<\/b>)\s',line)
        #for content in tag_content:
        #    if content !=[]:
        #        content = re.sub(r'<.*?>','',content)
        #        content = re.sub(':','',content)
        #        ep_chars.append(content)        
        
        #if tag_content != []:
        #    print(tag_content)
        tag_content = re.sub(r'<.*?>','',line)
        #ep_chars.append(tag_content)
        ep_chars.append(re.findall(r'^([^:]+):\s',tag_content))
    
            # ep_chars.append(re.findall(r'.*:\s',line))

    only_chars = [character for character in ep_chars if character !=[] ]
    only_chars_df = pd.DataFrame(only_chars)
    only_chars_df = only_chars_df[0].drop_duplicates()
    for row in only_chars_df.iteritems():
        # print(row[1], type(row[1]))
        currentChar = re.sub('\W','',row[1])
        for character in characterList:
            if character in currentChar.lower():
                characterVector[character] = True
                print(character + ' is in this episode********************')
            else:
                print(character + ' is NOT in this episode')
    
    
    #print(type(only_chars_df), type(Characters))
    Characters = pd.concat([Characters, characterVector], ignore_index= True)
    #Characters.append(only_chars_df.tolist())