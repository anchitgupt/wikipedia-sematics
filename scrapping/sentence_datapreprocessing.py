import re,string,math
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize,word_tokenize
import codecs
from nltk.stem import WordNetLemmatizer
from num2words import num2words
import contractions


class Preprocessing:
    
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
    
    def TexttoLower(self,text):
        text=text.lower()
        return text

    def sentence_tokenize(self,text):
        sentences=sent_tokenize(text)
        return sentences


    def expandContractions(self,sentences):
        for i in range(len(sentences)):
            sentences[i]=contractions.fix(sentences[i])
        return sentences
   
    def removeSpecialCharacter(self,sentences):
        # regex for handle, for RT and for URls
        regList = ['https?://[A-Za-z0-9./]+','[-)(:;/]+','(\\[\\d+\\]|\\[\\w+\\])']
        replaceChar=' '
        for i in range(len(sentences)):
            for regex in regList:
                sentences[i]= re.sub(pattern = regex, repl = replaceChar ,string = sentences[i])
        return sentences
        
    def removePunctaution_except(self,sentences):
        for i in range(len(sentences)):
            sentences[i]=re.sub(r'[~`!@#$%^&*(){[}|_<,>?/:;"-]',' ',sentences[i])
        return sentences
                           
    def wordTokenization(self,sentences):
        for i in range(len(sentences)):
            sentences[i]=word_tokenize(sentences[i])
        return sentences
    
    def removeStopword(self,sentences):
        stopword=set(stopwords.words('english'))
        word=[ [] for i in range(len(sentences)) ]
        for i in range(len(sentences)):
            for w in sentences[i]:
                if w not in stopword:
                    word[i].append(w)
        return word
                
    def spaces(self,sentences):
        word=[ [] for i in range(len(sentences)) ]
        for i in range(len(sentences)):
            word[i]=[s for s in sentences[i] if s]
        return word
        
    def lemmatization(self,word_list):
        word=[ [] for i in range(len(sentences)) ]
        for i in range(len(sentences)):
            for w in sentences[i]:
                word[i].append(self.lemmatizer.lemmatize(w))
        return word
        
    def makeSentence(self,sentences):
        word=[ [] for i in range(len(sentences)) ]
        s=' '
        for i in range(len(sentences)):
            word[i]=s.join(sentences[i])
        return word

