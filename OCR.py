import cv2
import numpy as np
from os import path

class DigitOCR:
    def __init__(self,trainImages='train'):
        self.knn = cv2.ml.KNearest_create()
        self.trainLibrary=trainImages

    def train(self):
        with np.load('train-data.npz') as data:
            train = data['train'].astype(np.float32)
            train_labels = data['train_labels']
            self.knn.train(train, cv2.ml.ROW_SAMPLE, train_labels)

    def identify(self,images):
        data = np.array([img.reshape(-1).astype(np.float32)\
                         for img in images])
        ret,result,neighbours,dist = self.knn.findNearest(data,k=5)
        return result

    def generateTrainFile(self):
        load=np.zeros((10,450))
        for i in range(10):
            filename=path.join(self.trainLibrary,'d{}.jpg'.format(i))
            img=cv2.imread(filename,0)
            if img is not None:
                print("d{}:{}".format(i,img.shape))
                load[i]=img.reshape(1,-1).astype(np.float32)
        train=load.repeat(5,axis=0)
        train_labels=np.arange(10).repeat(5)[:,np.newaxis]
        np.savez('train-data.npz',train=train, train_labels=train_labels)

    def generateTrainDigits(self):
        self.generateTrainFile()

if __name__=="__main__":
    ocr = DigitOCR(trainImages='train')
    ocr.generateTrainDigits()

