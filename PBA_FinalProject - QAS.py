import re
import nlp

def remove_stopwords(text, stopwords) :
    words = []
    for s in text :
        for w in nlp(s) :
            if w.text.lower() not in words and w.text.lower() not in stopwords :
                words.append(w.text)
    return words



def clean_news(news) :
    news = re.sub('\n','',news)
    news = re.sub('\'','',news)
    news = re.sub(',',' ',news)
    news = news.split('.')
    return news


with open("news.txt","r") as file :
    news = file.read()
with open("questions.txt","r") as file :
    questions = file.read()

questions = questions.split('\n')


news = clean_news(news)

words = []
stopwords = nlp.Defaults.stop_words
words = remove_stopwords(news,stopwords)

