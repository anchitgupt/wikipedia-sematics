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

    def expandContractions(self,text):
        text=contractions.fix(text)
        return text
   
    def removeSpecialCharacter(self,text):
        # regex for handle, for RT and for URls
        regList = ['https?://[A-Za-z0-9./]+','[-)(:;/]+','(\\[\\d+\\]|\\[\\w+\\])']
        replaceChar=' '
        for regex in regList:
            text = re.sub(pattern = regex, repl = replaceChar ,string = text)
        return text
        
    def removePunctaution_except(self,text):
        text=re.sub(r'[~`!@#$%^&*(){[}|_<,>?/:;"-]',' ',text)
        return text
                           
    def wordTokenization(self,text):
        text=word_tokenize(text)
        return text
    
    def removeStopword(self,word_list):
        stopword=set(stopwords.words('english'))
        word=[]
        for w in word_list:
            if w not in stopword:
                word.append(w)
        return word
                
    def spaces(self,word_list):
        word=[s for s in word_list if s]
        return word
        
    def lemmatization(self,word_list):
        word=[]
        for w in word_list:
            word.append(self.lemmatizer.lemmatize(w))
        return word
        
    


ps=Preprocessing()
text="" 
text=ps.expandContractions(text)
print(text)
text=ps.TexttoLower(text)
print(text)
text=ps.removeSpecialCharacter(text)
print(text)
text=ps.removePunctaution_except(text)
print(text)
word_list=ps.wordTokenization(text)
word_list=ps.removeStopword(word_list)
word_list=ps.lemmatization(word_list)
    
    