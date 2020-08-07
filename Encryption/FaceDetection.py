import cv2

class Detection:


    def __init__(self, filepath):
        self.filepath=filepath


    def faceDetector(self):
        #print(self.filename)
        imagePath =self.filepath
        cascPath = cv2.data.haarcascades+'haarcascade_frontalface_default.xml'
        # create a face cascade
        faceCascade = cv2.CascadeClassifier(cascPath)
        # read a image
        image = cv2.imread(imagePath)
        # convert image to gray image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.3, 4)
        # for x, y, w, h in faces:
        #     cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0))
        # # show the images
        # cv2.imshow("faces found", image)
        # cv2.waitKey(0)
        return faces


    def getFaceCordinates(self):
        cordinates = []
        faces=self.faceDetector()
        for x,y,w,h in faces:
            li = [x,y,w,h]
            flag = type(li) is tuple
            #print(flag)
            cordinates.append(li)
            #print(li,end=' ')
        return cordinates


#obj = Detection('Images//image2.png')
#obj.faceDetector()
#obj.getFaceCordinates()
