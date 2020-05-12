#library for Word2Vec
from wikipedia2vec import Wikipedia2Vec
from gensim.models import KeyedVectors
from gensim.test.utils import datapath
# library for Doc2Vec
from gensim.models.doc2vec import Doc2Vec
import multiprocessing
#general library
import xml.etree.ElementTree as ET
import time

class LoadEmbeddings:
    def __init__(self,xmlPath):
        self.currentModel,self.path = self.loadConfiguration(xmlPath);

    def loadConfiguration(self,path):
        root = ET.parse(path).getroot()
        # loadng all the available model into the dict
        modelInfoDict = dict()
        for typeTag in root.findall('models/model'):
            modelInfoDict[typeTag.get('name')] = typeTag.get('path')

        #finding the current model to read         
        currentModel = root.find('CurrentModel').text
        currentSimilarity = root.find('CurrentSimilarity')

        return currentModel , modelInfoDict[currentModel] 

    def loadWord2VecSelf(self, path):
        wordEmbedding= {}
        with open(modelPath, 'r', encoding="utf-8") as f:
            for line in tqdm(f):
                values = line.split()
                word = values[0]
                vector = np.asarray(values[1:], "float32")
                wordEmbedding[word] = vector
        return wordEmbedding

     
    def loadWord2Vec(self,modelPath):
        t1 = time.time()
        print ( "Loading Pretrained Word2Vec Model...... ")
        wordEmbedding = KeyedVectors.load_word2vec_format(datapath(modelPath), binary=False)
        print(time.time()-t1)
        return wordEmbedding 

    def loadDoc2Vec(self,modelPath):
        t1 = time.time()
        print ( "Loading SelfTrained Doc2Vec Model...... ")
        docEmbedding= Doc2Vec.load(modelPath)
        print(time.time()-t1)
        return docEmbedding

    def loadModel(self):
        if self.currentModel == 'Word2Vec':
            wordEmbedding = self.loadWord2Vec(self.path)
            return wordEmbedding
        elif self.currentModel == 'SelfTrainedDoc2Vec':
            docEmbedding = self.loadDoc2Vec(self.path)
            return docEmbedding 
                

lb = LoadEmbeddings("configuration.xml")
lb.loadModel()

