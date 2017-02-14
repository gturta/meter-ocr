import sys
import cv2
import numpy as np
from os import path
from Config import Config as CFG
from ImageProcess import ImagePreprocessor

class Extractor:
    def __init__(self,image):
        self.image = image

    def process(self):
        #the decimals are surrounded by a red box, so find it
        self.redBoxes=self.findRedBoxes()
        #expand the red boxes to contain all digits
        self.redBands=self.calculateRedBands()
        #process and extract the (possible) digit boxes
        self.redROIs=self.getRedROIs()
        #get the digits (by contours)
        self.digitSets=self.getDigitBoxes()
        #identify the best candidates
        self.foundIndex,self.foundConfidence = self.filterROIs()
        #try to order the digits from left to right
        self.orderDigitsByX()
        #identify which digits we found and which are not found
        self.foundDigits=self.identifyDigits()
        #normalize digits (same height and width)
        self.normalizeDigits()
        self.debugDump()

    @property
    def digits(self):
        return [self.getDigitROI(i) for i in range(len(self.foundDigits))]

    def getDigitROI(self,index):
        d=self.foundDigits[index]
        if d is None: return None
        bandROI=self.redROIs[self.foundIndex]
        digitROI = bandROI[d[0][1]:d[1][1],d[0][0]:d[1][0]]
        #resize to standard dimensions
        digitROI = cv2.resize(digitROI,\
                   (CFG.DIGIT_RESIZE_WIDTH,\
                    CFG.DIGIT_RESIZE_HEIGHT))
        return digitROI

    def findRedBoxes(self):
        img = self.image
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        #red color in HSV space: 0-10 & 160-179
        redmask1=cv2.inRange(hsv,(0,100,100),(10,255,255))
        redmask2=cv2.inRange(hsv,(160,100,100),(179,255,255))
        mask=cv2.add(redmask1,redmask2)
        _,contours,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,
                                      cv2.CHAIN_APPROX_SIMPLE)
        #filter boxes that don't fit digit sizes
        filtered=[]
        for contour in contours:
            x,y,w,h=cv2.boundingRect(contour)
            if CFG.DIGIT_MIN_HEIGHT<h<CFG.DIGIT_MAX_HEIGHT*3 \
               and 2*h<w<4*h: #should be three times wider than higher
                filtered.append([(x,y),(x+w,y+h)])
        return filtered

    def calculateRedBands(self):
        bands=[]
        for box in self.redBoxes:
            #band = 0.8*height of the box, 2.4*width of box
            boxHeight=box[1][1]-box[0][1]
            boxWidth=box[1][0]-box[0][0]
            x1=box[1][0]-int(2.4*boxWidth)
            y1=int(box[0][1]+int(0.1*boxHeight))
            x2=box[1][0]
            y2=box[1][1]-int(0.1*boxHeight)
            bands.append([(x1,y1),(x2,y2)])
        return bands

    def getRedROIs(self):
        redROIs=[]
        for band in self.redBands:
            roi = self.image[band[0][1]:band[1][1],band[0][0]:band[1][0]]
            #process ROI
            img=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
            height=int(roi.shape[0]/2)*2-1 #needs to be uneven
            img=cv2.adaptiveThreshold(img,255,\
                                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                        cv2.THRESH_BINARY,height,-40)
            #remove noise
            k = int(img.shape[0]*0.05)#one fifth of height
            if k > 1:
                kernel = np.ones((k,k),np.uint8)
                img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
            redROIs.append(img)
        return redROIs

    def rectFitsDigit(self,w,h,boxHeight):
        #a digit should be at least as high as 1/2 of band
        if boxHeight*2/5 < h < boxHeight*2/3\
            and h*CFG.DIGIT_W_H_MIN_RATIO < w < h*CFG.DIGIT_W_H_MAX_RATIO:
            return True
        else:
            return False

    def getDigitBoxes(self):
        digitSets=[]
        for roi in self.redROIs:
            img=roi.copy()
            _,contours,hierarchy=cv2.findContours(img,cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)
            #filter contours outside rules
            filteredRects=[]
            for i in range(0,len(contours)):
                contour=contours[i]
                #reject if not a digit 
                x,y,w,h=cv2.boundingRect(contour)
                if self.rectFitsDigit(w,h,img.shape[0]):
                    #dont add child contours if parent fits
                    parent_id=hierarchy[0][i][3]
                    if parent_id>0:
                        parent = contours[parent_id]
                        px,py,pw,ph=cv2.boundingRect(parent)
                        if self.rectFitsDigit(pw,ph,img.shape[0]):
                            continue
                    #no parent or parent too big
                    filteredRects.append([(x,y),(x+w,y+h)])
            #add to list
            digitSets.append(filteredRects)
        return digitSets

    def filterROIs(self):
        maxDigits,maxIdx=0,0
        for i in range(len(self.redROIs)):
            if len(self.digitSets[i]) > maxDigits:
                maxDigits=len(self.digitSets[i])
                maxIdx=i
        confidence=maxDigits/8 #we should have 8 digits
        return maxIdx,confidence

    def orderDigitsByX(self):
        digits = self.digitSets[self.foundIndex]
        self.digitSets[self.foundIndex] = \
            sorted(digits,key=lambda d: d[0][0])

    def identifyDigits(self):
        #we have 8 digits, let's find them in order
        orderedDigits=[]
        #digit n should have it's center between n*1/8 and (n+1)*1/8
        roi = self.redROIs[self.foundIndex]
        digits = self.digitSets[self.foundIndex]
        xCenters = [int((d[1][0]+d[0][0])/2)/roi.shape[1] for d in digits]
        for i in range(8):
            left,right = i*1/8,(i+1)*1/8
            foundDigit = None
            for d in range(len(digits)):
                if left < xCenters[d] < right:
                    foundDigit = digits[d]
                    break
            #add found digit / or None
            orderedDigits.append(foundDigit)
        return orderedDigits

    def normalizeDigits(self):
        maxHeight,maxWidth = 0,0
        #find max width & height
        for d in self.foundDigits:
            if d is None: continue
            maxHeight = max(maxHeight,d[1][1]-d[0][1])
            maxWidth = max(maxWidth,d[1][0]-d[0][0])
        #let them be even
        maxHeight = (int(maxHeight/2)+1)*2
        maxWidth = (int(maxWidth/2)+1)*2
        #adjust all digits to max
        for d in self.foundDigits:
            if d is None: continue
            height=d[1][1]-d[0][1]
            width=d[1][0]-d[0][0]
            offsetX=(maxWidth-width)/2
            offsetY=(maxHeight-height)/2
            d[0] = ( int(d[0][0]-offsetX), int(d[0][1]-offsetY) )
            d[1] = ( int(d[1][0]+offsetX), int(d[1][1]+offsetY) )

    def debugDump(self):
        if CFG.DEBUG:
            print("Extractor: {} red boxes".format(len(self.redBoxes)))
            copy=self.image.copy()
            for r in self.redBoxes:
                cv2.rectangle(copy,r[0],r[1],(255,0,0),3)
            for b in self.redBands:
                cv2.rectangle(copy,b[0],b[1],(0,255,0),3)
            cv2.imwrite(path.join(CFG.DEBUG_FOLDER,'debug-extract-boxes.jpg'),copy)
            for i,r in enumerate(self.redROIs):
                print("ROI {}: {} digits".format(i,len(self.digitSets[i])))
                copy=r.copy()
                for d in self.digitSets[i]:
                    cv2.rectangle(copy,d[0],d[1],255,1)
                cv2.imwrite(path.join(CFG.DEBUG_FOLDER,'debug-extract-roi-{}.jpg'.format(i)),copy)
            print("Found ROI {} with confidence {}".format(
                self.foundIndex,self.foundConfidence))
            for i,d in enumerate(self.foundDigits):
                print("Digit {} is {}".format(i,d))
                dr = self.getDigitROI(i)
                if dr is not None:
                    cv2.imwrite(path.join(CFG.DEBUG_FOLDER,"debug-extract-d{}.jpg".format(i)),dr)

if __name__=="__main__":
    img = cv2.imread(sys.argv[1])
    proc = ImagePreprocessor(img)
    ex=Extractor(proc.image)
    ex.process()

