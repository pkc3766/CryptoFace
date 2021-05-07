import os

import cv2
from PIL import ImageTk, Image


class Detection:


    def __init__(self, filepath):
        self.filepath=filepath


    def faceDetector(self):
        print('Face Detection')
        cascPath = cv2.data.haarcascades+'haarcascade_frontalface_default.xml'
        # create a face cascade
        faceCascade = cv2.CascadeClassifier(cascPath)
        image=cv2.imread(self.filepath)
        if image is None:
            print("could not load")
        # convert image to gray image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.3, 4)
        return faces


    def getFaceCordinates(self):
        cordinates = []
        faces=self.faceDetector()
        for x,y,w,h in faces:
            li = [x,y,w,h]
            flag = type(li) is tuple
            cordinates.append(li)
        return cordinates

