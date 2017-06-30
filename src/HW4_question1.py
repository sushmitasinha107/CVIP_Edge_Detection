import cv2
import scipy.signal
import math
import numpy as np


    
def applyfilterLoG(A, B):
    A = cv2.copyMakeBorder(np.asarray(A), 2, 2, 2, 2, cv2.BORDER_REFLECT)
    wk, hk = np.asarray(A).shape
    
    LoG = [[0.0 for x in range(hk-2)] for y in range(wk-2)] 
    gi = 0
    gj = 0
    for i in range(2, wk-2):
        gj = 0
        for j in range(2, hk-2):
            LoG[gi][gj] = ((A[i-2][j-2] * B[0][0]) + (A[i-2][j-1] * B[0][1]) + (A[i-2][j] * B[0][2]) + (A[i-2][j+1] * B[0][3]) + (A[i-2][j-2] * B[0][4]) + 
                          (A[i-1][j-2] * B[1][0]) + (A[i-1][j-1] * B[1][1]) + (A[i-1][j] * B[1][2]) + (A[i-1][j+1] * B[1][3]) + (A[i-1][j+2] * B[1][4]) + 
                          (A[i][j-2] * B[2][0]) + (A[i][j-1] * B[2][1]) + (A[i][j] * B[2][2]) + (A[i][j+1] * B[2][3]) + (A[i][j+2] * B[2][4]) + 
                          (A[i+1][j-2] * B[3][0]) + (A[i+1][j-1] * B[3][1]) + (A[i+1][j] * B[3][2]) + (A[i+1][j+1] * B[3][3]) + (A[i+1][j+2] * B[3][4])  +
                          (A[i+2][j-2] * B[4][0]) + (A[i+2][j-1] * B[4][1]) + (A[i+2][j] * B[4][2]) + (A[i+2][j+1] * B[4][3]) + (A[i+2][j+2] * B[4][4] ))
            gj += 1
        gi += 1 
    return LoG
    

def applyEdgeDetection(LoG):
    LoG = cv2.copyMakeBorder(np.asarray(LoG), 1, 1, 1, 1, cv2.BORDER_REFLECT)
    
    wk, hk = np.asarray(LoG).shape
    Edge = [[0.0 for x in range(hk-1)] for y in range(wk-1)] 
    gi = 0
    gj = 0
    for i in range(1, wk-1):
        gj = 0
        for j in range(1, hk-1):
            if ((LoG[i][j+1] > 0 and LoG[i][j] < 0) or (LoG[i][j+1] < 0 and LoG[i][j] > 0)
            or (LoG[i+1][j] > 0 and LoG[i][j] < 0) or (LoG[i+1][j] < 0 and LoG[i][j] > 0)):
 
                Edge[gi][gj] = LoG[i][j]  
               
                gj += 1
            else:
                Edge[gi][gj] = 0
                gj += 1
        gi += 1 
    return Edge
    
 
def applyfilterSobelMean(sobelx,sobely):
    
    
    wk, hk = np.asarray(sobelx).shape
    SobelMean = [[0.0 for x in range(hk)] for y in range(wk)] 
    gi = 0
    gj = 0
    for i in range(0, wk):
        gj = 0
        for j in range(0, hk):
                SobelMean[gi][gj] = math.sqrt(sobelx[i][j]*sobelx[i][j]+sobely[i][j]*sobely[i][j])
                gj += 1
        gi += 1 
    return SobelMean
    
def applyStrongEdge(LoGEgde,SobelMean):
    wk, hk = np.asarray(SobelMean).shape
    StrongEdge = [[0.0 for x in range(hk)] for y in range(wk)] 
    gi = 0
    gj = 0
    for i in range(0, wk):
        gj = 0
        for j in range(0, hk):
            if SobelMean[i][j]>180:
                StrongEdge[gi][gj] = SobelMean[i][j] + LoGEgde[i][j]
            else:   
                StrongEdge[gi][gj] = 0.0
            gj += 1
        gi += 1 
    return StrongEdge                     
          
img = cv2.imread('/Users/sushmitasinha/Downloads/UBCampus.jpg')
greyImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
greyImage = greyImage.astype(float)
cv2.imshow('Original', np.uint8(greyImage))

sobelx = cv2.Sobel(greyImage,cv2.CV_64F,1,0,ksize=3)  # x
sobely = cv2.Sobel(greyImage,cv2.CV_64F,0,1,ksize=3)  # y
cv2.imshow('sobelx', np.uint8(sobelx))
cv2.imshow('sobely', np.uint8(sobely))
SobelMean = applyfilterSobelMean(sobelx,sobely)
cv2.imshow('SobelMean', np.uint8(SobelMean))


filter = [[1.0/16, 1.0/8, 1.0/16], [1.0/8, 1.0/4, 1.0/8], [1.0/16, 1.0/8, 1.0/16]]
greyImage = scipy.signal.convolve2d(greyImage, np.array(filter))

#gaussian- for smoothenning

LoGMask = [[0.0,0.0,1.0,0.0,0.0],[0.0,1.0,2.0,1.0,0.0],[1.0,2.0,-16.0,2.0,1.0],[0.0,1.0,2.0,1.0,0.0],[0.0,0.0,1.0,0.0,0.0]]
LoG = scipy.signal.convolve2d(greyImage, np.array(LoGMask))
cv2.imshow('LoGMask', LoG) 

LoGEgde = applyEdgeDetection(LoG)
cv2.imshow('LoGEgde', np.uint8(LoGEgde))
StrongEdge = applyStrongEdge(LoGEgde,SobelMean)
cv2.imshow('StrongEdgeLog', np.uint8(StrongEdge))

DoGMask = [[0.0,0.0,-1.0,-1.0,-1.0,0.0,0.0], [0.0,-2.0,-3.0,-3.0,-3.0,-2.0,0.0], [-1.0,-3.0,5.0,5.0,5.0,-3.0,-1.0], [-1.0,-3.0,5.0,16.0,5.0,-3.0,-1.0], [-1.0,-3.0,5.0,5.0,5.0,-3.0,-1.0], [0.0,-2.0,-3.0,-3.0,-3.0,-2.0,0.0], [0.0,0.0,-1.0,-1.0,-1.0,0.0,0.0]]
DoG = scipy.signal.convolve2d(greyImage, np.array(DoGMask))
cv2.imshow('DoGMask', DoG)

cv2.imshow('DoGmasknp', np.uint8(DoG))
DoGEdge = applyEdgeDetection(DoG)
cv2.imshow('DoGEgde', np.uint8(DoGEdge))
StrongEdge = applyStrongEdge(DoGEdge,SobelMean)
cv2.imshow('StrongEdgeDog', np.uint8(StrongEdge))
