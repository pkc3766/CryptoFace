import decimal
import math
import pickle
import cv2
import Encryption.Key as Key
import Encryption.Images
from PIL import Image

getIfromRGB = lambda val: int(
    (val[0] << 16) + (val[1] << 8) + val[2])  # this lamda expression converts pixel value(rgb) to int
getRGBfromI = lambda val: ((val >> 16) & 255, (val >> 8) & 255, val & 255)

class FileDecryption:
    def __init__(self):
        self.retrievedKey = Key.keyFile()
        self.l = None
        self.x = None
        self.sigma = None
        self.xs = None
        self.n_seg = None

    def decrypt(self,filename):
        filepath = '../Encryption/Images/'+filename
        img = Image.open(filepath)
        pixelMap = img.load()
        with open('../Encryption/key.pkl', 'rb') as input:
            self.retrievedKey=pickle.load(input)
        for val in self.retrievedKey.constants:
            print(val)
            print("\n")
        cordinates = self.retrievedKey.cordinates
        # image = cv2.imread(filepath)
        # for x, y, w, h in cordinates:
        #     cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0))
        # # show the images
        # cv2.imshow("faces found", image)
        # cv2.waitKey(0)
        allfaces = []
        for cordinate in cordinates:
            allfaces.append(self.getFacePixels(cordinate, pixelMap))

        # ind = 0
        # while ind<len(allfaces):
        #     val=cordinates[ind][2]*cordinates[ind][3]
        #     val1=len(allfaces[ind])
        #     ind+=1
        #     print(val,val1,end=' ')
        ind = 0
        while ind < len(allfaces):
            self.initialise(self.retrievedKey, ind)
            # allfaces[ind] = self.reassemble(cordinates[ind], allfaces[ind])
            # self.fixImage(cordinates[ind], allfaces[ind], pixelMap)
            # self.putback(cordinate, pixelMap, allfaces[ind])
            x = cordinates[ind][0]
            y = cordinates[ind][1]
            w = cordinates[ind][2]
            h = cordinates[ind][3]
            val = self.x
            # ret = pix.copy()
            # ret=[]
            # print(self.x, self.l, end='')
            # print("\n")
            indx = 0
            list1 = []
            print(self.l,val,end='\n')
            for j in range(y, y + h):
                for i in range(x, x + w):
                    val = (self.l) * (val) * (1 - val)
                    valconf = int(round(val * 16777215))  # val ^ int(round(log * 16777215))
                    # pixelsNew[i,j]=pixelsNew[i,j]^valconf
                    # value = pix[ind]
                    # value=getIfromRGB(pixelMap[i,j])
                    if indx <= 10:
                        list1.append(valconf)
                        # indxx+=1
                    allfaces[ind][indx] = (allfaces[ind][indx] ^ valconf)
                    pixelMap[i, j] = getRGBfromI(allfaces[ind][indx])
                    # pixelMap[i,j]=(0,0,255)
                    indx += 1
            ind+=1
            print(list1)
            print("\n")
            # if ind==0:
            #     path = "../Encryption/Images/image2.png"
            #     img.save(path)
            # else:
            #     path = "../Encryption/Images/image1.png"
            #     img.save(path)
            # ind += 1
        # for cordinate in cordinates:

            # ind += 1
        img.show()
        path = "../Encryption/Images/original.png"
        img.save(path)
        img.close()

    def getFacePixels(self, cordinate, pixelMap):
        x = cordinate[0]
        y = cordinate[1]
        w = cordinate[2]
        h = cordinate[3]
        pix = []
        for j in range(y,y+h):
            for i in range(x,x+w):
                value = getIfromRGB(pixelMap[i, j])
                pix.append(value)
        return pix

    def reassemble(self, cordinate, pix):
        i = 0
        # print("got in reassemble\n")
        # while i <= 10:
        #     print(pix[i], end=' ')
        #     i += 1
        # print("\n")
        size = cordinate[2] * cordinate[3]
        # no of segments into which face is divided
        n_seg = self.n_seg
        spix = int(math.ceil(size / n_seg))
        sigma = self.sigma  # random.randrange(8700000, 10000000)) / 10000000
        xs = self.xs # random.randrange(0, 10000000)) / 10000000
        num_seg = 0
        indx = 0
        xcurr = xs
        # print("got into variables\n")
        # print(xs,sigma,n_seg,end=' ')
        print("\n")
        ret = pix.copy()
        while num_seg < n_seg:
            start = indx

            ma = min(size, start + spix) - start  # size of pix array
            pos = [ok for ok in range(ma)]

            # scrambling is done here
            i = 0
            list1 = []

            while i < ma:
                val_s = sigma * decimal.Decimal(math.sin(decimal.Decimal(math.pi) * xcurr))
                position = int(round(val_s * decimal.Decimal(len(pos) - 1)))
                # print(position,end=' ')

                list1.append(pos[position])
                pos.remove(pos[position])

                xcurr = val_s
                i += 1
                indx += 1

            i = 0
            for ok in list1:
                ret[start + ok] = pix[start + i]
                i += 1
            num_seg += 1
        # x = cordinate[0]
        # y = cordinate[1]
        # w = cordinate[2]
        # h = cordinate[3]
        # ind = 0
        # for j in range(y, y + h):
        #     for i in range(x, x + w):
        #         value = ret[ind]
        #         ind += 1
        #         # it accepts a tuple of rgb values
        #         pixelMap[i, j] = getRGBfromI(value)

        return ret

    def fixImage(self, cordinate, pix, pixelMap):
        x = cordinate[0]
        y = cordinate[1]
        w = cordinate[2]
        h = cordinate[3]
        val = self.x
        # ret = pix.copy()
        # ret=[]

        ind = 0
        for j in range(y, y + h):
            for i in range(x, x + w):
                val = (self.l) * (val) * (1 - val)
                valconf = int(round(val * 16777215))#val ^ int(round(log * 16777215))
                # pixelsNew[i,j]=pixelsNew[i,j]^valconf
                # value = pix[ind]
                # value=getIfromRGB(pixelMap[i,j])
                pix[ind]=(pix[ind]^valconf)
                pixelMap[i,j]=getRGBfromI(pix[ind])
                ind+=1
                # it accepts a tuple of rgb values
        # return pix


    def initialise(self,obj,ind):
        values=obj.constants[ind]
        # print("hello")
        # print(values,end=' ')
        self.x=values[0]
        self.l=values[1]
        self.n_seg=values[2]
        self.sigma=values[3]
        self.xs=values[4]
        # print(self.xs,self.sigma,self.n_seg,end=' ')
        # print("hello\n")


    def putback(self, cordinate, pixelMap, pix):
        x = cordinate[0]
        y = cordinate[1]
        w = cordinate[2]
        h = cordinate[3]
        ind = 0
        for j in range(y, y + h):
            for i in range(x, x + w):
                pixelMap[i, j] = getRGBfromI(pix[ind])
                ind += 1

def main():
    obj=FileDecryption()
    obj.decrypt('encrypted.png')

main()
