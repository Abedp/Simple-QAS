import re
import en_core_web_sm

def remove_stopwords(text, stopwords) :
    words = []
    for s in text :
        for w in nlp(s) :
            if w.text.lower() not in words and w.text.lower() not in stopwords :
                words.append(w.text)
    return words

def find_index(news, question) :
    match = 0
    value = 0
    question = question.split(' ')
    for i in range(len(news)):
        val = 0
        for j in range(len(question)):
            if question[j].lower() in news[i].lower():
                val += 1
        if val > value:
            value = val
            match = i
    return match

def clean_news(news) :
    news = re.sub('\n','',news)
    news = re.sub('\'','',news)
    news = re.sub(',',' ',news)
    news = news.split('.')
    return news

def clean_question(question) :
    question = question.replace('?','')
    q_word = re.findall('(^\w+)\s+',question)[0]
    q_word = q_word.lower()
    question = re.sub('^(\w+)\s+','',question)
    ner = []
    if q_word == 'who' :
        ner.append(['person'])
    elif q_word == 'where' :
        ner.append(['gpe'])
    elif q_word == 'when' :
        ner.append(['date'])
    elif q_word == 'how' :
        ner.append(['money'])

    return question, ner

def find_answer(sentence, question, q_word):
    ner = find_ner(sentence)
#    print(ner)
    answer = ''
    count = 0
    found = False
    index = 0
    for i in range(len(question)) :
        for j in range(len(ner)) :
            if question[i].lower() in ner[j][0].lower() :
#                print(question[i], ner[j][0])
                for l in range(j, len(ner)) :
                    if found == False :
                        if q_word[0].lower() in ner[l][1].lower():
                            answer = ner[l][0]
                            count = abs(j-l)
                            index = l
                            found = True
#                            print('0 q=', question[i],' a=', answer, ' count=',count)
                                           
                    elif found == True :
                        if q_word[0].lower() in ner[l][1].lower():
                            if ner[index][0].lower() == ner[l-1][0].lower() and ner[l][0] not in answer:
                                answer = " ".join((answer, ner[l][0]))
                                index = l
#                                print('1 q=', question[i],' a=',answer, ' count=',count)
                        
                            elif abs(j-l) < count :
                                answer = ner[l][0]
                                count = abs(j-l)
                                index = l
                                found = True
                        
#                                print('2 q=', question[i],' a=',answer, ' count=',count)
                        
                        
                for l in range(j, -1, -1):
                    if found == False :
                        if q_word[0].lower() in ner[l][1].lower():
                            answer = ner[l][0]
                            count = abs(j-l)
                            index = l
                            found = True
#                            print('3 q=', question[i],' a=',answer, ' count=',count)
                            
                    elif found == True :
                        if q_word[0].lower() in ner[l][1].lower():
                            if ner[index][0].lower() == ner[l+1][0].lower() and ner[l][0] not in answer :
                                answer = " ".join((ner[l][0], answer))
                                index = l
#                                print('4 q=', question[i],' a=',answer, ' count=',count)
                        
                            elif abs(j-l) < count :
                                answer = ner[l][0]
                                count = abs(j-l)
                                index = l
                                found = True
                        
#                                print('5 q=', question[i],' a=',answer, ' count=',count)
                                                    
    return answer
                
    
def find_ner(sentence):
    nlp = en_core_web_sm.load()
    ner = []
    for t in nlp(sentence) :
        ner.append([t.text, t.ent_type_])
    return ner


with open("news.txt","r") as file :
    news = file.read()
with open("questions.txt","r") as file :
    questions = file.read()

questions = questions.split('\n')
nlp = en_core_web_sm.load()

news = clean_news(news)

words = []
stopwords = nlp.Defaults.stop_words
words = remove_stopwords(news,stopwords)

for i, b in enumerate(questions) :
    q = []
    question, q_word = clean_question(b)
    q = question.split(' ')
    print(i+1, b)
    found_index = find_index(news, question)
    answer = find_answer(news[found_index], q, q_word[0])
    print(answer, '\n')
