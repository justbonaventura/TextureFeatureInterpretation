#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import mahotas
from mahotas import features
import matplotlib.pyplot as plt
from skimage.feature import graycomatrix
from PIL import Image, ImageDraw
import matplotlib.animation as animation
import matplotlib.colors as mcolors
import os
import random
from skimage import io


# In[5]:

#Color map skewed toward brightness for easier visualization of GLCMs with low values-
image = Image.open(r"C:\Users\justinamb\Desktop\TextureCode\Images\greymap3.png")
cmapdata = np.asarray(image)
cmapdata=np.fliplr(cmapdata)
newmap=cmapdata[15,:,:]/256
mymap2 = mcolors.ListedColormap(newmap)


#Function which plots image and GLCM, extracts and returns features and GLCM-
def showtexture(tester_array, nolevels=256, igzeros=False, show=True, normalized=False):
    
    if normalized==True:
    #To work with normalized array-
        normalizedarray = tester_array.astype(np.float64)/np.nanmax(tester_array)
        normalizedarray = normalizedarray*(nolevels-1)
        normalizedarray = normalizedarray.astype(np.uint8)
    
    if normalized == False:
    #Non-normalized array-
        normalizedarray = tester_array.astype(np.uint8)
    
    glcm = graycomatrix(
        normalizedarray, distances=[1], angles=[0], levels=nolevels, symmetric=False, normed=True
        )


    features=mahotas.features.haralick(normalizedarray, preserve_haralick_bug=False, use_x_minus_y_variance=True, compute_14th_feature=True)

    if igzeros:
        glcm[0,0]=0
    
    if show:
        fig, (ax1, ax2) = plt.subplots(1, 2)
        plt.rcParams["font.family"] = "serif"
        plt.rcParams["font.serif"] = "Times New Roman"
        f=ax1.imshow(normalizedarray, vmin=0, vmax=nolevels, cmap='gray')
        ax1.set_yticklabels([])
        ax1.set_xticklabels([])
        ax1.set_xticks([])
        ax1.set_yticks([])
        ax1.set_title("Input Image")
        plt.colorbar(f, ax=ax1, shrink=0.3)
        paddedglcm=np.zeros((nolevels+8,nolevels+8))
        paddedglcm[4:nolevels+4,4:nolevels+4]=glcm[:,:,0,0]
        g=ax2.imshow(paddedglcm, cmap=mymap2) 
        ax2.set_title("GLCM")
        plt.colorbar(g, ax=ax2, shrink=0.3)
        plt.tight_layout()
        plt.show()
        

    return(features,glcm)


# In[4]:


#Ordering the images based on feature value-
def sortSecond(val):
    return val[1] 


def orderims(Featarray):
    indecies=np.arange(len(Featarray)).reshape(len(Featarray),1)
    orderedfeats=[]
    for i in range(14):
        feats=Featarray[:,i].reshape(len(Featarray),1)
        featsandindicies=np.concatenate((indecies,feats),axis=1)
        orderedvals=list(featsandindicies)
        orderedvals.sort(key=sortSecond)
        orderedfeat=np.array(orderedvals)
        orderedfeats.append(orderedfeat)
        plt.plot(orderedfeat[:,1])
        plt.title("Feature " +str(i+1))
        plt.xlabel("Image Number")
        plt.ylabel("Feature Value")
        plt.show()
    return(orderedfeats)


# In[ ]:


#A function which takes as linear of a sampling of the images across the feature range as possible and plots them in various ways-
def linearsampling(dataset, ln, iset, mode="sim", indlist=[], imsize=100):
    vals=dataset[:,1]
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_size_inches(10, 3)
    xval0=np.arange(len(vals))
    ax1.scatter(xval0,vals,s=0.1)
    ax1.set_title("Original Value Distribution")
    ax1.set_xlabel("Image Number")
    ax1.set_ylabel("Feature Value")
    #To adjust linear stringency of slope ln value is added below-
    linearslope=(np.max(vals)-np.min(vals))/(len(vals)*ln)
    index=0
    val1=vals[0]
    linearlist=[dataset[0]]
    pointlist=[]
    while index<(len(vals)-1):
    #testing for linearity-
        index=index+1
        nextval=linearslope+val1
        val2=vals[index]
        while nextval>val2:
            index=index+1
            #Handling for the end value-
            if index<(len(vals)-1):
                val2=vals[index]
            else:
                index=(len(vals)-1)
                break
        linearlist.append(dataset[index])
        pointlist.append([index,dataset[index][1]])
        val1=val2
    lineararray=np.array(linearlist)
    pointarray=np.array(pointlist)
    print("Number of iamges in linear sampling- ", len(lineararray))
    xval=np.arange(len(lineararray))
    ax2.scatter(xval,lineararray[:,1], c="red", s=3)
    ax2.set_title("Linear Value Distribution")
    ax2.set_xlabel("raked value")
    plt.show()
    
    #A slice of each image in the linear sampling is taken and added to an array- 
    showlist=[]
    subshowlist=[]
    rangearray=np.zeros((imsize,len(linearlist)*20))
    #Simultaneously images are added to a list to show a sampling of images and GLCM's across the range-
    
    jumpsize=int(np.ceil(lineararray.shape[0]/5))
    #Adding a little handling for edge cases-
    if (lineararray.shape[0]-1)%jumpsize==0:
        jumpsize=int(np.ceil(lineararray.shape[0]/6))
    jump=0
    
    
    #Selecting out min max and central values to be plotted as well-
    linlength= len(lineararray)-1
    halflinlength=int(linlength/2)
    
    for j in range(lineararray.shape[0]):
        index=int(lineararray[j,0])
        if mode=="sim":
            chunk=iset[index][:imsize,:imsize]
       #For modes where index is encoded to crop image as well-
        else:
            chunkloco=indlist[index]
            a,b,c=chunkloco
            imup=iset[a]
            if len(imup.shape)>2:
                imup=imup[:,:,0]
            imup=imup-np.min(imup)
            imup=imup/np.max(imup)*255
            chunk=imup[b*imsize:(b+1)*imsize,c*imsize:(c+1)*imsize]
        glcm=showtexture(chunk, show=False)[1]
        if j==(jump*jumpsize) or j==lineararray.shape[0]-1:
            showlist.append([chunk,glcm])
            jump=jump+1
        if j==0 or j==halflinlength or j==linlength:
            subshowlist.append([chunk,glcm])
        colmax=np.argmax(np.mean(chunk,axis=0))
        if colmax<10:
            colmax=11
        if colmax>imsize-10:
            colmax=imsize-11
        rangearray[:,j*20:(j+1)*20]=chunk[:,colmax-10:colmax+10]
        
     
    rangelen=len(lineararray)*0.3
    fig, ax = plt.subplots(figsize=(rangelen, 2))
    ax.imshow(rangearray)
    ax.set_title("Image Slices Across Feature Range")
    ax.set_yticklabels([])
    ax.set_xticklabels(["Min. Feat Image","Max. Feat. Image"])
    ax.set_xticks([0,len(lineararray)*20])
    ax.set_yticks([])
    plt.show()
    

    #Plot six approximately spaced out images (Down then right for increasing feat. value)-
    
    #Shows resulting matricies
    plt.figure(figsize=(20,4), dpi=2000)
    fig, axs = plt.subplots(2,6)
    fig.set_size_inches(16, 6)
    l=0
    m=0
    for k in range(len(showlist)):
        [chunk, glcm]=showlist[k]
        
        paddedglcm=np.zeros((glcm.shape[0]+8,glcm.shape[1]+8))
        paddedglcm[4:glcm.shape[0]+4,4:glcm.shape[1]+4]=glcm[:,:,0,0]
        axs[l,m].imshow(chunk, vmin=0, vmax=255, cmap='gray')
        axs[l,m+1].imshow(paddedglcm, cmap=mymap2)
        l=l+1
        if l%2==0:
            l=0
            m=m+2
    plt.show()
    
    
    #Repeating this with min max and central value-
    plt.figure(figsize=(20,4), dpi=2000)
    fig, axs = plt.subplots(1,6)
    fig.set_size_inches(16, 2.75)
        
    for i in range(3):
        chunk,glcm=subshowlist[i]
        pglcm=np.zeros((glcm.shape[0]+8,glcm.shape[1]+8))
        pglcm[4:glcm.shape[0]+4,4:glcm.shape[1]+4]=glcm[:,:,0,0]
        
        axs[i*2].imshow(chunk, vmin=0, vmax=255, cmap='gray')
        axs[i*2].set_title("Image")
        axs[i*2].set_yticklabels([])
        axs[i*2].set_xticklabels([])
        axs[i*2].set_xticks([])
        axs[i*2].set_yticks([])
        axs[i*2+1].imshow(paddedglcm, cmap=mymap2)
        axs[i*2+1].set_title("GLCM")
   
    fig.suptitle('Minimum                                               Central Value                                                     Maximum', size=18)
    plt.show()
    
def corbydirection(FullFeatArray):
    titlelist=["Horizontal", "Vertical", "45", "135"]
    for i in range(4):
        cor=np.corrcoef(FullFeatArray[:,i,:].astype('float64').T)
        plt.title("Feature Correlation " + titlelist[i])
        f=plt.imshow(cor)
        plt.colorbar(f)
        plt.title("Correlation of Feature Values")
        plt.xlabel("Feature Number")
        plt.ylabel("Feature Number")
        plt.xticks([0,1, 2, 3,4,5,6,7,8,9,10,11,12,13], ['1', '2', '3','4', '5', '6','7', '8', '9','10', '11', '12','13', '14'])
        plt.yticks([0,1, 2, 3,4,5,6,7,8,9,10,11,12,13], ['1', '2', '3','4', '5', '6','7', '8', '9','10', '11', '12','13', '14'])
        plt.show()
    return()
