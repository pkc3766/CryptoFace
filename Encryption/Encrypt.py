import random

from Encryption.FaceDetection import Detection

from PIL import Image

getIfromRGB = lambda val: int(
    (val[0] << 16) + (val[1] << 8) + val[2])  # this lamda expression converts pixel value(rgb) to int
getRGBfromI = lambda val: ((val >> 16) & 255, (val >> 8) & 255, val & 255)  # this function gives rgb value from int

class FileEncryption:
    def __init__(self,filename):
        self.filepath = "Images\\"+filename
        self.l = None
        self.x=None
        self.obj=None



    def confusion(self):
        print("confusion" ,end="\n")
        self.obj=Detection(self.filepath)
        cordinates = self.obj.getFaceCordinates()
        self.getInitialValues()
        allfacepixels=[]

        val=self.x
        #flag = type(allfacepixels) is list
        #print(flag)

        im = Image.open(self.filepath)
        pixelMap = im.load()
        img = im.copy()
        pixelsNew = img.load()
        # img.show()
        for cordinate in cordinates:
            self.modifyFace(cordinate, pixelsNew)
        #removing the confusion
        # for cordinate in cordinates:
        #     self.modifyFace(cordinate, pixelsNew)
        im.close()
        img.show()
        path = "Images\\encrypted.png"
        img.save(path)
        img.close()



    def modifyFace(self,cordinate,pixelsNew):
        print("Image pixels modified")

        x = cordinate[0]
        y = cordinate[1]
        w = cordinate[2]
        h = cordinate[3]

        ind=0
        val=self.x
        for i in range(x, x + h ):
            for j in range(y, y + w):
                val=(self.l)*(val)*(1-val)
                valconf=round(val* 16777215)
                # pixelsNew[i,j]=pixelsNew[i,j]^valconf
                value=getIfromRGB(pixelsNew[i,j])
                #it accepts a tuple of rgb values
                pixelsNew[i,j]=getRGBfromI(value^valconf)
                ind+=1


    def diffusion(self):
        print("diffusion",end="\n")

    def getInitialValues(self):
        # print("getIntialValues",end=' ')
        # select a random value between a and b inclusive both
        self.l=random.randint(3560000,4000000)/1000000
        self.x=random.randint(0,1000000)/1000000

obj = FileEncryption('image2.png')
obj.confusion()





