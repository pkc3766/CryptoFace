import decimal
import math
import pickle

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
        # print("decryption is done here")
        filepath = '../Encryption/Images/'+filename
        img = Image.open(filepath)
        pixelMap = img.load()
        # retrievedKey = Key()
        with open('../Encryption/key.pkl', 'rb') as input:
            self.retrievedKey=pickle.load(input)
        cordinates = self.retrievedKey.cordinates
        # print(cordinates)
        # print("\n")
        # print(cordinates,end=' ')
        allfaces = []
        for cordinate in cordinates:
            allfaces.append(self.getFacePixels(pixelMap,cordinate))
        # print("ecrypted\n")
        # for face in allfaces:
        #     ind = 0
        #     while ind < 10:
        #         print(face[ind], end=' ')
        #         ind = ind + 1
        #     print("\n")
        # # for l in allfaces:
        # #     print(l,end=' ')
        # # print(len(allfaces))
        ind = len(allfaces)-1

        while ind>=0:
            self.initialise(self.retrievedKey,ind)
            # print(allfaces[ind])
            allfaces[ind]=self.reassemble(cordinates[ind],pixelMap,allfaces[ind])
            # print(allfaces[ind])
            allfaces[ind]=self.fixImage(cordinates[ind],pixelMap,allfaces[ind])
            # print(allfaces[ind],end="\n")
            self.putback(cordinates[ind],pixelMap,allfaces[ind])
            ind-=1

        # print("original\n")
        # for face in allfaces:
        #     ind = 0
        #     while ind < 10:
        #         print(face[ind], end=' ')
        #         ind = ind + 1
        #     print("\n")
        img.show()
        path = "../Encryption/Images/encrypted.png"
        img.save(path)
        img.close()

    def getFacePixels(self, pixelMap, cordinate):
        x = cordinate[0]
        y = cordinate[1]
        w = cordinate[2]
        h = cordinate[3]
        pix = []
        for j in range(y,y+h):
            for i in range(x,x+w):
                pix.append(getIfromRGB(pixelMap[i,j]))
        return pix

    def reassemble(self, cordinate, pixelMap, pix):
        size = cordinate[2] * cordinate[3]
        # no of segments into which face is divided
        n_seg =self.n_seg
        spix = int(math.ceil(size / n_seg))
        sigma = self.sigma  # random.randrange(8700000, 10000000)) / 10000000
        xs = self.xs # random.randrange(0, 10000000)) / 10000000
        num_seg = 0
        indx = 0
        xcurr = xs
        # print(xs,sigma,n_seg,end=' ')
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
                position = round(val_s * decimal.Decimal(len(pos) - 1))

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
        x = cordinate[0]
        y = cordinate[1]
        w = cordinate[2]
        h = cordinate[3]
        ind = 0
        for j in range(y, y + h):
            for i in range(x, x + w):
                value = ret[ind]
                ind += 1
                # it accepts a tuple of rgb values
                pixelMap[i, j] = getRGBfromI(value)
        return ret

    def fixImage(self, cordinate, pixelMap, pix):
        x = cordinate[0]
        y = cordinate[1]
        w = cordinate[2]
        h = cordinate[3]
        val = self.x
        # ret=pix.copy()
        ret=[]
        ind=0
        for j in range(y, y + h):
            for i in range(x, x + w):
                val = (self.l) * (val) * (1 - val)
                valconf = round(val * 16777215)
                # pixelsNew[i,j]=pixelsNew[i,j]^valconf
                # value = pix[ind]
                value=getIfromRGB(pixelMap[i,j])
                ret.append((value^valconf))
                pixelMap[i,j]=getRGBfromI(ret[ind])
                ind+=1
                # it accepts a tuple of rgb values
        return ret


    def initialise(self,obj,ind):
        values=obj.constants[ind]
        # print("hello")
        # print(values,end=' ')
        self.x=values[0]
        self.l=values[1]
        self.n_seg=values[2]
        self.sigma=values[3]
        self.xs=values[4]
        # print(self.x,self.l,self.n_seg,self.sigma,self.xs,end=' ')
        # print("\n")


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
