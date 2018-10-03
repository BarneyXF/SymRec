from PIL import Image
import math as Math
import numpy as NumPy

S = 1.4
K = 5

redConst = 0.299
greenConst = 0.587
blueConst = 0.114

HorizontalFilterKernel = [[1, 0, -1],
                          [2, 0, -2],
                          [1, 0, -1]
]

VerticalFilterKernel   = [[ 1,  2,  1],
                          [ 0,  0,  0],
                          [-1, -2, -1]
]

def TransformToGrey(ImagePic):
	ImagePic = ImagePic.convert('RGB')

	result = NumPy.asarray([[0 for x in range(ImagePic.size[0])] for y in range(ImagePic.size[1])])

	red, green, blue = ImagePic.split()

	red = NumPy.asarray(red)
	green = NumPy.asarray(green)
	blue = NumPy.asarray(blue)

	for y in range(ImagePic.size[ 0 ]):
		for x in range(ImagePic.size[ 1 ]):
			result[x ,y] = round(red[x, y] * redConst) + round(green[x, y] * greenConst) + round(blue[x, y] * blueConst)

	return Image.fromarray(result)


def CropImage(ImageToCrop, StartXPosition, StartYPosition, Width, Height):
	imageWidth = ImageToCrop.size[0]
	imageHeight = ImageToCrop.size[1]

	if StartXPosition > imageWidth:
		print("Width of slice to crop is greater that width of image")
		return
	elif Width + StartXPosition > imageWidth:
		Width = imageWidth - StartXPosition

	if StartYPosition > imageHeight:
		print("Height of slice to crop is greater that height of image")
		return
	elif Height + StartYPosition > imageHeight:
		Height = imageHeight - StartYPosition

	sliceSize = (StartXPosition, StartYPosition, StartXPosition + Width, StartYPosition + Height)
	return ImageToCrop.crop(sliceSize)


def GaussFunc(X, Y, Sigma):
	return  (1 / (2 * Math.pi * Sigma ** 2)) * Math.exp(-((X ** 2) + (Y ** 2)) / (2 * Sigma ** 2))


def GaussMask(Size, Sigma):
	shift = Math.floor( Size / 2 )

	mask = [[0 for x in range(Size)] for y in range(Size)]

	for y in range(Size):
		for x in range(Size):
			mask[y][x] = GaussFunc(x - shift, y - shift, Sigma)

	return mask


def SmoothGrey(ImagePic):
	filteredImage = ImagePic
	mask = NumPy.array( GaussMask( K, S ) )
	shift = Math.floor( K / 2 )

	for y in range( shift, ImagePic.size[ 1 ] - shift):
		for x in range( shift, ImagePic.size[ 0 ] - shift):
			partPixels = NumPy.asarray( CropImage( ImagePic, x - shift, y - shift, K, K ), "int32" )

			partPixels = mask * partPixels

			filteredImage.putpixel( (x, y), int(partPixels.sum()))

	return filteredImage

def SobelOperator(ImagePic):
	result = Image.new("L", (ImagePic.size[0], ImagePic.size[1]))
	resultAng = Image.new( "L", (ImagePic.size[ 0 ], ImagePic.size[ 1 ]) )
	for x in range(1, ImagePic.size[ 0 ] - 1):
		for y in range(1, ImagePic.size[ 1 ] - 1):
			partPixels = NumPy.asarray( CropImage( ImagePic, x - 1, y - 1, 3, 3 ), "int32" )

			horizontalPart = (partPixels * HorizontalFilterKernel).sum()
			verticalPart   = (partPixels * VerticalFilterKernel).sum()

			edgeGrad = Math.sqrt(horizontalPart ** 2 + verticalPart ** 2)

			if edgeGrad != 0:
				a = Math.atan2( verticalPart, horizontalPart )
				angle = round( a / (Math.pi / 4) ) * (Math.pi / 4) - (
							Math.pi / 2)
			else:
				angle = -1024
			#print(str(x) + " : " + str(y))

			result.putpixel( (x, y), int(edgeGrad) )
			resultAng.putpixel( (x, y), int(angle) )

	return result, resultAng


def CheckCorrectIndex(ImagePic, x, y):
	if 0 > x >= ImagePic.size[0] and 0 > y >= ImagePic.size[1]:
		return 0
	else:
		return 1

def Check(ImagePic, x, y, v):
	if not CheckCorrectIndex(ImagePic, x, y) == 0:
		return 0
	elif ImagePic.getpixel((x, y)) <= v:
		return 1
	else:
		return 0

def NonMaximumSuppression(ImagePic, ImageAng):
	result = ImagePic

	for y in range(ImagePic.size[ 1 ]):
		for x in range(ImagePic.size[ 0 ]):

			if ImageAng.getpixel((x, y)) ==  -1024:
				continue

			dx = int(Math.copysign(1, Math.cos(ImageAng.getpixel((x, y)))))
			dy = int(Math.copysign(1, Math.sin(ImageAng.getpixel((x, y)))))

			if Check(ImagePic, x + dx, y + dy, ImagePic.getpixel((x, y))) == 1:
				result.putpixel((x + dx, y + dy), 0)

			if Check(ImagePic, x - dx, y - dy, ImagePic.getpixel((x, y))) == 1:
				result.putpixel((x - dx, y - dy), 0)
			result.putpixel( (x, y),  ImagePic.getpixel((x, y)))

	return result