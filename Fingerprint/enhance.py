# -*- coding: utf-8 -*-

import numpy as np
import cv2
import matplotlib.pylab as plt
import sys

from scipy import ndimage
from scipy import signal
import scipy
import scipy.ndimage

import math

def frequest(im,orientim,windsze,minWaveLength,maxWaveLength):
    rows,cols = np.shape(im)
    
    # Find mean orientation within the block. This is done by averaging the
    # sines and cosines of the doubled angles before reconstructing the
    # angle again.  This avoids wraparound problems at the origin.
        
    cosorient = np.mean(np.cos(2*orientim))
    sinorient = np.mean(np.sin(2*orientim))
    orient = math.atan2(sinorient,cosorient)/2
    
    # Rotate the image block so that the ridges are vertical    
    
    #ROT_mat = cv2.getRotationMatrix2D((cols/2,rows/2),orient/np.pi*180 + 90,1)    
    #rotim = cv2.warpAffine(im,ROT_mat,(cols,rows))
    rotim = scipy.ndimage.rotate(im,orient/np.pi*180 + 90,axes=(1,0),reshape = False,order = 3,mode = 'nearest')

    # Now crop the image so that the rotated image does not contain any
    # invalid regions.  This prevents the projection down the columns
    # from being mucked up.
    
    cropsze = int(np.fix(rows/np.sqrt(2)))
    offset = int(np.fix((rows-cropsze)/2))
    rotim = rotim[offset:offset+cropsze][:,offset:offset+cropsze]
    
    # Sum down the columns to get a projection of the grey values down
    # the ridges.
    
    proj = np.sum(rotim,axis = 0)
    dilation = scipy.ndimage.grey_dilation(proj, windsze,structure=np.ones(windsze))

    temp = np.abs(dilation - proj)
    
    peak_thresh = 2
    
    maxpts = (temp<peak_thresh) & (proj > np.mean(proj))
    maxind = np.where(maxpts)
    
    rows_maxind,cols_maxind = np.shape(maxind)
    
    # Determine the spatial frequency of the ridges by divinding the
    # distance between the 1st and last peaks by the (No of peaks-1). If no
    # peaks are detected, or the wavelength is outside the allowed bounds,
    # the frequency image is set to 0    
    
    if(cols_maxind<2):
        freqim = np.zeros(im.shape)
    else:
        NoOfPeaks = cols_maxind
        waveLength = (maxind[0][cols_maxind-1] - maxind[0][0])/(NoOfPeaks - 1)
        if waveLength>=minWaveLength and waveLength<=maxWaveLength:
            freqim = 1/np.double(waveLength) * np.ones(im.shape)
        else:
            freqim = np.zeros(im.shape)
        
    return freqim

def ridge_freq(im, mask, orient, blksze, windsze,minWaveLength, maxWaveLength):
    rows,cols = im.shape
    freq = np.zeros((rows,cols))
    
    for r in range(0,rows-blksze,blksze):
        for c in range(0,cols-blksze,blksze):
            blkim = im[r:r+blksze][:,c:c+blksze]
            blkor = orient[r:r+blksze][:,c:c+blksze]
            
            freq[r:r+blksze][:,c:c+blksze] = frequest(blkim,blkor,windsze,minWaveLength,maxWaveLength)
    
    freq = freq*mask
    freq_1d = np.reshape(freq,(1,rows*cols))
    ind = np.where(freq_1d>0)
    
    ind = np.array(ind)
    ind = ind[1,:]
    
    non_zero_elems_in_freq = freq_1d[0][ind]
    
    meanfreq = np.mean(non_zero_elems_in_freq)
    medianfreq = np.median(non_zero_elems_in_freq)         # does not work properly
    return(freq,meanfreq)

def ridge_filter(im, orient, freq, kx, ky):
    angleInc = 3
    im = np.double(im)
    rows,cols = im.shape
    newim = np.zeros((rows,cols))
    
    freq_1d = np.reshape(freq,(1,rows*cols))
    ind = np.where(freq_1d>0)
    
    ind = np.array(ind)
    ind = ind[1,:]
    
    # Round the array of frequencies to the nearest 0.01 to reduce the
    # number of distinct frequencies we have to deal with.    
    
    non_zero_elems_in_freq = freq_1d[0][ind]
    non_zero_elems_in_freq = np.double(np.round((non_zero_elems_in_freq*100)))/100
    
    unfreq = np.unique(non_zero_elems_in_freq)

    # Generate filters corresponding to these distinct frequencies and
    # orientations in 'angleInc' increments.
    
    sigmax = 1/unfreq[0]*kx
    sigmay = 1/unfreq[0]*ky
    
    sze = np.int(np.round(3*np.max([sigmax,sigmay])))
    
    x,y = np.meshgrid(np.linspace(-sze,sze,(2*sze + 1)),np.linspace(-sze,sze,(2*sze + 1)))
    
    reffilter = np.exp(-(( (np.power(x,2))/(sigmax*sigmax) + (np.power(y,2))/(sigmay*sigmay)))) * np.cos(2*np.pi*unfreq[0]*x) # this is the original gabor filter
    
    filt_rows, filt_cols = reffilter.shape
    
    gabor_filter = np.array(np.zeros((int(180/angleInc),filt_rows,filt_cols)))
    
    for o in range(0,int(180/angleInc)):
        
        # Generate rotated versions of the filter.  Note orientation
        # image provides orientation *along* the ridges, hence +90
        # degrees, and imrotate requires angles +ve anticlockwise, hence
        # the minus sign.        
        
        rot_filt = scipy.ndimage.rotate(reffilter,-(o*angleInc + 90),reshape = False)
        gabor_filter[o] = rot_filt
                
    # Find indices of matrix points greater than maxsze from the image
    # boundary
    
    maxsze = int(sze)

    temp = freq>0;    
    validr,validc = np.where(temp)    
    
    temp1 = validr>maxsze
    temp2 = validr<rows - maxsze
    temp3 = validc>maxsze
    temp4 = validc<cols - maxsze
    
    final_temp = temp1 & temp2 & temp3 & temp4;    
    
    finalind = np.where(final_temp)
    
    # Convert orientation matrix values from radians to an index value
    # that corresponds to round(degrees/angleInc)    
    
    maxorientindex = np.round(180/angleInc)
    orientindex = np.round(orient/np.pi*180/angleInc)
    
    #do the filtering    
    
    for i in range(0,rows):
        for j in range(0,cols):
            if(orientindex[i][j] < 1):
                orientindex[i][j] = orientindex[i][j] + maxorientindex
            if(orientindex[i][j] > maxorientindex):
                orientindex[i][j] = orientindex[i][j] - maxorientindex
    finalind_rows,finalind_cols = np.shape(finalind)
    sze = int(sze)
    for k in range(0,finalind_cols):
        r = validr[finalind[0][k]]
        c = validc[finalind[0][k]]
        
        img_block = im[r-sze:r+sze + 1][:,c-sze:c+sze + 1]
        
        newim[r][c] = np.sum(img_block * gabor_filter[int(orientindex[r][c]) - 1])
        
    return newim

def ridge_orient(im, gradientsigma, blocksigma, orientsmoothsigma):
    rows,cols = im.shape
    #Calculate image gradients.
    sze = np.fix(6*gradientsigma)
    if np.remainder(sze,2) == 0:
        sze = sze+1
        
    gauss = cv2.getGaussianKernel(np.int(sze),gradientsigma)
    f = gauss * gauss.T
    
    fy,fx = np.gradient(f)     #Gradient of Gaussian
    
    #Gx = ndimage.convolve(np.double(im),fx);
    #Gy = ndimage.convolve(np.double(im),fy);
    
    Gx = signal.convolve2d(im,fx,mode='same')
    Gy = signal.convolve2d(im,fy,mode='same')
    
    Gxx = np.power(Gx,2)
    Gyy = np.power(Gy,2)
    Gxy = Gx*Gy
    
    #Now smooth the covariance data to perform a weighted summation of the data.    
    
    sze = np.fix(6*blocksigma)
    
    gauss = cv2.getGaussianKernel(np.int(sze),blocksigma)
    f = gauss * gauss.T
    
    Gxx = ndimage.convolve(Gxx,f)
    Gyy = ndimage.convolve(Gyy,f)
    Gxy = 2*ndimage.convolve(Gxy,f)
    
    # Analytic solution of principal direction
    denom = np.sqrt(np.power(Gxy,2) + np.power((Gxx - Gyy),2)) + np.finfo(float).eps
    
    sin2theta = Gxy/denom;            # Sine and cosine of doubled angles
    cos2theta = (Gxx-Gyy)/denom
    
    
    if orientsmoothsigma:
        sze = np.fix(6*orientsmoothsigma);
        if np.remainder(sze,2) == 0:
            sze = sze+1;    
        gauss = cv2.getGaussianKernel(np.int(sze),orientsmoothsigma)
        f = gauss * gauss.T
        cos2theta = ndimage.convolve(cos2theta,f); # Smoothed sine and cosine of
        sin2theta = ndimage.convolve(sin2theta,f); # doubled angles
    
    orientim = np.pi/2 + np.arctan2(sin2theta,cos2theta)/2
    return orientim

def normalise(img,mean,std):
    normed = (img - np.mean(img))/(np.std(img))
    return normed
    
def ridge_segment(im,blksze,thresh):
    
    rows,cols = im.shape
    
    im = normalise(im,0,1)    # normalise to get zero mean and unit standard deviation
    
    new_rows =  np.int(blksze * np.ceil((np.float(rows))/(np.float(blksze))))
    new_cols =  np.int(blksze * np.ceil((np.float(cols))/(np.float(blksze))))
    
    padded_img = np.zeros((new_rows,new_cols))
    stddevim = np.zeros((new_rows,new_cols))
    
    padded_img[0:rows][:,0:cols] = im
    
    for i in range(0,new_rows,blksze):
        for j in range(0,new_cols,blksze):
            block = padded_img[i:i+blksze][:,j:j+blksze]
            
            stddevim[i:i+blksze][:,j:j+blksze] = np.std(block)*np.ones(block.shape)
    
    stddevim = stddevim[0:rows][:,0:cols]
    
    # cv2.imshow("window", stddevim)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
                    
    mask = stddevim > thresh
    
    mean_val = np.mean(im[mask])
    
    std_val = np.std(im[mask])
    
    normim = (im - mean_val)/(std_val)
    
    return(normim,mask)

def enhance_image(img):
        
#     if(len(sys.argv)<2):
#         print('No Image path given')
#         sys.exit(0)
# #        img_name = '1.jpg'
# #        img_name = '3_7.png'
# #        img = cv2.imread('../images/PNG/' + img_name)
#     elif(len(sys.argv) >= 2):
#         img_name = sys.argv[1]
        # img = cv2.imread(sys.argv[1])
        
    if(len(img.shape)>2):
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blksze = 16
    thresh = 0.1
    normim,mask = ridge_segment(img,blksze,thresh)

    gradientsigma = 1
    blocksigma = 7
    orientsmoothsigma = 7
    orientim = ridge_orient(normim, gradientsigma, blocksigma, orientsmoothsigma)

    blksze = 38
    windsze = 5
    minWaveLength = 5
    maxWaveLength = 15
    freq,medfreq = ridge_freq(normim, mask, orientim, blksze, windsze, minWaveLength,maxWaveLength)    #find the overall frequency of ridges

    freq = medfreq*mask
    kx = 0.65
    ky = 0.65
    newim = ridge_filter(normim, orientim, freq, kx, ky)       # create gabor filter and do the actual filtering
    newim = newim < -3
    return newim
    # plt.imshow(np.asarray(newim),cmap='gray')
    # plt.show()
