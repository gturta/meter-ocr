import cv2
import numpy as np
import sys
from os import path
from . import Config as CFG
from .ImageProcess import ImagePreprocessor
from .Extractor import Extractor
from .OCR import DigitOCR


class MeterOCR:
    def __init__(self, image, folder='.', debug=False):
        self.folder=folder
        self.imgName=image
        self.filename=path.join(self.folder, self.imgName)
        self.debug=debug

    def loadImage(self, fileName):
        img=cv2.imread(fileName)
        if img is None:
            exit("Invalid image")
        if self.debug:
            print("Image shape: {}".format(img.shape))
        return img

    def process(self):
        self.image = self.loadImage(self.filename)
        preprocess = ImagePreprocessor(self.image, self.folder, debug=True)
        extractor = Extractor(preprocess.image, self.folder, debug=True)
        extractor.process()
        ocr = DigitOCR()
        ocr.train()
        res = ocr.identify(extractor.digits)
        return res

if __name__=="__main__":
    mocr = MeterOCR(sys.argv[1])
    res = mocr.process()
    print(res)
