import time
t1 = time.time()
import re
import requests
import bs4
import DataPreprocessing as p
import nltk
from nltk.tokenize import sent_tokenize


############################################################################################################
############################################################################################################
# basic url segmentation
wiki_bPath   = 'https://en.wikipedia.org'
qtitle       = 'Car'  # str(input("Enter the Title name: "))
fileName     = "/wiki/" + qtitle
url          = wiki_bPath + fileName
cite_num     = sorted([4, 5])


# read the URL data
res     = requests.get(url)
wiki    = bs4.BeautifulSoup(res.text, "lxml")



# checking if somedata is available or not
if wiki == None:
    print('Document reference Can\'t be reached')
    exit(1)



# read each cite note
citations = wiki.find_all("li", {'id': re.compile(r'^cite_note')})



# citations = [wiki.find_all("li", {'id': re.compile(r'^cite_note\-'+str(i)+'|cite_note\-[a-zA-Z0-9]*\-'+str(i)+'')}) for i in cite_num]


# ### https://regex101.com/r/b1ZjYR/4


# create a dictionary of citations

## Stop the loop as all the elements from the cite_num are not extracted
cite_no = 1
i = 0
lines = {}
for cite in citations:
    url = []
    for a in cite.find_all('a', href=True):
        if a['href'].startswith('/wiki'):
            links = wiki_bPath + a['href']
            if len(links.split('/')[0]) < 3:
                links = 'http:' + links
            url.append(links)
        elif not a['href'].startswith('#'):
            url.append(a['href'])
    lines[cite_no] = url
    cite_no += 1



## here all citations have been gathered.

##############################################################################################################################
##############################################################################################################################


# check url's which are working fine:
flines = {}
for citen in cite_num:
    urls = []
    if len(lines[citen]) != 0:
        # iterating over url's
        for url in lines[citen]:
            res = requests.get(url)
            # print(citen, res, url)
            # TODO: response is in 404 then do not add the url in the urls list
            if res == False:
                # TODO: handle exception
                print('Exception')
            wiki = bs4.BeautifulSoup(res.text, "lxml")
            urls.append(wiki)
        flines[citen] = urls


dlines = {}
# cite number
for j in cite_num:
    data = []
    for k in flines[j]:
        data.extend(['\n'.join([i.getText() for i in k.select('p')])])
    dlines[j] = data


print('Time : ' , time.time() - t1)
# TODO: make sentence vector


