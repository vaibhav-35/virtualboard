import cv2 as cv
import numpy as np


class drawingCanvas():
    def __init__(self):
        self.penrange = np.load('penrange.npy')
        self.cap = cv.VideoCapture(0)
        self.canvas = None
         
        self.x1,self.y1=0,0
        #used to toggle between pen and eraser mode
        self.val=1
        self.draw()

    def draw(self):
        while True:
            _, self.frame = self.cap.read()
            self.frame = cv.flip( self.frame, 1 )

            if self.canvas is None:
                self.canvas = np.zeros_like(self.frame)
            
            mask=self.CreateMask()
            contours=self.ContourDetect(mask)
            self.drawLine(contours)
            self.display()
            k = cv.waitKey(1) & 0xFF
            self.takeAction(k)
            
            #if esc key is pressed exit
            if k == 27:
                break        
    def CreateMask(self):
        hsv = cv.cvtColor(self.frame, cv.COLOR_BGR2HSV) 
        lower_range = self.penrange[0]
        upper_range = self.penrange[1]
        mask = cv.inRange(hsv, lower_range, upper_range)
        return mask
    
    def ContourDetect(self,mask):
        # Find Contours
        contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        return contours
    
    def drawLine(self,contours):
        #if contour area is not none and is greater than 100 draw the line
        if contours and cv.contourArea(max(contours, key = cv.contourArea)) > 100:                
            c = max(contours, key = cv.contourArea)    
            x2,y2,w,h = cv.boundingRect(c)
    
            if self.x1 == 0 and self.y1 == 0:
                self.x1,self.y1= x2,y2
            else:
                # Draw the line on the canvas
                self.canvas = cv.line(self.canvas, (self.x1,self.y1),(x2,y2), [255*self.val,0,0], 10)
            #New point becomes the previous point 
            self.x1,self.y1= x2,y2
        else:
            # If there were no contours detected then make x1,y1 = 0 (reset)
            self.x1,self.y1 =0,0        
    
    def display(self):
        # Merge the canvas and the frame.
        self.frame = cv.add(self.frame,self.canvas)    
        cv.imshow('Press Esc to close, "c" to clear screem, "e" to change modes',self.frame)
        cv.imshow('canvas',self.canvas)
    
    def takeAction(self,k):
        # When c is pressed clear the entire canvas
        if k == ord('c'):
            self.canvas = None
        #press e to change between eraser mode and writing mode
        if k==ord('e'):
            self.val= int(not self.val)
                   
if __name__ == '__main__':
    drawingCanvas()
    
cv.destroyAllWindows()