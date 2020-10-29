import tkinter as tk
from tkinter import filedialog, Text

import cv2
from PIL import ImageTk, Image
import Encryption.Encrypt as enc
import Decryption.Decrypt as dec
import os

class Application:
    def __init__(self):
        self.window = tk.Tk()
        self.bgimg = "back.jpg"
        self.filedir = None
        self.file = None
        self.createWidgets(self.bgimg)

    def exit(self):
        self.window.destroy()
        return

    def upload(self):
        # dir= r"/Encryption/Images"
        self.filedir = filedialog.askopenfilename(title='select images',
                           filetypes=[('Image Files', ['.jpeg', '.jpg', '.png', ])])
        # print(self.filedir)
        a = self.filedir.split('/')
        self.file = a[len(a) - 1]
        print(self.file)
        # print(filename)


    # def encrypt(self):
    #     a=self.filedir.split('/')
    #     filename=a[len(a)-1]
    #     enc.main(filename)
    #     return

    def createWidgets(self,filename):
        # create a canvas with background image
        self.window.title("Face Cryptography")
        self.window.iconbitmap("")
        self.window.geometry('610x500')
        frame=tk.Frame(self.window,width=500,height=300,highlightbackground='red'
                       ,highlightthickness=3)
        frame.grid(row=0,column=0)
        folder = "Images"
        # self.canvas = tk.Canvas(frame, height=1000, width=1000, bg="white")
        image = ImageTk.PhotoImage(Image.open(os.path.join(folder, filename)))
        # image=cv2.imread("Images\\pic.jpg")
        label = tk.Label(image=image)
        label.grid(row=0, column=0)
        # frame.pack()
        # create buttons
        buttonframe = tk.Frame(self.window,width=500,height=100)
        buttonframe.grid(row=1,column=0)
        upload_image = tk.Button(buttonframe,bg="black",fg="white",text="uploadImage"
                               ,padx=10,pady=10,command=self.upload)
        encrypt_image = tk.Button(buttonframe,bg="black",fg="white",text="encrypt"
                               ,padx=10,pady=10,command=lambda:enc.main(self.file))
        share_image = tk.Button(buttonframe,bg="black",fg="white",text="share"
                               ,padx=10,pady=10)
        decrypt_image = tk.Button(buttonframe,bg="black",fg="white",text="decrypt"
                               ,padx=10,pady=10,command=dec.main)
        exit = tk.Button(buttonframe, bg="black", fg="white", text="exit"
                                  , padx=10, pady=10,command=self.exit)
        upload_image.grid(row=0,column=0,sticky='E',padx=10,pady=10)
        encrypt_image.grid(row=0,column=1,sticky='E',padx=10,pady=10)
        share_image.grid(row=0,column=2,sticky='E',padx=10,pady=10)
        decrypt_image.grid(row=0,column=3,sticky='E',padx=10,pady=10)
        exit.grid(row=0,column=4,sticky='E',padx=10,pady=10)
        # buttonframe.pack()
        self.window.mainloop()


def main():
    Application()

main()


