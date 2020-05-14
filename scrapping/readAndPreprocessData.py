import re
import requests
import bs4
import sentence_datapreprocessing as p

def readUrlContent(url):
    '''
    read pages form given URL
    '''
    if url[:2] == "//":
        url = 'http:'+ url
    res = requests.get(url)
    if res == False:
        print('404 Page Not Found')
        exit(1)
    #res.raise_for_status()
    #Just to raise the status code
    wiki = bs4.BeautifulSoup(res.text,"lxml")
    return wiki


def getParas(wiki):
    '''
    read files that are in the cited link and fetch its text
    '''
    elems = wiki.select('p')
    data = []
    for i in range(len(elems)):
        data.append(elems[i].getText())
    dataString = "\n".join(data)
    return dataString


def getAllCiteLink(wiki_bPath,wiki):
    '''
    get citation link from the wikipedia page
    retunns a dictionary the sore key as citation number and value as a list of url in that citations
    '''
    cite_no = 1
    lines = dict()
    citations = wiki.find_all("li", {'id': re.compile(r'^cite_note')})
    for cite in citations: 
        url = []
        for a in cite.find_all('a', href=True):
            if a['href'].startswith('/wiki'):
                url.append(wiki_bPath+a['href'])
            elif not a['href'].startswith('#'):
                url.append(a['href'])
        lines[cite_no] = url
        cite_no += 1
    return lines 

def getCiteLink(wiki_bPath,wiki,citeNub):
    '''
    get citation url link of a partivular citation number
    returns a list of citation
    '''
    urlList = []
    citations = wiki.find_all("li", {'id': re.compile(r'^cite_note')})
    for cite in citations:
        for a in cite.find_all('a', href=True):
            if a['href'].startswith('/wiki'):
                urlList.append(wiki_bPath+a['href'])
            elif not a['href'].startswith('#'):
                urlList.append(a['href'])
    return urlList

def fetchCitedUrlData(citeList):
    '''
    Read each url in the document(citeList) and scrap those url content and return a preprocess sentence list
    '''
    docSentences = []
    for cite in citeList:
        data = getParas(readUrlContent(cite))
        #print (preprocessData(data))
        docSentences += preprocessData(data)
    return docSentences


def seperateQueryAndCitation(queryText):
    '''
    Query String receives the query text from the front and returns the data back
    ''' 
    qrySplit = re.split(r']|\[',queryText)
    citationList = []
    qryList = []
    for qryTrm in qrySplit:
        if qryTrm.isdigit():
            citationList.append(int(qryTrm))
        else:
            qryList.append(qryTrm.strip())
    return ' '.join(qryList),citationList 


'''
Preprocessing utility methods
'''
def preprocessData(data):
    ps=p.Preprocessing()
    #Making the text to lower case 
    data = ps.TexttoLower(data)
    #Expanding the contraction
    data=ps.sentence_tokenize(data)
    data = ps.expandContractions(data)
    data=ps.removeSpecialCharacter(data)
    data=ps.removePunctaution_except(data)
    data=ps.wordTokenization(data)
    data=ps.spaces(data)
    dataList=ps.lemmatization(data)
    dataList=ps.makeSentence(dataList)
    return dataList

def ConvertSenToTokenizeForm(sentence):
    '''
    preprocess the sentence so that they can be found in embeddings
    '''
    for i in range(len(sentence)):
        sentence[i] = sentence[i].replace('.',' ')
        sentence[i]=preprocessData(sentence[i])
    
    return sentence

def queryPreprocess(query):
    '''
    code to preprocess the qry
    '''
    query = preprocessData(query)
    queryList=query[0].replace('.','')
    return queryList