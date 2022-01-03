# -*- coding: utf-8 -*-
"""Black_coffer_article_analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ye0hlo0CdfvBh80WdUELZ69S8jGqDIZY
"""

import pandas as pd
import requests
import bs4 as bfs
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import string
from textblob import TextBlob
import csv
import numpy as np

nltk.download('stopwords')
nltk.download('punkt')

df = pd.read_csv('/content/Input.xlsx - Sheet1.csv',index_col=0)

li = [url for url in df['URL']]

text = []
for url in li:
  text.append(requests.get(url,headers={"User-Agent": "XY"}))

for i in range(len(text)):
  text[i] = bfs.BeautifulSoup(text[i].content,'html.parser')

articles = []
for text in text:
  articles.append(text.find(attrs= {"class":"td-post-content"}).text)

for i in range(len(articles)):
  articles[i]= articles[i].replace('\n','')

stop_words = list(set(stopwords.words('english')))

sentences = []
for article in articles:
  sentences.append(len(sent_tokenize(article)))

cleaned_articles = [' ']*len(articles)

for i in range(len(articles)):
  for w in stop_words:
    cleaned_articles[i]= articles[i].replace(' '+w+' ',' ').replace('?','').replace('.','').replace(',','').replace('!','')
    #? ! , .

words = []
for article in articles:
  words.append(len(word_tokenize(article)))

words_cleaned = []
for article in cleaned_articles:
  words_cleaned.append(len(word_tokenize(article)))

dictionary = pd.read_excel('/content/LoughranMcDonald_MasterDictionary_2020.xlsx')

positive_words = list(dictionary[dictionary['Positive']==2009]['Word'])
positive_words = [word.lower() for word in positive_words]

negative_words = list(dictionary[dictionary['Negative']==2009]['Word'])

positive_score = [0]*len(articles)
for i in range(len(articles)):
  for word in positive_words:
    for letter in cleaned_articles[i].lower().split(' '):
      if letter==word:
        positive_score[i]+=1

negative_score = [0]*len(articles)
for i in range(len(articles)):
  for word in negative_words:
    for letter in cleaned_articles[i].upper().split(' '):
      if letter==word:
        negative_score[i]+=1

words_cleaned = np.array(words_cleaned)
sentences = np.array(sentences)

df['POSITIVE SCORE'] = positive_score
df['NEGATIVE SCORE'] = negative_score

df['POLARITY SCORE'] = (df['POSITIVE SCORE']-df['NEGATIVE SCORE'])/ ((df['POSITIVE SCORE'] +df['NEGATIVE SCORE']) + 0.000001)

df['SUBJECTIVITY SCORE'] = (df['POSITIVE SCORE'] + df['NEGATIVE SCORE'])/( (words_cleaned) + 0.000001)

df['AVG SENTENCE LENGTH'] = np.array(words)/np.array(sentences)

complex_words = []
sylabble_counts = []

for article in articles:
  sylabble_count=0
  d=article.split()
  ans=0
  for word in d:
    count=0
    for i in range(len(word)):
      if(word[i]=='a' or word[i]=='e' or word[i] =='i' or word[i] == 'o' or word[i] == 'u'):
           count+=1
#            print(words[i])
      if(i==len(word)-2 and (word[i]=='e' and word[i+1]=='d')):
        count-=1;
      if(i==len(word)-2 and (word[i]=='e' and word[i]=='s')):
        count-=1;
    sylabble_count+=count    
    if(count>2):
        ans+=1
  sylabble_counts.append(sylabble_count)
  complex_words.append(ans)

df['PERCENTAGE OF COMPLEX WORDS'] = np.array(complex_words)/np.array(words)

df['FOG INDEX'] = 0.4 * (df['AVG SENTENCE LENGTH'] + df['PERCENTAGE OF COMPLEX WORDS'])

df['AVG NUMBER OF WORDS PER SENTENCES'] = df['AVG SENTENCE LENGTH']

df['COMPLEX WORD COUNT'] = complex_words

df['WORD COUNT'] = words

df['SYLLABLE PER WORD'] = np.array(sylabble_counts)/np.array(words)

total_characters = []
for article in articles:
  characters = 0
  for word in article.split():
    characters+=len(word)
  total_characters.append(characters)

personal_nouns = []
personal_noun =['I', 'we','my', 'ours','and' 'us','My','We','Ours','Us','And'] 
for article in articles:
  ans=0
  for word in article:
    if word in personal_noun:
      ans+=1
  personal_nouns.append(ans)

df['PERSONAL PRONOUN'] = personal_nouns
#as the all pronouns were cleared when clearing the stop words.

df['AVG WORD LENGTH'] = np.array(total_characters)/np.array(words)

from google.colab import drive
drive.mount('drive')

df.to_csv('Prateek_Pal.csv',index=False)
!cp Prateek_Pal.csv "drive/My Drive/"



