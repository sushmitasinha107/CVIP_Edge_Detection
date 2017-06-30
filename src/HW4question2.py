import cv2
import numpy as np

def reduceimage(colorregion,greyImage):
    w, h = np.asarray(colorregion).shape
    G = [[0.0 for x in range(h*2)] for y in range(w*2)] 
    di = 0
    dj = 0
    for i in range (0, w,2):
        dj = 0
        for j in range (0, h,2):
                G[di][dj] = colorregion[i][j] 
                dj += 1
        di += 1
    return G 

def colorregion(regiont3,removet1,regionaverage):
    w, h = np.asarray(regiont3).shape
    for regioncolor in range(0, len(regionaverage),2):
        for i in range(0, w-2,2):
            for j in range(0, h-2, 2): 
                if regiont3[i][j] == regionaverage[regioncolor]: 
                    removet1[i][j]= regionaverage[regioncolor+1]                          
    return removet1

def calculateregionaverage(regiont3,removet1):
    w, h = np.asarray(regiont3).shape
    average = []
    Unique = np.unique(regiont3)
    for region in range(3, Unique.size):
        average.append(Unique[region])
        sum = 0
        count = 0 
        for i in range(0, w,2):
            for j in range(0, h, 2): 
                if regiont3[i][j] == Unique[region]: 
                    sum=sum+removet1[i][j]
                    count=count+1 
                         
        average.append(sum/count)                  
    return average
        


def Removet3(regiont2,W2,t3):
    wi, h = np.asarray(regiont1).shape
    regiont3 = [["" for x in range(h)] for y in range(wi)]
    regiont3=regiont2
    for w in range(0, len(W),3):
        r1 = W[w]
        r2 = W[w+1]
        r1r2w = W[w+2]
        if(r1r2w) >= t3:
            for i in range(0, wi-2,2):
                for j in range(0, h-2, 2): 
                    if(regiont2[i][j] == r2):
                        regiont3[i][j] == r1
    return regiont3
                                    
          
def Removet2(removet1,regiont1,W,perimeter,t2):
    wi, h = np.asarray(regiont1).shape
    regiont2 = [["" for x in range(h)] for y in range(wi)]
    regiont2=regiont1;
    for w in range(0, len(W),3):
        r1 = W[w]
        r2 = W[w+1]
        r1r2w = W[w+2]
        for p in range(0, len(perimeter), 2):
            if perimeter[p] == r1:
                l1 = perimeter[p+1] 
            if perimeter[p] == r2:
                l2 = perimeter[p+1] 
        if(l1 < l2): min=l1
        else: min = l2
        
        if(r1r2w/min) >= t2:
           
            for i in range(0, wi,2):
                for j in range(0, h,2):
                   
                    if(regiont1[i][j] == r2):
                        regiont2[i][j] == r1
    return regiont2
                                              

def checkNeighbour(R,element,posx,posy):
 #R = cv2.copyMakeBorder(np.asarray(R), 2, 2, 2, 2, cv2.BORDER_REFLECT)
 #constant= cv2.copyMakeBorder(img1,10,10,10,10,cv2.BORDER_CONSTANT,value=BLUE)
 sumequalregion = 0
 if R[posx+2][posy] == element:
    sumequalregion = sumequalregion + 1
 if R[posx][posy+2] == element:
    sumequalregion = sumequalregion + 1
 if R[posx][posy-2] == element:
    sumequalregion = sumequalregion + 1
 if R[posx-2][posy] == element:
    sumequalregion = sumequalregion + 1
 if(sumequalregion>2) :
    return 0
 else:
     return 1  
    
def makeperimeter(removet1,R):
    w, h = np.asarray(removet1).shape
   # print(w,h)
    perimeter = []
    Unique = np.unique(R)
    #print Unique          
    for region in range(3, Unique.size): 
        perimeter.append(Unique[region])
        peri = 1 
        for i in range(0, w-2,2):
            for j in range(0, h-2, 2): 
                if R[i][j] == Unique[region]: 
                    peri=peri+checkNeighbour(R,Unique[region],i,j)
        perimeter.append(peri)                  
    return perimeter
        
  
def countW(removet1,R):
    w, h = np.asarray(removet1).shape
    #print(w,h)
    G = [["" for x in range(h)] for y in range(w)]
    W = []
    Unique = np.unique(R)
    for region1 in range(3, Unique.size):
      for region2 in range(4, Unique.size):
        
        if(Unique[region1] != Unique[region2]): 
            W.append(Unique[region1]) 
            W.append(Unique[region2])
            weak = 0
            for i in range(0, w-2,2):
                for j in range(0, h-2, 2): 
                    if (R[i][j] == Unique[region1] and  R[i][j+2] == Unique[region2]) and  R[i][j+1] == 0:  
                        weak = weak+1 
                    if (R[i][j] == Unique[region1] and  R[i+2][j] == Unique[region2]) and  R[i+1][j] == 0 :  
                        weak = weak+1 
                                 
            W.append(weak)                  
    return W
      
def makeregiont1(doublematrix):
    w, h = np.asarray(doublematrix).shape
    #print(w,h)
    G = [["" for x in range(h)] for y in range(w)] 
    r=0
    for i in range(0, w-2,2):
        for j in range(0, h-2, 2):    
            if doublematrix[i][j+1] == 0 :  
                G[i][j+1] = 0 
               # G[gi][gj+1] = (doublematrix[i][j] + doublematrix[i][j+2])/2 
               #G[gi][gj] = G[gi][gj+2]=(doublematrix[i][j] + doublematrix[i][j+2])/2 
                if(G[i][j] == ""):
                    G[i][j] = "R["+str(i)+"]["+ str(j)+"]"
                if(G[i][j+2] == ""):   
                    G[i][j+2] =  G[i][j] 
            else:
                 G[i][j+1] = 1 
                 if(G[i][j] == ""): 
                    G[i][j] = "R["+str(i)+"]["+ str(j)+"]"
                 if(G[i][j+2] == ""): 
                    G[i][j+2] = "R["+str(i)+"]["+ str(j+2)+"]" 
            
            if doublematrix[i+1][j] == 0 :  
                G[i+1][j] = 0
               # G[gi][gj+1] = (doublematrix[i][j] + doublematrix[i][j+2])/2 
               #G[gi][gj] = G[gi][gj+2]=(doublematrix[i][j] + doublematrix[i][j+2])/2 
                if(G[i][j] == ""):
                    G[i][j] = "R["+str(i)+"]["+ str(j)+"]"
                if(G[i+2][j] == ""):   
                    G[i+2][j] = G[i][j]
            else:
                 G[i+1][j] = 1
                 if(G[i][j] == ""): 
                    G[i][j] = "R["+str(i)+"]["+ str(j)+"]"
                 if(G[i+2][j] == ""): 
                    G[i+2][j] = "R["+str(i+2)+"]["+ str(j)+"]"
 
    return G 
     
def markweakedge(doublematrix,t1):
    w, h = np.asarray(doublematrix).shape
    G = [[0 for x in range(h)] for y in range(w)] 
    
    G = doublematrix
    for i in range(0, w,2):
        for j in range(0, h, 2):
            if doublematrix[i][j+1] <= t1: 
                G[i][j+1] = 0
            else:  
                G[i][j+1] = 255
            if doublematrix[i+1][j] <= t1 :   
                G[i+1][j] = 0
            else: 
                G[i+1][j] = 255
        
        
    return G      
    
def doublematrix(Matrix):
    w, h = np.asarray(Matrix).shape
    G = [[0.0 for x in range(h*2)] for y in range(w*2)] 
    di = 0
    dj = 0
    for i in range (0, w-1):
        dj = 0
        for j in range (0, h-1):
            G[di][dj] = Matrix[i][j]
            if Matrix[i][j] > Matrix[i+1][j]:
                G[di+1][dj] = abs(Matrix[i][j] - Matrix[i][j+1])
            else:
                G[di+1][dj] = abs(Matrix[i][j+1] - Matrix[i][j])
            if Matrix[i][j] > Matrix[i][j+1]:
                G[di][dj+1] = abs(Matrix[i][j] - Matrix[i][j+1])
            else:
                G[di][dj+1] = abs(Matrix[i][j+1] - Matrix[i][j])     
            dj += 2
        di += 2
    return G 
           
img = cv2.imread('/Users/sushmitasinha/Downloads/MixedVegetables.jpg')
greyImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
greyImage = greyImage.astype(float)
w,h = greyImage.shape
cv2.imshow('Original', np.uint8(greyImage))
doublematrix = doublematrix(greyImage)
#print(doublematrix)
cv2.imshow('doublematrix', np.uint8(doublematrix))
t1 = 15
removet1 = markweakedge(doublematrix,t1)
cv2.imshow('removet1', np.uint8(removet1))
#print(removet1)
regiont1 = makeregiont1(removet1)
#print(regiont1)

regionaveraget1 =  calculateregionaverage(regiont1,removet1)
#print(regionaveraget1)
colorregiont1 =  colorregion(regiont1,removet1,regionaveraget1)
cv2.imshow('colorregiont1', np.uint8(colorregiont1))


perimeter = makeperimeter(removet1,regiont1)
print("----------------------------perimeter------------------")
#print(perimeter)
W = countW(removet1,regiont1)
print("----------------------------W------------------")
#print(W)
t2=0.5
regiont2 = Removet2(removet1,regiont1,W,perimeter,t2)
print("----------------------------regiont2------------------")
#print(regiont2)
regionaveraget2 =  calculateregionaverage(regiont2,removet1)
#print(regionaveraget1)
colorregiont2 =  colorregion(regiont2,removet1,regionaveraget2)
cv2.imshow('colorregiont2', np.uint8(colorregiont2))
print("----------------------------W2------------------")
W2 = countW(removet1,regiont2)
#print(W2)
t3=20
print("----------------------------regiont3------------------")
regiont3 = Removet3(regiont2,W2,t3)

#print(regiont3)

regionaverage =  calculateregionaverage(regiont3,removet1)
#print(regionaverage)

colorregion =  colorregion(regiont3,removet1,regionaverage)
#print(colorregion)
cv2.imshow('colorregion', np.uint8(colorregion))

final =  reduceimage(colorregion,greyImage)
cv2.imshow('final', np.uint8(final))

