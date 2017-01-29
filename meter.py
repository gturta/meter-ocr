import cv2
import numpy as np
import sys
from Config import Config as CFG
from ImageProcess import ImagePreprocessor
from Extractor import Extractor
from OCR import DigitOCR

def loadImage(fileName):
    img=cv2.imread(fileName)
    if img is None:
        exit("Invalid image")
    if CFG.DEBUG:
        print("Image shape: {}".format(img.shape))
    return img

if __name__=="__main__":
    img=loadImage(sys.argv[1])
    proc = ImagePreprocessor(img,CFG.DEBUG)
    ex=Extractor(proc.image,CFG.DEBUG)
    ex.process()
    ocr = DigitOCR()
    ocr.train()
    res = ocr.identify(ex.digits)
    print(res)
