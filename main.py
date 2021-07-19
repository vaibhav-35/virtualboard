import cv2 as cv
import numpy as np

#for multiple cameras
cameraIdx = 0


CamFound = False

while not CamFound:
    currIdx = 0
    checkVidSource = cv.VideoCapture(currIdx)

    while True:
        ret, frame = checkVidSource.read()

        cv.imshow("CurrentSource, Press 's' to use this source. 'n' and 'p' to navigate between sources",frame)

        key = cv.waitKey(1)

        if key == ord('s'):
            cameraIdx = currIdx
            CamFound = True
            break
        if key == ord('n'):#upper or right arrow key press
            print("Increase index")
            currIdx+=1
            break   
        if key == ord('p'):#lower or left arrow key press
            print("Decrease index")
            
            if currIdx >=0: 
                currIdx-=1
            break
        if key == 27 :#esc to exit anyway
            print("esc")
            CamFound = True
            break

    if CamFound:
        checkVidSource.release()
        cv.destroyAllWindows()
        break



cap=cv.VideoCapture(cameraIdx)
                
def nothing(x):
    pass

#Create trackbar to adjust HSV range
cv.namedWindow("trackbar")
cv.createTrackbar("L-H","trackbar",0,179,nothing)
cv.createTrackbar("L-S","trackbar",0,255,nothing)
cv.createTrackbar("L-V","trackbar",0,255,nothing)
cv.createTrackbar("U-H","trackbar",179,179,nothing)
cv.createTrackbar("U-S","trackbar",255,255,nothing)
cv.createTrackbar("U-V","trackbar",255,255,nothing)

while True:
    ret,frame =cap.read()
    cv.putText(frame, 'Adjust sliders till you only see pointer, Press "s" to save', (50, 50), cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 2, cv.LINE_4)

    hsv=cv.cvtColor(frame,cv.COLOR_BGR2HSV)    
    
    l_h=cv.getTrackbarPos("L-H","trackbar")
    l_s=cv.getTrackbarPos("L-S","trackbar")
    l_v=cv.getTrackbarPos("L-V","trackbar")
    h_h=cv.getTrackbarPos("U-H","trackbar")
    h_s=cv.getTrackbarPos("U-S","trackbar")
    h_v=cv.getTrackbarPos("U-V","trackbar")
   
    low=np.array([l_h,l_s,l_v])
    high=np.array([h_h,h_s,h_v])

    mask=cv.inRange(hsv,low,high) 
    result=cv.bitwise_and(frame,frame,mask=mask)    
    cv.imshow("result",result)# If the user presses ESC then exit the program
    
    key = cv.waitKey(1)
    # If the user presses `s` then print and save this array.
    if key == ord('s'):
        thearray = [[l_h,l_s,l_v],[h_h, h_s, h_v]]
        # Save this array as penrange.npy
        np.save('penrange',thearray)
        break
    #if esc pressed exit
    if key == 27:
        break

cap.release()
cv.destroyAllWindows()


class drawingCanvas():
    def __init__(self):
        self.penrange = np.load('penrange.npy')
        self.cap = cv.VideoCapture(cameraIdx)
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
        cv.imshow('Esc to close, "c" to clear screem, "e" to change modes',self.frame)
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