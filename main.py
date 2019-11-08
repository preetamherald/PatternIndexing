from PIL import ImageGrab, ImageOps, Image, ImageFilter
import time
from numpy import *
import cv2

def alignmentCorrecter(image, count):
    # image = image.transpose(Image.ROTATE_90)
    # image = image.transpose(Image.ROTATE_90)
    # return image
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
    print(L.sum()+R.sum())
    print(C.sum())
    if(((L.sum()+R.sum())>9000)):
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
    # temp.show()
    a = array(temp)
    return 1 if average(a) > 70 else 0

def read_N_crop(img):
    blurred = cv2.blur(img, (3,3))
    canny = cv2.Canny(blurred, 50, 200)

    ## find the non-zero min-max coords of canny
    pts = argwhere(canny>0)
    y1,x1 = pts.min(axis=0)
    y2,x2 = pts.max(axis=0)

    ## crop the region
    cropped = img[y1:y2, x1:x2]
    cv2.imwrite("cropped.png", cropped)

def main():
    test_image = "Test1 (1).jpg"
    img = cv2.imread(test_image)
    read_N_crop(img)
    original = Image.open("cropped.png")
    original.show()
    image = ImageOps.grayscale(original)

    image.show()

    alignedImage = alignmentCorrecter(image,0)
    grid = cropGrid(alignedImage)

    grid.show()
    result = gridValues(grid)

    print(result)

if __name__ == "__main__":
    main()
else:
    pass #TODO