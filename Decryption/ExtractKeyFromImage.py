# Steganography Extraction
import cv2

HEADER_FILENAME_LENGTH: int = 30
HEADER_FILESIZE_LENGTH = 20
HEADER_LENGTH = HEADER_FILENAME_LENGTH + HEADER_FILESIZE_LENGTH

# n: 104 ---> [011, 010, 00]
getBits = lambda n: [n >> 5, (n & 0x1C) >> 2, n & 0x3]

# bits[011, 010, 00] ---> 104
getByte = lambda bits: (((bits[0] << 3) | bits[1]) << 2) | bits[2]


def extract(resultant_img, target_folder):
    # load the image as numpy.ndarray
    image = cv2.imread(resultant_img, cv2.IMREAD_COLOR)
    if image is None:
        print(resultant_img, 'not found')
        return
    h, w, _ = image.shape
    # print( h*w*_  )
    # extract
    # order : header, file
    header = ''
    fh = None
    i = 0
    cnt = 0
    keepExtracting = True
    while i < h and keepExtracting:
        j = 0
        while j < w:
            # get the data
            bit1 = image[i, j, 2] & 0x7  # extract from red band
            bit2 = image[i, j, 1] & 0x7  # extract from green band
            bit3 = image[i, j, 0] & 0x3  # extract from blue band

            data = getByte([bit1, bit2, bit3])
            # print( data , end = ' ' )
            # put the data
            if cnt < HEADER_LENGTH:  # either into header
                # print( data , end=' ' )
                # print( chr(data) )
                header = header + chr(data)
            else:  # or into file
                if cnt == HEADER_LENGTH:
                    filename = target_folder + '/' + header[:HEADER_FILENAME_LENGTH].strip('*')
                    filesize = int(header[HEADER_FILENAME_LENGTH:].strip('*')) + cnt
                    fh = open(filename, 'wb')

                if cnt < filesize:
                    data = int.to_bytes(int(data), 1, byteorder='big')
                    fh.write(data)
                else:  # Done
                    fh.close()
                    keepExtracting = False
                    break
            cnt += 1
            j += 1
        i += 1

    print('Extracting Done')


# start here
# fileName = "image3.png"
# extract("../Encryption/Images/encrypted.png", "key.txt")
# print("key Extracted")
