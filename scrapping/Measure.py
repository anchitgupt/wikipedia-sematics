import LoadEmbeddings as model
import xml.etree.ElementTree as ET
import DataPreprocessing as p
from scipy import spatial
import enum

class Convert2Vec:
    '''
    Class takes care of converting the sentences to the vector
    '''
    def __init__(self,model):
        self.model = model

    def convertSen2Vec(self,senlist,isquery):
        
        if isquery:
            return self.makeSentenceVector(model,senlist) 
        else:
            return self.sentenceList2Vector(model,senlist) 


    def makeSentenceVector(self,model,sentence):
        '''
        Convert a single sentence to vector
        '''
        sentence = sentence.replace('.','')
        senWords = sentence.split(' ')
        if model.currentModel = ModelType.Word2Vec:
            wordEmbedding = model.embedding
            ps=p.Preprocessing()
            senWords = ps.removeStopword(senWords)
            mat = []
            for i in senWords:
                if i in wordEmbedding:
                    mat.append(wordEmbedding[i])
            mat = np.array(mat)
            return np.mean(mat,axis = 0)
        esif model.currentModel  = ModelType.SelfTrainedDoc2Vec:
            embedding = model.embedding
            mat = np.array(embedding.infer_vector(senWords))
        return mat 

        
    def sentenceList2Vector(self,model,listSen):
        '''
        make a 2D matrix of vector
        '''
        senVecDict= {sen : self.makeSenVecWord2Vec(model,sen) for sen in sentences}
        return senVecDict    


class MeasureType(enum.Enum):
    CosineSimilarity = 1
    SmoothFreqInverse = 2
    WordMoverDist = 3


class Measure:
    def __init__(self,xmlPath,model):
        '''
        Read All the configuration of the Measure of the model
        '''
        self.currentMeasure = self.loadMeasureConfiguration(xmlPath)
        self.model = model


    def loadConfiguration(self,path):
        root = ET.parse(path).getroot()
        # loadng all the available model into the dict
        # mesures = dict()
        # for typeTag in root.findall('mesures/mesure'):
        #     mesures[MeasureType[typeTag.get('name')]]  = bool(typeTag.get('requireVec')))
        
        #finding the current model to read         
        currentMeasure = MeasureType[root.find('CurrentMesures').text]
        
        return currentMeasure

    def computeMeasure(self,query,sentencesList):
        if self.currentMeasure == MeasureType.CosineSimilarity:
            #get the vectors form the sentences
            obConvert2Vec = Convert2Vec(self.model) 
            qryVector = obConvert2Vec.convertSen2Vec(query,True)
            sentenceVectorDict = obConvert2Vec.convertSen2Vec(query,False)
            # get scores
            scores, sentence = self.cosineSimilarity(qryVector,sentence)
        elif self.currentMeasure == MeasureType.SmoothFreqInverse:
            # TODO Later
        elif self.currentMeasure == MeasureType.WordMoverDist:
            scores, sentence = self.wordMoverDist(query,sentencesList,model)


    def cosineSimilarity(self,queryVector,sentenceVector):
        '''
        calcualtes the cosine similarity between query and sentences
        '''
        scores = []
        for key in sentenceVector:
            #print(sentenceVector[key])
            scores.append(spatial.distance.cosine(sentenceVector[key], queryVector))
        scores, sentence = zip(*sorted(zip(scores, sentenceVector.keys())))
        return scores, sentence

    def wordMoverDist(self,query,sentence,model):
    '''
    calculates the word Mover Distance between query and sentences
    '''
    scores = []
    for sen in sentence:
        scores.append(model.embedding.wmdistance(sen, query))
    scores, sentence = zip(*sorted(zip(scores, sentence)))
    return scores, sentence
    