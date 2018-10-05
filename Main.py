from PIL import Image
import EdgeDetector
from EdgeDetector import CropImage
import Constants
import timeit as Timer


# Parts dictionary (x, y): Image
ImageParts = {}

# todo: insert some preprocessing to reduce


def Main():
    a = Timer.default_timer()
    #image = Image.open("C:/Users/valer/Desktop/a.jpg", "r")
    image = Image.open(Constants.FilePath, "r")

    #height = 100
    #width = 100

    # for x in range(0, image.size[0], width):
    #	for y in range(0, image.size[1], height):
    #		part = CropImage(image, x, y, width, height)
    #		ImageParts [int( x / width ), int( y / height)] = part
    # for (key1, key2), value in ImageParts.items():
    #	print(str(key1) + " : " + str(key2) + " || " + str(value))
    #ImageParts.get((5, 4)).show()
    #img = Smoother(ImageParts[5, 4])
    #img = Smoother(image)
    # image.show()

    img = EdgeDetector.TransformToGrey(image)
    img = EdgeDetector.SmoothGrey(img)
    (img, angImg) = EdgeDetector.SobelOperator(img)
    img = EdgeDetector.NonMaximumSuppression(img, angImg)
    img = EdgeDetector.DoubleThresholding(
        img, Constants.LowerBound, Constants.HigherBound)
    img = EdgeDetector.BlobAnalysis(
        img, Constants.MaxColorValue, Constants.MinColorValue)
    img.show()
    print(Timer.default_timer()-a)


Main()
