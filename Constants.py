FilePath = "C:/Users/valer/Desktop/valve.png"

SliceSize = 100

SigmaConst = 0.35
GaussMaskSize = 5

LowerBound = 0.599
HigherBound = 0.6

RedLineMultiplier = 0.3
GreenLineMultiplier = 0.6
BlueLineMultiplier = 0.1

WrongValue = -255

MaxColorValue = 255
MidColorValue = 127
MinColorValue = 0

HorizontalFilterKernel = [	[1, 0, -1],
							[2, 0, -2],
							[1, 0, -1]
]

VerticalFilterKernel = [	[1,  2,  1],
							[0,  0,  0],
							[-1, -2, -1]
]

LineDirection = [	[-1, -1, -1,  0, 0,  1, 1, 1],
					[-1,  0,  1, -1, 1, -1, 0, 1]
]
