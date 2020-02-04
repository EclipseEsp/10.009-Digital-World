from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import argparse
import imutils
import numpy as np
import cv2

#ap = argparse.ArgumentParser()
#ap.add_argument("-i","--images", required=True, help="/home/pi/Desktop/canteenpic.jpeg")
#args = vars(ap.parse_args())                

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

imagePath = "/home/pi/Desktop/Canteen/canteen145.jpe"

image = cv2.imread(imagePath)
image = imutils.resize(image, width = min(800, image.shape[1]))
orig = image.copy()

(rects, weights) = hog.detectMultiScale(image,winStride=(4,4)
                                        ,padding=(4,4),scale=1.05) #padding(8,8) , scale 1.01

for (x,y,w,h) in rects:
    cv2.rectangle(orig, (x,y), (x+w,y+h),(0, 0, 255), 2)

rects = np.array([[x,y,x+w,y+h] for (x,y,w,h) in rects])
pick = non_max_suppression(rects, probs=None
                           ,overlapThresh= 0.65) #0.65 bigger value less overlap

for (xA,yA,xB,yB) in pick:
    cv2.rectangle(image,(xA,yA),(xB,yB),(0,255,0),2)

filename = imagePath#[imagePath.rfind("/")+1:]
print("[INFO] {}: {} original boxes, {} after suppression".format(filename, len(rects), len(pick)))

#cv2.imshow("Before NMS" , orig)
#cv2.imshow("After NMS" , image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
cv2.imwrite('tuning_canteenpic.jpeg',image)
cv2.destroyAllWindows()
