from PIL import Image
import ImageFilter
from ImageFilter import CropImage
# Parts dictionary (x, y): Image
ImageParts = {}


def Main():
	#image = Image.open("C:/Users/valer/Desktop/a.jpg", "r")
	image = Image.open( "C:/Users/valer/Desktop/HabraCaptcha.jpg", "r" )

	#height = 100
	#width = 100

	#for x in range(0, image.size[0], width):
	#	for y in range(0, image.size[1], height):
	#		part = CropImage(image, x, y, width, height)
	#		ImageParts [int( x / width ), int( y / height)] = part
	#for (key1, key2), value in ImageParts.items():
	#	print(str(key1) + " : " + str(key2) + " || " + str(value))
	#ImageParts.get((5, 4)).show()
	#img = Smoother(ImageParts[5, 4])
	#img = Smoother(image)
	#image.show()

	img = ImageFilter.TransformToGrey(image)
	#img.show()

	img = ImageFilter.SmoothGrey( img )
	#img.show()

	( img, angImg ) = ImageFilter.SobelOperator(img)
	img.show()
	
	#angImg.show()
	img = ImageFilter.NonMaximumSuppression( img, angImg )
	img.show( )


Main()



