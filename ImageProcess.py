import cv2
import numpy as np
from Config import Config as CFG

class ImagePreprocessor:
    def __init__(self,img,debug=False):
        self.original = img
        self.__skew = None
        self.__image = None
        self.__horizLines = None

    @property
    def skew(self):
        if self.__skew is None:
            self.process()
        return self.__skew
    @property
    def image(self):
        if self.__image is None:
            self.process()
        return self.__image

    @property
    def threshold(self):
        if self.__thresh is None:
            _,self.__thresh=cv2.threshold(self.gray,0,255,\
                                          cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            #self.__thresh=cv2.adaptiveThreshold(self.gray,255,\
            #                                    cv2.ADAPTIVE_THRESH_MEAN_C,\
            #                                    cv2.THRESH_BINARY,11,2)
        return self.__thresh

    def process(self):
        gray=cv2.cvtColor(self.original,cv2.COLOR_BGR2GRAY)
        #remove noise
        kernel = np.ones((3,3),np.uint8)
        gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
        #find the edges
        edges = cv2.Canny(gray,CFG.CANNY_MIN,CFG.CANNY_MAX)
        #level image by finding horizontal lines and rotating
        self.__skew = self.detectSkew(edges)
        self.__image = self.levelImage(self.original)
        self.DebugDump()

    def detectSkew(self,edges):
        #call with binary img (eg edges)
        thresh = max(int(edges.shape[0]*0.1),CFG.HOUGH_MIN_THRESH)
        lines=cv2.HoughLines(edges,1,np.pi/180,thresh)
        if lines is None:
            print("No HoughLines detected, cannot adjust level")
            return 0.0
        if CFG.DEBUG:
            print("HoughLines detected {} lines".format(len(lines)))
        #find horizontal lines and their angle average
        horizLines = []
        horizAvg = 0.
        for line in lines:
            rho,theta=line[0][0],line[0][1]
            #check if line is horizontal (with LEVEL_THRESH accuracy)
            theta_min=(90.-CFG.LEVEL_THRESH)*np.pi/180
            theta_max=(90.+CFG.LEVEL_THRESH)*np.pi/180
            if theta_min < theta < theta_max:
                horizLines.append([rho,theta])
                horizAvg += theta
        #calc average
        if len(horizLines)>0:
            horizAvg /= len(horizLines)
        skew = (horizAvg*180/np.pi)-90
        self.__horizLines = horizLines
        self.__skew = skew
        return skew

    def levelImage(self,img):
        rows,cols=img.shape[0],img.shape[1]
        matrix=cv2.getRotationMatrix2D((cols/2,rows/2),self.skew,1)
        rotated=cv2.warpAffine(img,matrix,(cols,rows))
        return rotated

    def resizeImage(self):
        max_dim = max(self.original.shape[0],self.original.shape[1])
        ratio = CFG.MAX_IMG_SIZE/max_dim
        if ratio < 1.:
            self.original = cv2.resize(self.original,None,fx=ratio,fy=ratio,\
                                    interpolation = cv2.INTER_CUBIC)

    def DebugDump(self):
        if CFG.DEBUG:
            print("Average rotation angle from {} horiz lines: {}"
                  .format(len(self.__horizLines),self.__skew))
            #debug write image with detected horiz lines
            copy = self.original.copy()
            for rho, theta in self.__horizLines:
                a,b = np.cos(theta),np.sin(theta)
                x0,y0 = a*rho,b*rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))
                cv2.line(copy,(x1,y1),(x2,y2),(255,0,0),2)
            cv2.imwrite('debug-process-lines.jpg',copy)

