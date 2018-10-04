from PIL import Image
import math as Math
import numpy as NumPy
import Constants

# TODO: Write docs.


def TransformToGrey(ImageArg):
	"""
			Преобразует входное изображение в изображение в оттенках серого.\n
			ImageArg argument:  PIL . Image\n
			Return value:  PIL . Image
	"""
	image = ImageArg.convert('RGB')

	resultImage = NumPy.asarray(
		[[0 for x in range(image.size[0])] for y in range(image.size[1])])

	(redLine, greenLine, blueLine) = image.split()

	redLine = NumPy.asarray(redLine)
	greenLine = NumPy.asarray(greenLine)
	blueLine = NumPy.asarray(blueLine)

	for y in range(image.size[0]):
		for x in range(image.size[1]):
			resultImage[x, y] = round(redLine[x, y] * Constants.RedLineMultiplier) + round(
				greenLine[x, y] * Constants.GreenLineMultiplier) + round(blueLine[x, y] * Constants.BlueLineMultiplier)

	return Image.fromarray(resultImage)


def CropImage(ImageArg, StartXPosition, StartYPosition, WidthOfResult, HeightOfResult):
	(width, height) = ImageArg.size

	if 0 > StartXPosition or StartXPosition > width:
		print(" -- Предупреждение! Начальная точка(ширина) должна находиться в пределах изображения.")
		print("    (начальная точка будет установлена в 0)")
		StartXPosition = 0
	elif 0 > WidthOfResult + StartXPosition > width:
		print(" -- Предупреждение! Конечная точка(ширина) должна находиться в пределах изображения.")
		print("    (конечная точка будет установлена в значение ширины изображения)")
		WidthOfResult = width

	if 0 <= StartYPosition > height:
		print(" -- Предупреждение! Начальная точка(высота) должна находиться в пределах изображения.")
		print("    (высота будет установлена в 0)")
		return
	elif 0 <= HeightOfResult + StartYPosition > height:
		print(" -- Предупреждение! Конечная точка(высота) должна находиться в пределах изображения.")
		print("    (конечная точка будет установлена в значение высоты изображения)")
		HeightOfResult = height

	sliceSizes = (StartXPosition, StartYPosition, StartXPosition +
					WidthOfResult, StartYPosition + HeightOfResult)
	return ImageArg.crop(sliceSizes)


def GaussFunc(X, Y, Sigma):
	return (1 / (2 * Math.pi * Sigma ** 2)) * Math.exp(-((X ** 2) + (Y ** 2)) / (2 * Sigma ** 2))


def GaussMask(Size, Sigma):
	shift = Math.floor(Size / 2)

	mask = [[0 for x in range(Size)] for y in range(Size)]

	for y in range(Size):
		for x in range(Size):
			mask[y][x] = GaussFunc(x - shift, y - shift, Sigma)

	return mask


def SmoothGrey(Image):
	resultImage = Image
	mask = NumPy.array(
		GaussMask(Constants.GaussMaskSize, Constants.SigmaConst))
	shift = Math.floor(Constants.GaussMaskSize / 2)

	for y in range(shift, Image.size[1] - shift):
		for x in range(shift, Image.size[0] - shift):
			imagePart = NumPy.asarray(CropImage(
				Image, x - shift, y - shift, Constants.GaussMaskSize, Constants.GaussMaskSize), "int32")

			imagePart = mask * imagePart

			resultImage.putpixel((x, y), int(imagePart.sum()))

	return resultImage


def SobelOperator(ImageArg):
	result = Image.new("L", (ImageArg.size[0], ImageArg.size[1]))
	resultAngles = Image.new("L", (ImageArg.size[0], ImageArg.size[1]))

	for x in range(1, ImageArg.size[0] - 1):
		for y in range(1, ImageArg.size[1] - 1):
			imagePart = NumPy.asarray(
				CropImage(ImageArg, x - 1, y - 1, 3, 3), "int32")

			horizontalPart = (
				imagePart * Constants.HorizontalFilterKernel).sum()
			verticalPart = (imagePart * Constants.VerticalFilterKernel).sum()

			edgeGrad = Math.sqrt(horizontalPart ** 2 + verticalPart ** 2)

			if edgeGrad != 0:
				a = Math.atan2(horizontalPart, verticalPart)
				angle = round(a / (Math.pi / 4)) * \
					(Math.pi / 4) - (Math.pi / 2)
			else:
				angle = Constants.WrongValue

			result.putpixel((x, y), int(edgeGrad))
			resultAngles.putpixel((x, y), int(angle))

	return result, resultAngles


def CheckCorrectIndex(Image, X, Y):
	if 0 < X < Image.size[0] and 0 < Y < Image.size[1]:
		return 0
	else:
		return 1


def Check(Image, X, Y, OriginPixel):
	if CheckCorrectIndex(Image, X, Y) != 0:
		return 0
	elif Image.getpixel((X, Y)) <= OriginPixel:
		return 1
	else:
		return 0


def NonMaximumSuppression(ImageArg, ImageAng):
	result = Image.new("L", (ImageArg.size[0], ImageArg.size[1]))

	for y in range(ImageArg.size[1]):
		for x in range(ImageArg.size[0]):

			if ImageAng.getpixel((x, y)) == Constants.WrongValue:
				continue

			dx = int(Math.copysign(1, Math.cos(ImageAng.getpixel((x, y)))))
			dy = int(Math.copysign(1, Math.sin(ImageAng.getpixel((x, y)))))

			if Check(ImageArg, x + dx, y + dy, ImageArg.getpixel((x, y))) == 1:
				result.putpixel((x + dx, y + dy), 0)

			if Check(ImageArg, x - dx, y - dy, ImageArg.getpixel((x, y))) == 1:
				result.putpixel((x - dx, y - dy), 0)
			result.putpixel((x, y), ImageArg.getpixel((x, y)))

	return result


def DoubleThresholding(ImageArg, LowerBound, HigherBound):
	lowBound = LowerBound * Constants.MaxColorValue
	highBound = HigherBound * Constants.MaxColorValue

	resultImage = Image.new("L", (ImageArg.size[0], ImageArg.size[1]))

	for y in range(ImageArg.size[1]):
		for x in range(ImageArg.size[0]):
			if ImageArg.getpixel((x, y)) >= highBound:
				resultImage.putpixel((x, y), Constants.MaxColorValue)
			elif ImageArg.getpixel((x, y)) <= lowBound:
				resultImage.putpixel((x, y), Constants.MinColorValue)
			else:
				resultImage.putpixel((x, y), Constants.MidColorValue)

	return resultImage
