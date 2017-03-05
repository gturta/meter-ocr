import cv2
import numpy as np
from os import path
import csv
import uuid

class DigitOCR:
    def __init__(self,trainLibrary='train',trainStage0='train0'):
        self.knn = cv2.ml.KNearest_create()
        self.trainLibrary=trainLibrary
        self.trainStage0=trainStage0
        self.trainIndex='index.txt'
        self.trainData='train-data.npz'

    def train(self):
        with np.load(self.trainData) as data:
            train = data['train'].astype(np.float32)
            train_labels = data['train_labels']
            self.knn.train(train, cv2.ml.ROW_SAMPLE, train_labels)

    def identify(self,images):
        results=[]
        for img in images:
            if img is not None:
                img=img.reshape(-1,450).astype(np.float32)
                ret,result,neighbours,dist = self.knn.findNearest(img,k=5)
                results.append([ret,result,neighbours,dist])
            else:
                results.append([None,None,None,None])
        return results

    def generateTrainFile(self):
        libIndex=path.join(self.trainLibrary,self.trainIndex)
        with open(libIndex,'r') as index:
            reader=csv.reader(index)
            data=np.array([row for row in reader])
            files=data[:,0]
            digits=data[:,1]
            load=np.zeros((len(files),450))#assuming a 15x30px image
            for i in range(len(files)):
                filename=path.join(self.trainLibrary,files[i])
                img=cv2.imread(filename,0)
                if img is not None:
                    load[i]=img.reshape(1,-1).astype(np.float32)
            digits=digits[:,np.newaxis].astype(np.float32)
            np.savez(self.trainData, train=load, train_labels=digits)

    def generateTrainingDigits(self):
        #read digit images from stage0
        #generate training images from them
        #by shifting them with 2px up,down,left&right
        generated=[]
        s0index = path.join(self.trainStage0,self.trainIndex)
        with open(s0index,'r') as s0file:
            s0reader = csv.reader(s0file)
            for row in s0reader:
                #read s0 image
                s0name,s0digit=row[0],row[1]
                s0File=path.join(self.trainStage0,s0name)
                img = cv2.imread(s0File,0)
                rows,cols=img.shape
                #write original image
                libFile=str(uuid.uuid4())+'.jpg'
                filename=path.join(self.trainLibrary,libFile)
                cv2.imwrite(filename,img)
                generated.append([libFile,s0digit])
                #x,y for shifting
                offsets=[(0,-2),(0,2),(-2,0),(2,0)]
                for x,y in offsets:
                    #shift
                    m=np.float32([[1,0,x],[0,1,y]])
                    shift=cv2.warpAffine(img,m,(cols,rows))
                    libFile=str(uuid.uuid4())+'.jpg'
                    filename=path.join(self.trainLibrary,libFile)
                    cv2.imwrite(filename,shift)
                    generated.append([libFile,s0digit])
        #write generated images
        self.addToTrainingIndex(generated)

    def addToTrainingIndex(self, data):
        #data should be a list of [img,digit]
        indexFile = path.join(self.trainLibrary,self.trainIndex)
        with open(indexFile,'w') as index:
            writer=csv.writer(index)
            for row in data:
                writer.writerow(row)

if __name__=="__main__":
    ocr = DigitOCR(trainLibrary='train',trainStage0='train0')
    ocr.generateTrainingDigits()
    ocr.generateTrainFile()

