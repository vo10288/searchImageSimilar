#!/usr/bin/python3.11

# by Antonio "Visi@n" Broi        antonio@tsurugi-linux.org
# https://tsurugi-linux.org
# 20230407

# 
# LICENSE M.I.T. https://opensource.org/licenses/MIT
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS 
#OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
#OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Example: imageDifferenceHash_dirlist.py -i imagetest.jpg -o imagesTosearch/

# Import dependencies
from PIL import Image
import imagehash
import argparse
import os
from datetime import datetime
import time
import psutil

##
from imutils import paths
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--inputimage", required=True, 
	help="first image to compare")
ap.add_argument("-o", "--outputdirectory", required=True,
	help="directory images to compare")
		
args = vars(ap.parse_args())


first_image = Image.open(args["inputimage"])
#first_image.show()

average = "average"
if not os.path.exists(average):
	os.makedirs(average)
	
filenameAVERAGE = str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))+".csv"
filenameAVERAGE = open(average+"/"+filenameAVERAGE, "w")
filenameAVERAGE.write("IMAGE_1"+","+"IMAGES_COMPARE"+","+"HASH_AVERAGE_1"+","+"HASH_AVERAGE_COMPARE"+"\n")

phash = "phash"
if not os.path.exists(phash):
	os.makedirs(phash)
filenamePHASH = str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))+".csv"
filenamePHASH = open(phash+"/"+filenamePHASH, "w")
filenamePHASH.write("IMAGE_1"+","+"IMAGES_COMPARE"+","+"HASH_PHASH_1"+","+"HASH_PHASH_COMPARE"+"\n")

dhash = "dhash"
if not os.path.exists(dhash):
	os.makedirs(dhash)
filenameDHASH = str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))+".csv"
filenameDHASH = open(dhash+"/"+filenameDHASH, "w")
filenameDHASH.write("IMAGE_1"+","+"IMAGES_COMPARE"+","+"HASH_DHASH_1"+","+"HASH_DHASH_COMPARE"+"\n")

whash = "whash"
if not os.path.exists(whash):
	os.makedirs(whash)
filenameWHASH = str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))+".csv"
filenameWHASH = open(whash+"/"+filenameWHASH, "w")
filenameWHASH.write("IMAGE_1"+","+"IMAGES_COMPARE"+","+"HASH_WHASH_1"+","+"HASH_WHASH_COMPARE"+"\n")
### £££££££££££££££££££££££££££££££££
imagePaths = list(paths.list_images(args["outputdirectory"]))
#data = []
#try:
	
	
	# loop over the image paths
for (i, imagePath) in enumerate(imagePaths):
	# load the input image and convert it from RGB (OpenCV ordering)
	# to dlib ordering (RGB)
	print("[INFO] processing image {}/{}".format(i + 1,
		len(imagePaths)))
	print(imagePath)
### £££££££££££££££££££££££££££££££££

# make a list of all available images 
#images = os.listdir(args["outputdirectory"]) 

#for image in images:
	
	#####################################################################
	### AVERAGE HASH DISTANCE
	# Create the Hash Object of the first image
	Image1 = imagehash.average_hash(Image.open(args["inputimage"]))
	print('The first picture: ' + str(Image1))

	# Create the Hash Object of the second image
	Image2 = imagehash.average_hash(Image.open(imagePath))
	print('The second picture: ' + str(Image2))
	
	second_image = Image.open(imagePath)
	
	# Compare hashes to determine whether the pictures are the same or not
	if(Image1 == Image2):
		print("AVERAGE: The pictures are perceptually the same! distance: " + str(Image1 - Image2))
		print(str(args["inputimage"])+" <<<->>> "+str(imagePath))
		first_image.show("IMAGE TOC COMPARE")

		second_image.show()
		filenameAVERAGE.write(str(args["inputimage"])+","+str(imagePath)+","+str(Image1)+","+str(Image2)+"\n")
		time.sleep(3)
		# hide image
		for proc in psutil.process_iter():
			if proc.name() == "display":
				proc.kill()

	else:
		print("AVERAGE: The pictures are different, distance: " + str(Image1 - Image2))
		print(str(args["inputimage"])+" <<<->>> "+str(imagePath))
		# display image for 10 seconds
		
		
	print("   ")
	print("   ")
    
	#####################################################################
	### PHASH HASH DISTANCE
	# Create the Hash Object of the first image
	Image1 = imagehash.phash(Image.open(args["inputimage"]))
	print('The first picture: ' + str(Image1))

	# Create the Hash Object of the second image
	Image2 = imagehash.phash(Image.open(imagePath))
	print('The second picture: ' + str(Image2))

	
	# Compare hashes to determine whether the pictures are the same or not
	if(Image1 == Image2):
		print("PHASH: The pictures are perceptually the same ! distance: " + str(Image1 - Image2))
		print(str(args["inputimage"])+" <<<->>> "+str(imagePath))
		first_image.show()

		second_image.show()
		filenamePHASH.write(str(args["inputimage"])+","+str(imagePath)+","+str(Image1)+","+str(Image2)+"\n")
		time.sleep(3)
		# hide image
		for proc in psutil.process_iter():
			if proc.name() == "display":
				proc.kill()

	else:
		print("PHASH: The pictures are different, distance: " + str(Image1 - Image2))
		print(str(args["inputimage"])+" <<<->>> "+str(imagePath))
	print("   ")
	print("   ")
	########################################################################
	### DHASH HASH DISTANCE   
	# Create the Hash Object of the first image
	Image1 = imagehash.dhash(Image.open(args["inputimage"]))
	print('The first picture: ' + str(Image1))

	# Create the Hash Object of the second image
	Image2 = imagehash.dhash(Image.open(imagePath))
	print('The second picture: ' + str(Image2))


	# Compare hashes to determine whether the pictures are the same or not
	if(Image1 == Image2):
		print("DHASH: The pictures are perceptually the same! distance: " + str(Image1 - Image2))
		print(str(args["inputimage"])+" <<<->>> "+str(imagePath))
		first_image.show()

		second_image.show()
		filenameDHASH.write(str(args["inputimage"])+","+str(imagePath)+","+str(Image1)+","+str(Image2)+"\n")
		time.sleep(3)
		# hide image
		for proc in psutil.process_iter():
			if proc.name() == "display":
				proc.kill()

	else:
		print("DHASH: The pictures are different, distance: " + str(Image1 - Image2))
		print(str(args["inputimage"])+" <<<->>> "+str(imagePath))
	print("   ")
	print("   ")

	####################################################################
	### WHASH HASH DISTANCE
	# Create the Hash Object of the first image
	Image1 = imagehash.whash(Image.open(args["inputimage"]))
	print('The first picture: ' + str(Image1))

	# Create the Hash Object of the second image
	Image2 = imagehash.whash(Image.open(imagePath))
	print('The second picture: ' + str(Image2))

	# Compare hashes to determine whether the pictures are the same or not
	if(Image1 == Image2):
		print("WHASH: The pictures are perceptually the same! distance: " + str(Image1 - Image2))
		print(str(args["inputimage"])+" <<<->>> "+str(imagePath))
		first_image.show()

		second_image.show()
		filenameWHASH.write(str(args["inputimage"])+","+str(imagePath)+","+str(Image1)+","+str(Image2)+"\n")

		time.sleep(3)
		# hide image
		for proc in psutil.process_iter():
			if proc.name() == "display":
				proc.kill()

	else:
		print("WASH: The pictures are different, distance: " + str(Image1 - Image2))
		print(str(args["inputimage"])+" <<<->>> "+str(imagePath))    
    
	print("   ")
	print("   ")

#time.sleep(10)

		# hide image
#for proc in psutil.process_iter():
#	if proc.name() == "display":
#		proc.kill()
filenameAVERAGE.close()
filenameDHASH.close()
filenamePHASH.close()
filenameWHASH.close()
