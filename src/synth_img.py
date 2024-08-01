#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 12:02:20 2024

@author: janmejoyarch
"""

import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
import os
import datetime

def prep_header(fname, comment):
    header=fits.Header()
    header['FNAME']=(fname, 'filename')
    header['MFG_DATE']= (str(datetime.date.today()), "Date of generating this image")
    header['COMMENTS']=(comment)
    return (header)

def image_gen():
    flat50k= np.ones((25, 25))*5e4
    noisy50k= np.random.poisson(flat50k)
    gradient= np.ones((25,25))
    col_count= np.linspace(5e4, 1e4, 25)
    for i in range(25):
        gradient[:,i]=col_count[i]
    noisy_gradient=np.random.poisson(gradient)
    flat10k= np.ones((25, 25))*1e4
    full_image= np.hstack((flat50k, noisy50k, noisy_gradient, flat10k))
    return full_image

save= True
sav= os.path.expanduser('~/Dropbox/Janmejoy_SUIT_Dropbox/writing_and_presentations/SUIT_meetings/payload_baking/baking_closeout_project/products/')

img1= image_gen()
hdu1=fits.PrimaryHDU(img1, header=prep_header('img1.fits', 'Flat50k -> Noisy_50k -> Noisy_50k-10k_gradient -> Flat10k'))
img2= image_gen()
hdu2=fits.PrimaryHDU(img2, header=prep_header('img2.fits', 'Flat50k -> Noisy_50k -> Noisy_50k-10k_gradient -> Flat10k'))
div= img1/img2
hdu3=fits.PrimaryHDU(div, header=prep_header('div.fits', 'img1/img2'))

if save: 
    hdu1.writeto(os.path.join(sav, 'img1.fits'), overwrite=True)
    hdu2.writeto(os.path.join(sav, 'img2.fits'), overwrite=True)
    hdu3.writeto(os.path.join(sav, 'div.fits'), overwrite=True)

plt.figure("Figure2")
plt.subplot(3,1,1)
plt.imshow(img1, origin='lower', cmap='jet')
plt.title('img1')
plt.colorbar()
plt.subplot(3,1,2)
plt.imshow(img2, origin='lower', cmap='jet')
plt.colorbar()
plt.title('img2')
plt.subplot(3,1,3)
plt.imshow(div, origin='lower', cmap='jet')
plt.colorbar()
plt.title('img1/img2')