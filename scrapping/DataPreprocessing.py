import re,string,math
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize,word_tokenize
import codecs
from nltk.stem import WordNetLemmatizer
from num2words import num2words
# import contractions


class Preprocessing:
    
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
    
    def TexttoLower(self,text):
        text=text.lower()
        return text
    
    def removeMetaData(self,text):
        text=re.sub(r'\n\n','',text)
        #text=re.sub(r'.*[lL]ines: \d+','',text)
        return text
    
    def expandContractions(self,text):
        text=contractions.fix(text)
        return text
    
    #Updated by Prashant
    def removeSpecialCharacter(self,regList,replaceChar,data):
        # reger for handle, for RT and for URls
        for regex in regList:
            data = re.sub(pattern = regex, repl = replaceChar ,string = data)
        return data
        
    def removeEmailId(self,text):
        text=re.sub(r'\b[A-Za-z0-9=.-]+@[A-Za-z0-9]+\.*[.\w+]+\b',' ',text)
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
                    
    def removePunctuations(self,word_list):
        table = str.maketrans(' ', ' ', string.punctuation)
        word_list = [w.translate(table) for w in word_list]
        return word_list
    
    def spaces(self,word_list):
        word=[s for s in word_list if s]
        return word
        
    def lemmatization(self,word_list):
        word=[]
        for w in word_list:
            word.append(self.lemmatizer.lemmatize(w))
        return word
        
    def num2wordExpansion(self,word_list):
        final_word=[]
        for w in word_list:
            if w.isdigit():
                final_word.append(num2words(w))
            else:
                final_word.append(w)
        return final_word

    def removeDigits(self,text):
        text=re.sub(r'\b\d+\b',' ',text)
        return text



#ps=Preprocessing()
#text="4253 derd"
#text=ps.removeDigits(text)
#print(text)
# word_list=ps.wordTokenization(text)
# word_list=ps.removeStopword(word_list)
# print(ps.lemmatization(word_list))
    
    