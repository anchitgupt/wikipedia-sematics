import flask
from flask import Flask, abort
from flask import request, jsonify
import readAndPreprocessData as rp
from flask_cors import CORS
from model import LoadEmbeddings
import model
import Measure as m


app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

xmlPath = "configuration.xml"
#defining the model for generating the embedings
model = LoadEmbeddings(xmlPath)
#loading the embeddings
model.loadModel()


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
    # preprocess the query and tokenizing it for further use
    preprocessedQry = rp.queryPreprocess(queryString)
    #print("preprocessedQry" , preprocessedQry)
    # read the wikipedia path
    wiki = rp.readUrlContent(completeUrl)
    # get the url at the citation
    urlDict = rp.getAllCiteLink(wikiBasePath, wiki)
    
    #variable to store result
    result = dict()
    # loop for evry citation in the query
    for i in citationList:
        urlList = urlDict[i]
        if (len(urlList) == 0):
            errorText = "No data To handle"
            result[i] = (errorText,"")
            print(errorText)
            # break
        elif urlList[0].split('/')[-1].split('.')[-1] == 'pdf':
            errorText = 'PDF not supported'
            result[i] = (errorText,"")
            print(errorText)
            # break
        else:
            # read the data of the cited document and return proper sentences
            sentences = rp.fetchCitedUrlData(urlList)
            # pass list of sentence and convert it into token form so that it can be give and converted into vector
            sentenceWordTokenize = rp.ConvertSenToTokenizeForm(sentences)
            #print('Sentences: ', ' '.join(sentenceWordTokenize[0]))
            #print("Sentences",sentenceWordTokenize)
            if(len(sentenceWordTokenize) == 0):
                errorText = 'No sentences found in the cited document'
                result[i] = (errorText,"")
                print(errorText)
            else:
                '''
                Now we have to convert the list of words for sentences and query to vector according
                to model and perform of simialrity task
                '''
                measure = m.Measure(xmlPath,model)
                scores ,sentences = measure.computeMeasure(preprocessedQry,sentenceWordTokenize)
                print(scores[:5],sentences[:5])
                result[i] = ("",sentences[0])
            

    op = {
        'status': "OK",
        'result' : result
        }

    return jsonify(op), 201


app.run()