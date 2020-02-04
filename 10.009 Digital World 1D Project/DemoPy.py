from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
from picamera import PiCamera
from time import sleep
import argparse
import imutils
import numpy as np
import cv2
import pyrebase
import time

#ap = argparse.ArgumentParser()
#ap.add_argument("-i","--images", required=True, help="/home/pi/Desktop/canteenpic.jpeg")
#args = vars(ap.parse_args())                
""" ------------- FIREBASE SETUP -------------"""
print("Setting up Firebase...")
url = "https://digitalworld-a7fd7.firebaseio.com/"
apikey = "AIzaSyBHXFPfYxwQSdjQh43IXWTBQLl7OxNzXcE"
urlstore ="digitalworld-a7fd7.appspot.com"
auth = "digitalworld-a7fd7.firebaseapp.com"

config = {
    "apiKey": apikey,
    "authDomain": auth,
    "databaseURL": url,
    "storageBucket": urlstore
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()
storage = firebase.storage()
print("Firebase Setup Successful")
print('\n')
""" ----------- End of FIREBASE SETUP -------------"""

""" ------------------ Pi Camera ------------------ """
print("Taking a picture...")
camera = PiCamera()
cameraPath = '/home/pi/Desktop/image.jpg'
camera.start_preview()
sleep(5)
camera.capture(cameraPath)
camera.stop_preview()
print("Picture Saved to : ",'/home/pi/Desktop/image.jpg')
print('\n')
""" --------------- Endo Of Pi Camera ------------- """

""" ------------- OPENCV PORTION -------------"""
print("Starting OpenCV...")

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

imagePath = "/home/pi/Desktop/Canteen/canteen145.jpe"

image = cv2.imread(cameraPath) #imagePath / cameraPath
image = imutils.resize(image, width = min(1000, image.shape[1])) #default 800
orig = image.copy()

(rects, weights) = hog.detectMultiScale(image,winStride=(3,3) #last tested
                                        ,padding=(8,8),scale=1.05)
                            #lower winStride, more accurate/detections but more processing time.
                            #padding(8,8) , scale 1.01 (Default Parameters)
                            #winStride=(4,4) #padding=(4,4) #scale=1.05 (Good for canteen)
                            #winStride=(2,2) #padding=(8,8) #scale=1.05 (Good for close up)

for (x,y,w,h) in rects:
    cv2.rectangle(orig, (x,y), (x+w,y+h),(0, 0, 255), 2)

rects = np.array([[x,y,x+w,y+h] for (x,y,w,h) in rects])
pick = non_max_suppression(rects, probs=None
                           ,overlapThresh= 0.65) #0.65 bigger value less overlap

for (xA,yA,xB,yB) in pick:
    cv2.rectangle(image,(xA,yA),(xB,yB),(0,255,0),2)

filename = cameraPath#[imagePath.rfind("/")+1:]
print("[INFO] {}: {} original boxes, {} after suppression".format(filename, len(rects), len(pick)))

#cv2.imshow("Before NMS" , orig)
#cv2.imshow("After NMS" , image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
cv2.imwrite('processed_canteenpic.jpeg',image)
cv2.destroyAllWindows()
total_count = len(pick)
print("OpenCV Processing Successful")
print("No. of people detected:",total_count)
print('\n')
""" ------------ END Of OPENCV PORTION ------------ """

""" --------- Starting Upload to Firebase --------- """
print("Uploading Images to Firebase...")

storeimgurl = "images/canteenpic.jpeg"
storeimgurl_processed = "opencv_images/processed_canteenpic.jpeg"
# Store canteenpic(unprocessed from camera into images/ folder)
# Store proccessed_canteenpic(from desktop into opencv_images/ folder)
storage.child(storeimgurl).put(cameraPath) #imagePath/cameraPath
storage.child(storeimgurl_processed).put("processed_canteenpic.jpeg")
print("Firebase Image Upload Successful")

ts = time.gmtime()
current_time = time.strftime("%Y-%m-%d %H:%M:%S",ts)
print("Picture taken on: ",current_time)
#database.child("canteen").set(total_count)
database.child("canteen").child(current_time).set(total_count)
canteen = database.child("canteen").get()
print(canteen.key(), canteen.val())
print("Firebase Upload Successful")
print('\n')
""" --------- End Of Upload to Firebase --------- """
