from ast import Raise
from itertools import count
import itertools
from logging import raiseExceptions
from lucaskanadev1 import *
from array_generator_cardio import *
import SimpleITK as sitk
import numpy as np
import cv2 as cv
from scipy.signal import convolve2d
import sys

def laplacian(arr):
    laplace = cv.Laplacian(arr, cv.CV_64F, ksize=3)
    return laplace


def sobel_filter(arr):
    #Sobel
    image = sitk.GetImageFromArray(arr)
    sobelFilter = sitk.SobelEdgeDetectionImageFilter()
    float_image =  sitk.Cast(image, sitk.sitkFloat32)
    sobelEdge = sitk.SobelEdgeDetection(float_image)

    sobel = sitk.GetArrayFromImage(sobelEdge)
    return sobel


def edge_sharp(arr):
    
    ker1 = np.array([[-1, -1, -1], 
                     [-1, 9, -1], 
                     [-1, -1, -1]])
    
    '''ker2 = np.array([[0, 1, 2], 
                     [-1, 0, 1], 
                     [-2, -1, 0]])
    
    ker3 = np.array([[0, -1, -2], 
                     [1, 0, -1], 
                     [2, 1, 0]]) '''  
    
    sharp = convolve2d(arr, ker1, mode='same')
    #t1 = convolve2d(sharp, ker2, mode='same')
    #t2 = convolve2d(sharp, ker3, mode='same')
    #t1 = t1.astype('float64')
    #t2 = t2.astype('float64')
    #sob = (np.sqrt(np.square(t1), np.square(t2)))
    
    
    
    return sharp
    #print(np.shape(ker1))
    

def normalize_image(arr):
    img = sitk.GetImageFromArray(arr)
    #img = sitk.Cast(img, sitk.sitkFloat32)
    n = sitk.NormalizeImageFilter()
    normalize = n.Execute(img)
    normalize = sitk.GetArrayFromImage(normalize)
    return normalize


def gaussian_blur(arr, sigmaX, sigmaY):
    blur = cv.GaussianBlur(arr, (3, 3),
                           sigmaX=sigmaX, sigmaY=sigmaY)
    return blur


def sitk_threshold(arr, lower, upper, outside, inside):
    img = sitk.GetImageFromArray(arr)
    binT = sitk.BinaryThresholdImageFilter()
    binT.SetLowerThreshold(lower)
    binT.SetUpperThreshold(upper)
    binT.SetOutsideValue(outside)
    binT.SetInsideValue(inside)
    binImg = binT.Execute(img)
    return binImg


def binary_contour(arr):
    img = sitk.GetImageFromArray(arr)
    contour = sitk.BinaryContourImageFilter()
    contour.FullyConnectedOn()
    contour.SetBackgroundValue(0)
    contour.SetForegroundValue(255)
    contImg = contour.Execute(img)
    return contImg


def denoise_binary(arr):
    img = sitk.GetImageFromArray(arr)
    img = sitk.Cast(img, sitk.sitkFloat32)
    denoise = sitk.BinaryMinMaxCurvatureFlowImageFilter()
    denoise.SetThreshold(1)
    denoise.SetStencilRadius(10)
    denoise.SetNumberOfIterations(100)
    denoised = denoise.Execute(img)
    return denoised


def canny_detector(arr, lower, upper, variance, error):
    img = sitk.GetImageFromArray(arr)
    img = sitk.Cast(img, sitk.sitkFloat32)
    canny = sitk.CannyEdgeDetectionImageFilter()
    
    canny.SetUpperThreshold(upper)
    canny.SetLowerThreshold(lower)
    
    #canny.SetVariance(variance)
    
    #canny.SetMaximumError(error)
    
    cannyArr = canny.Execute(img)
    cannyArr = sitk.GetArrayFromImage(cannyArr)
    
    return cannyArr


def gradients_IxIy(arr, size):
    #3x3
    #Ix
    ker1 = np.array([[0, 0, 0],
                     [0, -1, 1],
                     [0, 0, 0]])
    #Iy    
    ker2 = np.array([[0, 0, 0],
                     [0, -1, 0],
                     [0, 1, 0]])
    #5x5
    #Ix
    ker3 = np.array([[0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, -1, 1, 1],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0]])
    #Iy
    ker4 = np.array([[0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, -1, 0, 0],
                     [0, 0, 1, 0, 0],
                     [0, 0, 1, 0, 0]])
    
    if size == 3:
        Ix = convolve2d(arr, ker1, mode='same')
        Iy = convolve2d(arr, ker2, mode='same')
    if size == 5:
        Ix = convolve2d(arr, ker3, mode='same')
        Iy = convolve2d(arr, ker4, mode='same')       
    
    return Ix, Iy


def gradient_It(arr1, arr2):
    
    It = np.subtract(arr2, arr1)
    
    return It


def lucas_kanade(arr1, arr2):
    
    #Grab two equally sized arrays
    shape1, shape2 = np.shape(arr1), np.shape(arr2)
    if (shape1 != shape2):
        raise Exception('Arrs should be same size.')
    else:
        #Compute Ix, Iy, It gradients
        Ix1 = gradients_IxIy(arr1)
        Iy1 = gradients_IxIy(arr2)
        It = gradient_It(arr1, arr2)
        
        for i in range(shape1[0]):
            for j in range(shape1[1]):
                
                
                pass
        pass
    
    
    
    return


#Generamos una lista de pixel arrays y una lista de los objetos de cada img
tensors, objList = array_generator_cardio()

#Cropper
totalOfImages = int(len(objList))
middleImage = int(totalOfImages/2)
referenceImage = ((objList[middleImage]).img)
print(type(referenceImage))

#img = myshow(sitk.GetImageFromArray(referenceImage), cmap=plt.cm.bone)
referenceImage2 = referenceImage.astype(np.int8)
#referenceImage2 = cv.applyColorMap(referenceImage2, colormap=cv.COLORMAP_BONE)

roi = cv.selectROI("Seleccione el ROI a analizar", referenceImage2)
#referenceImage2 = referenceImage.astype(np.int8)
#roi = cv.selectROI('prueba color', referenceImage2)

print('Chosen ROI', roi)
cv.destroyAllWindows()

x1, y1, x2, y2 = int(roi[0]), int(roi[1]), int(roi[2]), int(roi[3])

newList = []


class Manipulator(Study):
    def __init__(self, slice, img, cardPhase, path, Ix, Iy, It, cropped):
        super().__init__(slice, img, cardPhase, path)
        self.cropped = cropped
        self.Ix = Ix
        self.Iy = Iy
        self.It = It
    
    def cropper(x1, x2, y1, y2):
        cropped = arr[y1:int(y1 + y2), x1:int(x1 + x2)]
        
        return cropped
     
    def gradients_IxIy(arr, size):
    #3x3
    #Ix
        ker1 = np.array([[0, 0, 0],
                        [0, -1, 1],
                        [0, 0, 0]])
        #Iy    
        ker2 = np.array([[0, 0, 0],
                        [0, -1, 0],
                        [0, 1, 0]])
        #5x5
        #Ix
        ker3 = np.array([[0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, -1, 1, 1],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0]])
        #Iy
        ker4 = np.array([[0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, -1, 0, 0],
                        [0, 0, 1, 0, 0],
                        [0, 0, 1, 0, 0]])
        
        if size == 3:
            Ix = convolve2d(arr, ker1, mode='same')
            Iy = convolve2d(arr, ker2, mode='same')
        if size == 5:
            Ix = convolve2d(arr, ker3, mode='same')
            Iy = convolve2d(arr, ker4, mode='same')       
    
        return Ix, Iy


for n in objList:
    arr = n.img
    newArr = arr[y1:int(y1 + y2), x1:int(x1 + x2)]
    
    norm = normalize_image(newArr)
    blur = gaussian_blur(norm, 3, 3)
    sobel = sobel_filter(blur)
    sharp = edge_sharp(norm)
    
    Ix, Iy = gradients_IxIy(norm, 3)
    
    thresh = sitk_threshold(blur, lower=-0.6, upper=0.6, outside=0, inside=255)
    thresh = sitk.GetArrayFromImage(thresh)
    
    
    contour = binary_contour(thresh)
    contour = sitk.GetArrayFromImage(contour)
    
    multiplied = np.multiply(sobel, contour)
    
    canny = canny_detector(arr=blur, lower=-1, upper=0, variance=0, error=0)

    
    setattr(n, 'crop', newArr)
    setattr(n, 'sobel', sobel)
    setattr(n, 'thresh', thresh)
    setattr(n, 'sharp', sharp)
    setattr(n, 'contour', contour)
    setattr(n, 'multiplied', multiplied)
    setattr(n, 'canny', canny)
    setattr(n, 'norm', norm)
    setattr(n, 'Ix', Ix)
    setattr(n, 'Iy', Iy)

    newList.append(n)
    #print(np.shape(arr), np.shape(newArr))
    #img = myshow(sitk.GetImageFromArray(newArr), cmap=plt.cm.bone)    
n = 0
lkList = []
iterlist = list(itertools.pairwise(objList))
#print(iterlist)


class lk(Study):
    def __init__(self, slice, img, cardPhase, path):
        super().__init__(slice, img, cardPhase, path)
        


for n in iterlist:
    obj1 = n[0]
    obj2 = n[1]
    It = gradient_It(obj1, obj2)
    
    
    
    pass


#Un atributo de cada objeto es el numero de phase cardiacas (esto te reeordena los objetitos)
cardPhase = int((newList[0]).cardPhase)
totalCardiacCycles = int(totalOfImages/cardPhase)
print('Cantidad de img = ', totalOfImages)
print("Cantidad de fases cardiacas = ", totalCardiacCycles)

splitedList = np.array_split(newList, totalCardiacCycles)

print(np.shape(tensors))

def plot():
    n=1
    for i in splitedList[7]:
        
        print(n)
        n+=1
        
        originalArr = i.crop
        sobelArr = i.sobel
        threshArr = i.thresh
        sharpArr = i.sharp
        substractedArr = np.subtract(originalArr, sobelArr)
        contourArr = i.contour
        multipliedArr = i.multiplied
        cannyArr = i.canny
        #sobel2Arr = np.multiply(10000000, sobel2Arr)
        normArr = i.norm
        
        IxArr = i.Ix
        IyArr = i.Iy
        
        originalImg = sitk.GetImageFromArray(originalArr)
        sobelImg = sitk.GetImageFromArray(sobelArr)
        substractedImg = sitk.GetImageFromArray(substractedArr)
        threshImg = sitk.GetImageFromArray(threshArr)
        sharpImg = sitk.GetImageFromArray(sharpArr)
        multipliedImg = sitk.GetImageFromArray(multipliedArr)
        cannyImg = sitk.GetImageFromArray(cannyArr)
        normImg = sitk.GetImageFromArray(normArr)
        contourImg = sitk.GetImageFromArray(contourArr)
        
        Ix = sitk.GetImageFromArray(IxArr)
        Iy = sitk.GetImageFromArray(IyArr)
        
        myshow(originalImg, cmap=plt.cm.bone)
        #myshow(sobelImg, cmap=plt.cm.bone)
        #myshow(substractedImg, cmap=plt.cm.bone)
        #myshow(multipliedImg, cmap=plt.cm.bone)
        myshow(threshImg, cmap=plt.cm.bone)
        myshow(contourImg, cmap=plt.cm.bone)
        #myshow(cannyImg, cmap=plt.cm.bone)
        myshow(Ix, cmap=plt.cm.bone)
        myshow(Iy, cmap=plt.cm.bone)

#plot()  








