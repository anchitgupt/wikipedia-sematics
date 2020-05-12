import flask
from flask import Flask, abort
from flask import request, jsonify
import readAndPreprocessData as rp
from flask_cors import CORS


app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)


@app.route('/', methods=['POST'])
def home():
    if not request.json:  # on or not 'pageName' in request.json:
        print('Request Aborted')
        abort(400)

    # Read data from the POST method
    pageName = request.json['pageName']
    queryText = request.json['queryText']

    # Read the wikipedia path
    wikiBasePath = 'https://en.wikipedia.org'
    completeUrl = wikiBasePath + "/wiki/" + pageName

    # variable to store error message
    errorText = ''
    # seperate the query and citation part
    queryString, citationList = rp.seperateQueryAndCitation(queryText)
    # read the wikipedia path
    wiki = rp.readUrlContent(completeUrl)
    # get the url at the citation
    urlDict = rp.getAllCiteLink(wikiBasePath, wiki)
    # loop for evry citation in the query
    for i in citationList:
        urlList = urlDict[i]
        if (len(urlList) == 0):
            errorText = "No data To handle"
            print("No data To handle")
            break
        elif urlList[0].split('/')[-1].split('.')[-1] == 'pdf':
            errorText = 'PDF not supported'
            print('PDF not supported')
            break
        else:
            # read the data of the cited document and return proper sentences
            sentences = rp.fetchCitedUrlData(urlList)
            # pass list of sentence and convert it into token form so that it can be give and converted into vector
            sentenceWordTokenize = rp.convertListSenToToken(sentences)
            #print('Sentences: ', ' '.join(sentenceWordTokenize[0]))
            #print("Sentences",sentenceWordTokenize)
            
            # preprocess the query
            preprocessedQry = rp.queryPreprocess(queryString)
            #print("preprocessedQry" , preprocessedQry)
            
            '''
            Now we have to convert the list of words for sentences and query to vector according to model 
            and perform of simialrity task
            '''

    op = {
        'status': "OK",
        'citationList': citationList,
        'error': errorText,
        'data': ' '.join(sentenceWordTokenize[0])
    }

    return jsonify(op), 201


app.run()