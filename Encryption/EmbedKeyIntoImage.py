#Steganography
import cv2
import os

HEADER_FILENAME_LENGTH: int= 30
HEADER_FILESIZE_LENGTH= 20
HEADER_LENGTH = HEADER_FILENAME_LENGTH +  HEADER_FILESIZE_LENGTH

#n: 104 ---> [011, 010, 00]
getBits = lambda n : [n >> 5, (n&0x1C)>>2, n&0x3]

#bits[011, 010, 00] ---> 104
getByte = lambda bits: (((bits[0]<<3) | bits[1])<<2)|bits[2]

def get_file_size(fileName):
	try:
		return os.stat(fileName).st_size
	except:
		return 0

def generate_header(fileName):
	qty = get_file_size(fileName)
	if qty == 0:
		return None

	#compose header for fileName
	#fileName: 'd:/images/work.jpg
	#splitted: [d:, images, work.jpg]

	name= fileName.split('/')[-1] #work.jpg
	name_extension = name.split('.') #[work, jpg]
	ext_len = len(name_extension[1]) + 1
	name_len = HEADER_FILENAME_LENGTH - ext_len
	name = name_extension[0][:name_len] + '.' + name_extension[1]

	name = name.ljust(HEADER_FILENAME_LENGTH, '*')

	qty = str(qty).ljust(HEADER_FILESIZE_LENGTH,'*')
	return name+qty


def embed(resultant_img, source_img, file_to_embed):
	#load the image as numpy.ndarray
	image = cv2.imread(source_img, cv2.IMREAD_COLOR)
	if image is None:
		print(source_img,'not found')
		return

	#check the file to embed
	fs = get_file_size(file_to_embed)
	if fs == 0:
		print(file_to_embed, 'not found')
		return

	#capacity check
	h,w,_ = image.shape
	if h*w < fs + HEADER_LENGTH:
		print('Insufficient Embedding Capacity')
		return

	#embed
	#order : header, file
	header = generate_header(file_to_embed)
	fh = open(file_to_embed, 'rb')
	i = 0
	cnt = 0
	data = 0
	keepEmbedding = True
	while i < h and keepEmbedding:
		j=0
		while j < w:
			#get the data
			if cnt < HEADER_LENGTH:#either from header
				data = ord(header[cnt])
			else:#or from file
				data = fh.read(1)#read one byte from the file
				if data:
					# as the file is opened in binary mode
					# so we get byte objects on read
					# the byte object dont support bitwise operations
					# hence they are to be converted to int
					data = int.from_bytes(data, byteorder='big')
				else:#EOF
					keepEmbedding = False
					break

			bits = getBits(data)

			image[i,j,2] = (image[i,j,2]& ~0x7) | bits[0] #embed in red band
			image[i,j,1] = (image[i,j,1]& ~0x7) | bits[1] #embed in green band
			image[i,j,0] = (image[i,j,0]& ~0x3) | bits[2] #embed in blue band

			cnt+=1
			j+=1
		i+=1

	#close the file
	fh.close()

	#save back the image
	cv2.imwrite(resultant_img, image)
	print('Embedding Done')
