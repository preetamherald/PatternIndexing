
from PIL import ImageGrab, ImageOps, Image, ImageFilter
import time
from numpy import *
import numpy as np

def alignmentCorrecter(image, count):
    if count>3:
        image.show()
        return image
    width, height = image.size
    imageL = image.crop((0, 0, width/3, height/4))
    imageC = image.crop((width/3, 0, 2*width/3 , height/4))
    imageR = image.crop((2*width/3, 0, width, height/4))
    L = array(imageL.getcolors())
    C = array(imageC.getcolors())
    R = array(imageR.getcolors())
    # print(L.sum()+R.sum())
    # print(C.sum())
    if(((L.sum()+R.sum())>10000)):
        return alignmentCorrecter(image.transpose(Image.ROTATE_90),count+1)
    else:
        image.show()
        return image

def cropGrid(image):
    width, height = image.size
    image = image.crop((width/10, height/4, 9* width/10, height))
    return image

def gridValues(image):
    # print("grid")
    image = image.filter(ImageFilter.MinFilter(9))
    image.show()
    width, height = image.size
    width = width/3
    height = height/3
    result = []
    for i in range(3):
        for j in range(3):
            temp = image.crop((width*j, height*i, width*(j+1), height*(i+1)))
            result.append(gridEval(temp))
    return result

def gridEval(image):
    width, height = image.size
    temp = image.crop((3*width/8, 3*height/8, 5*width/8, 5*height/8))
    temp.show()
    a = array(temp)
    return 1 if np.average(a) > 70 else 0

test_image = "Test4.jpg"
original = Image.open(test_image)
original.show()

left = 236
top = 112
right = 385
bottom = 271
image = original.crop((left, top, right, bottom))
image = ImageOps.grayscale(image)

alignedImage = alignmentCorrecter(image,0)
grid = cropGrid(alignedImage)

grid.show()
result = gridValues(grid)

print(result)